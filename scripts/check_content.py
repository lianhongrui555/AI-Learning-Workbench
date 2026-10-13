"""检查课程文件和练习数据是否完整。"""

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
if len(lessons) != 17:
    errors.append(f"课程数量应为 17，实际为 {len(lessons)}")

for lesson in lessons:
    lesson_file = CONTENT / "lessons" / lesson.get("file", "")
    if not lesson_file.exists():
        errors.append(f"缺少课程文件：{lesson_file}")
    if len(lesson.get("quiz", [])) != 3:
        errors.append(f"{lesson.get('id')} 的概念题不是 3 道")
    code_quiz = lesson.get("code_quiz", [])
    if len(code_quiz) != 3:
        errors.append(f"{lesson.get('id')} 的代码题不是 3 道")
    kinds = {item.get("kind") for item in code_quiz}
    if kinds != expected_kinds:
        errors.append(f"{lesson.get('id')} 的代码题型不完整：{sorted(kinds)}")
    if "practice" in lesson:
        errors.append(f"{lesson.get('id')} 不应再包含 practice 动手任务字段")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"内容检查通过：{len(lessons)} 节课程，包含概念题和代码阅读题")