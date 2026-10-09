import unittest

from content_loader import get_lessons, get_projects, load_curriculum, read_lesson_markdown, render_markdown


class ContentLoaderTests(unittest.TestCase):
    def test_curriculum_has_twelve_lessons(self):
        self.assertEqual(len(get_lessons()), 12)

    def test_every_lesson_has_three_quizzes_and_markdown(self):
        for lesson in get_lessons():
            self.assertEqual(len(lesson["quiz"]), 3, lesson["id"])
            self.assertTrue(read_lesson_markdown(lesson["id"]).strip(), lesson["id"])

    def test_projects_are_available(self):
        projects = get_projects()
        self.assertEqual(len(projects), 3)
        self.assertEqual({project["id"] for project in projects}, {"local-ai-agent", "code-harness", "yolo-detection"})

    def test_markdown_renderer(self):
        html = render_markdown("# 标题\n\n这是一个**测试**。\n\n```python\nprint('ok')\n```")
        self.assertIn("<h1>标题</h1>", html)
        self.assertIn("<strong>测试</strong>", html)
        self.assertIn("<pre><code", html)


if __name__ == "__main__":
    unittest.main()