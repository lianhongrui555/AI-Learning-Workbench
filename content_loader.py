"""课程内容加载和 Markdown 渲染工具。"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

# 项目根目录和内容目录。
PROJECT_DIR = Path(__file__).resolve().parent
CONTENT_DIR = PROJECT_DIR / "content"
LESSON_DIR = CONTENT_DIR / "lessons"


def _load_json(path: Path) -> Any:
    """读取 JSON 文件并返回 Python 数据。"""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_curriculum() -> dict[str, Any]:
    """读取课程元数据，并检查每节课的 Markdown 文件是否存在。"""
    data = _load_json(CONTENT_DIR / "curriculum.json")
    lessons = data.get("lessons", [])
    for lesson in lessons:
        lesson_path = LESSON_DIR / lesson["file"]
        if not lesson_path.exists():
            raise FileNotFoundError(f"课程文件不存在：{lesson_path}")
    return data


def load_projects() -> list[dict[str, Any]]:
    """读取项目实战卡片数据。"""
    return _load_json(CONTENT_DIR / "projects.json")


def get_lessons() -> list[dict[str, Any]]:
    """返回按顺序排列的课程列表。"""
    return sorted(load_curriculum().get("lessons", []), key=lambda item: item["number"])


def get_lesson(lesson_id: str) -> dict[str, Any] | None:
    """按课程编号查找一节课。"""
    return next((lesson for lesson in get_lessons() if lesson["id"] == lesson_id), None)


def get_project(project_id: str) -> dict[str, Any] | None:
    """按项目编号查找一个实战项目。"""
    return next((project for project in load_projects() if project["id"] == project_id), None)


def get_projects() -> list[dict[str, Any]]:
    """返回全部项目实战数据。"""
    return load_projects()


def read_lesson_markdown(lesson_id: str) -> str:
    """读取一节课的 Markdown 正文。"""
    lesson = get_lesson(lesson_id)
    if lesson is None:
        raise KeyError(f"课程不存在：{lesson_id}")
    return (LESSON_DIR / lesson["file"]).read_text(encoding="utf-8")


def _inline_markdown(text: str) -> str:
    """把 Markdown 行内元素转换成安全的 HTML。"""
    # 先转义 HTML，避免课程文件中的标签直接进入浏览器。
    escaped = html.escape(text)
    code_tokens: dict[str, str] = {}

    def replace_code(match: re.Match[str]) -> str:
        token = f"@@CODE{len(code_tokens)}@@"
        code_tokens[token] = f"<code>{match.group(1)}</code>"
        return token

    # 先把行内代码取出来，避免其中内容继续被处理。
    escaped = re.sub(r"`([^`]+)`", replace_code, escaped)

    # 支持安全的 http/https 链接。
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        escaped,
    )
    # 支持加粗。
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    # 恢复行内代码。
    for token, value in code_tokens.items():
        escaped = escaped.replace(token, value)
    return escaped


def render_markdown(text: str) -> str:
    """把课程使用的简单 Markdown 转成 HTML。"""
    lines = text.splitlines()
    parts: list[str] = []
    paragraph: list[str] = []
    code_lines: list[str] = []
    code_language = ""
    in_code = False
    list_type: str | None = None

    def flush_paragraph() -> None:
        if paragraph:
            parts.append("<p>" + " ".join(paragraph) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            parts.append(f"</{list_type}>")
            list_type = None

    def open_list(kind: str) -> None:
        nonlocal list_type
        if list_type != kind:
            close_list()
            parts.append(f"<{kind}>")
            list_type = kind

    for raw_line in lines:
        stripped = raw_line.strip()

        if stripped.startswith("```"):
            if in_code:
                language_class = f' class="language-{html.escape(code_language)}"' if code_language else ""
                parts.append(f"<pre><code{language_class}>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                code_language = ""
                in_code = False
            else:
                flush_paragraph()
                close_list()
                in_code = True
                code_language = stripped[3:].strip()
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            close_list()
            level = len(heading_match.group(1))
            parts.append(f"<h{level}>{_inline_markdown(heading_match.group(2))}</h{level}>")
            continue

        bullet_match = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet_match:
            flush_paragraph()
            open_list("ul")
            parts.append(f"<li>{_inline_markdown(bullet_match.group(1))}</li>")
            continue

        number_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if number_match:
            flush_paragraph()
            open_list("ol")
            parts.append(f"<li>{_inline_markdown(number_match.group(1))}</li>")
            continue

        quote_match = re.match(r"^>\s?(.*)$", stripped)
        if quote_match:
            flush_paragraph()
            close_list()
            parts.append(f"<blockquote>{_inline_markdown(quote_match.group(1))}</blockquote>")
            continue

        if stripped in {"---", "***"}:
            flush_paragraph()
            close_list()
            parts.append("<hr>")
            continue

        paragraph.append(_inline_markdown(stripped))

    if in_code:
        parts.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    flush_paragraph()
    close_list()
    return "\n".join(parts)