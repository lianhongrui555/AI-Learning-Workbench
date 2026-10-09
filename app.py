"""AI Learning Workbench 的 Flask 后端。"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, abort, g, jsonify, render_template, request

from content_loader import (
    PROJECT_DIR,
    get_lesson,
    get_lessons,
    get_project,
    load_curriculum,
    load_projects,
    read_lesson_markdown,
    render_markdown,
)

# 加载项目根目录下的 .env。
load_dotenv(PROJECT_DIR / ".env")


def utc_now() -> str:
    """返回统一的 UTC 时间字符串。"""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """创建 Flask 应用，方便运行和自动化测试。"""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.getenv("DATABASE_PATH") or str(PROJECT_DIR / "data" / "workbench.db"),
        DIFY_TUTOR_API_URL=os.getenv("DIFY_TUTOR_API_URL") or "http://localhost/v1/chat-messages",
        DIFY_TUTOR_API_KEY=os.getenv("DIFY_TUTOR_API_KEY") or "",
    )
    if test_config:
        app.config.update(test_config)

    # 确保数据目录存在。
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    def get_db() -> sqlite3.Connection:
        """获取当前请求共用的 SQLite 连接。"""
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(_: BaseException | None = None) -> None:
        """请求结束时关闭数据库连接。"""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def ensure_column(db: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        """在旧数据库缺少新列时执行兼容迁移。"""
        columns = {row[1] for row in db.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def init_db() -> None:
        """创建本地进度、笔记、项目和助教数据表。"""
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS lesson_progress (
                lesson_id TEXT PRIMARY KEY,
                completed INTEGER NOT NULL DEFAULT 0,
                score INTEGER,
                last_viewed_at TEXT,
                completed_at TEXT,
                concept_submitted INTEGER NOT NULL DEFAULT 0,
                code_submitted INTEGER NOT NULL DEFAULT 0,
                concept_score INTEGER,
                code_score INTEGER
            );
            CREATE TABLE IF NOT EXISTS notes (
                lesson_id TEXT PRIMARY KEY,
                content TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS project_progress (
                project_id TEXT PRIMARY KEY,
                completed INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tutor_conversations (
                lesson_id TEXT PRIMARY KEY,
                conversation_id TEXT
            );
            CREATE TABLE IF NOT EXISTS tutor_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        # 兼容旧数据库：缺少的新列会自动补齐，不删除旧记录。
        ensure_column(db, "lesson_progress", "concept_submitted", "INTEGER NOT NULL DEFAULT 0")
        ensure_column(db, "lesson_progress", "code_submitted", "INTEGER NOT NULL DEFAULT 0")
        ensure_column(db, "lesson_progress", "concept_score", "INTEGER")
        ensure_column(db, "lesson_progress", "code_score", "INTEGER")

        # 旧版 score 迁移为概念题分数；旧完成记录继续保留。
        db.execute(
            """
            UPDATE lesson_progress
            SET concept_score = COALESCE(concept_score, score),
                concept_submitted = 1
            WHERE score IS NOT NULL
            """
        )
        db.execute(
            """
            UPDATE lesson_progress
            SET code_submitted = 1
            WHERE completed = 1
            """
        )
        db.commit()

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    @app.context_processor
    def inject_navigation() -> dict[str, Any]:
        """给所有模板注入简单的导航信息。"""
        return {"nav_lessons": get_lessons()}

    def require_lesson(lesson_id: str) -> dict[str, Any]:
        """查找课程；不存在时返回 404。"""
        lesson = get_lesson(lesson_id)
        if lesson is None:
            abort(404, description=f"课程不存在：{lesson_id}")
        return lesson

    @app.get("/")
    def dashboard():
        """显示总览看板。"""
        lessons = get_lessons()
        progress_rows = {row["lesson_id"]: dict(row) for row in get_db().execute("SELECT * FROM lesson_progress")}
        project_rows = {row["project_id"]: dict(row) for row in get_db().execute("SELECT * FROM project_progress")}
        completed = sum(1 for lesson in lessons if progress_rows.get(lesson["id"], {}).get("completed"))
        next_lesson = next((lesson for lesson in lessons if not progress_rows.get(lesson["id"], {}).get("completed")), lessons[0])
        projects = load_projects()
        return render_template(
            "dashboard.html",
            lessons=lessons,
            progress_rows=progress_rows,
            project_rows=project_rows,
            project_progress=project_rows,
            completed_count=completed,
            next_lesson=next_lesson,
            projects=projects,
            total_count=len(lessons),
        )

    @app.get("/path")
    def learning_path():
        """显示完整学习路线。"""
        lessons = get_lessons()
        progress_rows = {row["lesson_id"]: dict(row) for row in get_db().execute("SELECT * FROM lesson_progress")}
        modules: dict[str, list[dict[str, Any]]] = {}
        for lesson in lessons:
            modules.setdefault(lesson["module"], []).append(lesson)
        return render_template("path.html", modules=modules, progress_rows=progress_rows)

    @app.get("/lesson/<lesson_id>")
    def lesson_detail(lesson_id: str):
        """显示一节课程和配套工具。"""
        lesson = require_lesson(lesson_id)
        note_row = get_db().execute("SELECT content FROM notes WHERE lesson_id = ?", (lesson_id,)).fetchone()
        progress_row = get_db().execute("SELECT * FROM lesson_progress WHERE lesson_id = ?", (lesson_id,)).fetchone()
        get_db().execute(
            """
            INSERT INTO lesson_progress (lesson_id, completed, last_viewed_at, completed_at)
            VALUES (?, 0, ?, NULL)
            ON CONFLICT(lesson_id) DO UPDATE SET last_viewed_at = excluded.last_viewed_at
            """,
            (lesson_id, utc_now()),
        )
        get_db().commit()
        return render_template(
            "lesson.html",
            lesson=lesson,
            lesson_html=render_markdown(read_lesson_markdown(lesson_id)),
            note=(note_row["content"] if note_row else ""),
            progress=dict(progress_row) if progress_row else {"completed": 0, "concept_submitted": 0, "code_submitted": 0, "concept_score": None, "code_score": None},
        )

    @app.get("/projects")
    def project_gallery():
        """显示现有项目实战卡片。"""
        rows = {row["project_id"]: dict(row) for row in get_db().execute("SELECT * FROM project_progress")}
        return render_template("projects.html", projects=load_projects(), project_progress=rows)

    @app.get("/notes")
    def notes_page():
        """显示全部课程笔记。"""
        lessons = get_lessons()
        note_rows = {row["lesson_id"]: row["content"] for row in get_db().execute("SELECT lesson_id, content FROM notes")}
        return render_template("notes.html", lessons=lessons, notes=note_rows)

    @app.get("/tutor")
    def tutor_page():
        """显示通用 AI 助教页面。"""
        lessons = get_lessons()
        selected = request.args.get("lesson_id", lessons[0]["id"] if lessons else "")
        lesson = get_lesson(selected)
        if lesson is None:
            lesson = lessons[0] if lessons else None
        conversation = None
        if lesson:
            row = get_db().execute("SELECT conversation_id FROM tutor_conversations WHERE lesson_id = ?", (lesson["id"],)).fetchone()
            conversation = row["conversation_id"] if row else None
        return render_template("tutor.html", lessons=lessons, lesson=lesson, conversation_id=conversation)

    @app.get("/health")
    def health():
        """提供简单健康检查。"""
        return jsonify({"status": "ok", "service": "ai-learning-workbench"})

    @app.get("/api/curriculum")
    def api_curriculum():
        """返回课程结构和当前完成状态。"""
        progress_rows = {row["lesson_id"]: dict(row) for row in get_db().execute("SELECT * FROM lesson_progress")}
        curriculum = load_curriculum()
        for lesson in curriculum.get("lessons", []):
            lesson["progress"] = progress_rows.get(lesson["id"], {"completed": 0, "concept_submitted": 0, "code_submitted": 0, "concept_score": None, "code_score": None})
        return jsonify(curriculum)

    @app.get("/api/progress")
    def api_progress():
        """返回所有课程进度。"""
        rows = [dict(row) for row in get_db().execute("SELECT * FROM lesson_progress")]
        return jsonify({"items": rows})


    @app.get("/api/notes/<lesson_id>")
    def api_get_note(lesson_id: str):
        """读取一篇课程笔记。"""
        require_lesson(lesson_id)
        row = get_db().execute("SELECT content, updated_at FROM notes WHERE lesson_id = ?", (lesson_id,)).fetchone()
        return jsonify({"lesson_id": lesson_id, "content": row["content"] if row else "", "updated_at": row["updated_at"] if row else None})

    @app.put("/api/notes/<lesson_id>")
    def api_save_note(lesson_id: str):
        """保存课程 Markdown 笔记。"""
        require_lesson(lesson_id)
        payload = request.get_json(silent=True) or {}
        content = str(payload.get("content", ""))
        now = utc_now()
        get_db().execute(
            """
            INSERT INTO notes (lesson_id, content, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(lesson_id) DO UPDATE SET content = excluded.content, updated_at = excluded.updated_at
            """,
            (lesson_id, content, now),
        )
        get_db().commit()
        return jsonify({"lesson_id": lesson_id, "saved": True, "updated_at": now})

    @app.post("/api/quiz/<lesson_id>/submit")
    def api_submit_quiz(lesson_id: str):
        """批改概念题或代码理解题，并更新课程完成状态。"""
        lesson = require_lesson(lesson_id)
        payload = request.get_json(silent=True) or {}
        quiz_type = str(payload.get("quiz_type", "concept")).strip()
        if quiz_type not in {"concept", "code"}:
            return jsonify({"error": "quiz_type 只能是 concept 或 code。"}), 400

        answers = payload.get("answers", {})
        questions = lesson.get("quiz", []) if quiz_type == "concept" else lesson.get("code_quiz", [])
        correct_count = 0
        details = []
        for question in questions:
            raw_answer = answers.get(question["id"])
            try:
                selected = int(raw_answer)
            except (TypeError, ValueError):
                selected = -1
            is_correct = selected == question["answer"]
            correct_count += 1 if is_correct else 0
            details.append({
                "id": question["id"],
                "kind": question.get("kind"),
                "correct": is_correct,
                "answer": question["answer"],
                "explanation": question.get("explanation", ""),
            })
        total = len(questions)
        score = round(correct_count / total * 100) if total else 0
        now = utc_now()
        db = get_db()
        if quiz_type == "concept":
            db.execute(
                """
                INSERT INTO lesson_progress (lesson_id, concept_submitted, concept_score, score, last_viewed_at)
                VALUES (?, 1, ?, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    concept_submitted = 1,
                    concept_score = excluded.concept_score,
                    score = excluded.score,
                    last_viewed_at = excluded.last_viewed_at
                """,
                (lesson_id, score, score, now),
            )
        else:
            db.execute(
                """
                INSERT INTO lesson_progress (lesson_id, code_submitted, code_score, last_viewed_at)
                VALUES (?, 1, ?, ?)
                ON CONFLICT(lesson_id) DO UPDATE SET
                    code_submitted = 1,
                    code_score = excluded.code_score,
                    last_viewed_at = excluded.last_viewed_at
                """,
                (lesson_id, score, now),
            )

        progress_row = db.execute(
            "SELECT concept_submitted, code_submitted FROM lesson_progress WHERE lesson_id = ?",
            (lesson_id,),
        ).fetchone()
        completed = bool(progress_row["concept_submitted"] and progress_row["code_submitted"])
        db.execute(
            """
            UPDATE lesson_progress
            SET completed = ?,
                completed_at = CASE WHEN ? = 1 THEN COALESCE(completed_at, ?) ELSE NULL END
            WHERE lesson_id = ?
            """,
            (1 if completed else 0, 1 if completed else 0, now, lesson_id),
        )
        db.commit()
        return jsonify({
            "lesson_id": lesson_id,
            "quiz_type": quiz_type,
            "correct": correct_count,
            "total": total,
            "score": score,
            "completed": completed,
            "details": details,
        })

    @app.get("/api/projects")
    def api_projects():
        """返回项目卡片和完成状态。"""
        rows = {row["project_id"]: dict(row) for row in get_db().execute("SELECT * FROM project_progress")}
        projects = []
        for project in load_projects():
            item = dict(project)
            item["progress"] = rows.get(project["id"], {"completed": 0})
            projects.append(item)
        return jsonify({"items": projects})

    @app.post("/api/projects/<project_id>/progress")
    def api_update_project(project_id: str):
        """更新项目实战完成状态。"""
        if get_project(project_id) is None:
            abort(404, description=f"项目不存在：{project_id}")
        payload = request.get_json(silent=True) or {}
        completed = bool(payload.get("completed", True))
        now = utc_now()
        get_db().execute(
            """
            INSERT INTO project_progress (project_id, completed, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(project_id) DO UPDATE SET completed = excluded.completed, updated_at = excluded.updated_at
            """,
            (project_id, 1 if completed else 0, now),
        )
        get_db().commit()
        return jsonify({"project_id": project_id, "completed": completed})

    @app.post("/api/tutor")
    def api_tutor():
        """把当前课程上下文和学生问题发送给 Dify。"""
        payload = request.get_json(silent=True) or {}
        lesson_id = str(payload.get("lesson_id", "")).strip()
        message = str(payload.get("message", "")).strip()
        lesson = require_lesson(lesson_id)
        if not message:
            return jsonify({"error": "问题不能为空。"}), 400

        api_key = app.config.get("DIFY_TUTOR_API_KEY", "")
        endpoint = app.config.get("DIFY_TUTOR_API_URL", "")
        if not api_key or "请在这里" in api_key:
            return jsonify({"error": "尚未配置 AI 助教 API Key。"}), 503

        conversation_row = get_db().execute("SELECT conversation_id FROM tutor_conversations WHERE lesson_id = ?", (lesson_id,)).fetchone()
        conversation_id = conversation_row["conversation_id"] if conversation_row else ""
        prompt = (
            f"当前课程：{lesson['title']}\n"
            f"课程摘要：{lesson.get('summary', '')}\n"
            "请使用中文、类比和分步骤方式回答零基础学习者的问题。"
            f"\n\n学生问题：{message}"
        )
        request_payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "user": "local-learning-workbench",
        }
        if conversation_id:
            request_payload["conversation_id"] = conversation_id
        try:
            response = requests.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=request_payload,
                timeout=300,
            )
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.Timeout:
            return jsonify({"error": "AI 助教响应超时，请稍后重试。"}), 504
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "无法连接 Dify，请确认 Docker Desktop 和 Dify 正在运行。"}), 503
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else 502
            return jsonify({"error": f"AI 助教接口返回错误：HTTP {status_code}"}), 502
        except requests.exceptions.RequestException:
            return jsonify({"error": "调用 AI 助教失败。"}), 502

        answer = result.get("answer")
        if not answer:
            return jsonify({"error": "Dify 没有返回 answer 字段。"}), 502
        new_conversation_id = result.get("conversation_id") or conversation_id
        db = get_db()
        db.execute(
            "INSERT INTO tutor_conversations (lesson_id, conversation_id) VALUES (?, ?) ON CONFLICT(lesson_id) DO UPDATE SET conversation_id = excluded.conversation_id",
            (lesson_id, new_conversation_id),
        )
        db.execute("INSERT INTO tutor_messages (lesson_id, role, content, created_at) VALUES (?, 'user', ?, ?)", (lesson_id, message, utc_now()))
        db.execute("INSERT INTO tutor_messages (lesson_id, role, content, created_at) VALUES (?, 'assistant', ?, ?)", (lesson_id, answer, utc_now()))
        db.commit()
        return jsonify({"answer": answer, "conversation_id": new_conversation_id})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("WEB_HOST", "127.0.0.1"),
        port=int(os.getenv("WEB_PORT", "5000")),
        debug=False,
        use_reloader=False,
    )