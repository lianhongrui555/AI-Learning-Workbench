"""检查课程文件和自测数据是否完整。"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

with (CONTENT / "curriculum.json").open("r", encoding="utf-8") as file:
    data = json.load(file)

lessons = data.get("lessons", [])
errors = []
if len(lessons) != 12:
    errors.append(f"课程数量应为 12，实际为 {len(lessons)}")

for lesson in lessons:
    lesson_file = CONTENT / "lessons" / lesson.get("file", "")
    if not lesson_file.exists():
        errors.append(f"缺少课程文件：{lesson_file}")
    if len(lesson.get("quiz", [])) != 3:
        errors.append(f"{lesson.get('id')} 的自测题不是 3 道")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"内容检查通过：{len(lessons)} 节课程")