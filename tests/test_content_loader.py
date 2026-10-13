import unittest

from content_loader import get_lessons, get_projects, read_lesson_markdown, render_markdown


class ContentLoaderTests(unittest.TestCase):
    def test_curriculum_has_twenty_seven_lessons(self):
        self.assertEqual(len(get_lessons()), 27)

    def test_every_lesson_has_concept_and_code_quizzes(self):
        knowledge_points = []
        for lesson in get_lessons():
            self.assertEqual(len(lesson["quiz"]), 3, lesson["id"])
            self.assertEqual(len(lesson["code_quiz"]), 3, lesson["id"])
            self.assertEqual({item["kind"] for item in lesson["code_quiz"]}, {"output", "bug", "parameter"})
            self.assertTrue(read_lesson_markdown(lesson["id"]).strip(), lesson["id"])
            knowledge_points.extend(item["knowledge_point"] for item in lesson["code_quiz"])
        self.assertEqual(len(knowledge_points), len(set(knowledge_points)))

    def test_new_project_lessons_have_steps_and_exercises(self):
        project_lessons = [lesson for lesson in get_lessons() if lesson.get("project")]
        self.assertEqual(len(project_lessons), 10)
        for lesson in project_lessons:
            self.assertGreaterEqual(len(lesson["project"]["steps"]), 4)
            self.assertGreaterEqual(len(lesson["project"]["exercises"]), 2)
            self.assertTrue(lesson["project"]["deliverable"])

    def test_projects_are_available(self):
        self.assertEqual(len(get_projects()), 4)

    def test_markdown_renderer(self):
        html = render_markdown("# 标题\n\n这是一个**测试**。\n\n```python\nprint('ok')\n```")
        self.assertIn("<h1>标题</h1>", html)
        self.assertIn("<strong>测试</strong>", html)
        self.assertIn("<pre><code", html)


if __name__ == "__main__":
    unittest.main()