"""检查课程文件、题目和项目步骤是否完整。"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

with (CONTENT / "curriculum.json").open("r", encoding="utf-8") as file:
    data = json.load(file)

lessons = data.get("lessons", [])
errors = []
expected_kinds = {"output", "bug", "parameter"}
knowledge_points = []
question_texts = []
code_snippets = []

if len(lessons) != 27:
    errors.append(f"课程数量应为 27，实际为 {len(lessons)}")

for lesson in lessons:
    lesson_file = CONTENT / "lessons" / lesson.get("file", "")
    if not lesson_file.exists():
        errors.append(f"缺少课程文件：{lesson_file}")
    if len(lesson.get("quiz", [])) != 3:
        errors.append(f"{lesson.get('id')} 的概念题不是 3 道")
    code_quiz = lesson.get("code_quiz", [])
    if len(code_quiz) != 3:
        errors.append(f"{lesson.get('id')} 的代码题不是 3 道")
    if {item.get("kind") for item in code_quiz} != expected_kinds:
        errors.append(f"{lesson.get('id')} 的代码题型不完整")
    for item in code_quiz:
        point = item.get("knowledge_point")
        if point:
            knowledge_points.append(point)
        if item.get("kind") == "bug" and not item.get("error_type"):
            errors.append(f"{lesson.get('id')} {item.get('id')} 缺少 error_type")
        question_texts.append(item.get("question", ""))
        code_snippets.append(item.get("code", ""))
    project = lesson.get("project")
    if lesson.get("number", 0) >= 18:
        if not project:
            errors.append(f"{lesson.get('id')} 缺少 project 项目数据")
        else:
            if not project.get("deliverable"):
                errors.append(f"{lesson.get('id')} 缺少项目交付物")
            if len(project.get("steps", [])) < 4:
                errors.append(f"{lesson.get('id')} 项目步骤少于 4 个")
            if len(project.get("exercises", [])) < 2:
                errors.append(f"{lesson.get('id')} 代码填空少于 2 个")
            for step in project.get("steps", []):
                for field in ("title", "instruction", "expected", "common_errors"):
                    if not step.get(field):
                        errors.append(f"{lesson.get('id')} 步骤 {step.get('id')} 缺少 {field}")
            for exercise in project.get("exercises", []):
                for field in ("title", "prompt", "starter", "answer", "explanation"):
                    if not exercise.get(field):
                        errors.append(f"{lesson.get('id')} 练习 {exercise.get('id')} 缺少 {field}")

if len(knowledge_points) != len(set(knowledge_points)):
    errors.append("存在重复的 knowledge_point")
if len(question_texts) != len(set(question_texts)):
    errors.append("存在重复的代码题文本")
if len(code_snippets) != len(set(code_snippets)):
    errors.append("存在重复的代码片段")
if "KeyError" in json.dumps(data, ensure_ascii=False):
    errors.append("题库仍包含 KeyError 相关代码题")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"内容检查通过：{len(lessons)} 节课程，项目步骤、考点和代码填空完整")