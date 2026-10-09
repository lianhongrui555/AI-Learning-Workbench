import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import create_app


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"answer": "这是测试回答。", "conversation_id": "conversation-1"}


class AppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "DATABASE": str(Path(self.temp_dir.name) / "test.db"),
            "DIFY_TUTOR_API_KEY": "test-key",
            "DIFY_TUTOR_API_URL": "http://localhost/v1/chat-messages",
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health_and_dashboard(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("从零开始".encode("utf-8"), page.data)

    def test_progress_and_note_persist(self):
        self.assertEqual(self.client.post("/api/progress/ai-overview", json={"completed": True}).status_code, 200)
        progress = self.client.get("/api/progress").get_json()["items"]
        self.assertEqual(progress[0]["completed"], 1)
        self.assertEqual(self.client.put("/api/notes/ai-overview", json={"content": "# 我的笔记"}).status_code, 200)
        note = self.client.get("/api/notes/ai-overview").get_json()
        self.assertEqual(note["content"], "# 我的笔记")

    def test_quiz_and_project_progress(self):
        answers = {"q1": 1, "q2": 0, "q3": 0}
        quiz = self.client.post("/api/quiz/ai-overview/submit", json={"answers": answers})
        self.assertEqual(quiz.status_code, 200)
        self.assertEqual(quiz.get_json()["score"], 100)
        project = self.client.post("/api/projects/code-harness/progress", json={"completed": True})
        self.assertEqual(project.status_code, 200)

    def test_tutor_missing_key(self):
        app = create_app({
            "TESTING": True,
            "DATABASE": str(Path(self.temp_dir.name) / "missing.db"),
            "DIFY_TUTOR_API_KEY": "",
        })
        response = app.test_client().post("/api/tutor", json={"lesson_id": "ai-overview", "message": "什么是 AI？"})
        self.assertEqual(response.status_code, 503)

    @patch("app.requests.post", return_value=FakeResponse())
    def test_tutor_success(self, mocked_post):
        response = self.client.post("/api/tutor", json={"lesson_id": "ai-overview", "message": "什么是 AI？"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["answer"], "这是测试回答。")
        self.assertTrue(mocked_post.called)


if __name__ == "__main__":
    unittest.main()