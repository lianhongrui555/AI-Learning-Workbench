import sqlite3
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
        self.db_path = str(Path(self.temp_dir.name) / "test.db")
        self.app = create_app({
            "TESTING": True,
            "DATABASE": self.db_path,
            "DIFY_TUTOR_API_KEY": "test-key",
            "DIFY_TUTOR_API_URL": "http://localhost/v1/chat-messages",
        })
        self.client = self.app.test_client()
        self.concept_answers = {"q1": 1, "q2": 0, "q3": 0}
        self.code_answers = {"cq1": 0, "cq2": 1, "cq3": 1}

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health_and_dashboard(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("从零开始".encode("utf-8"), page.data)

    def test_completion_requires_both_quiz_types(self):
        concept = self.client.post("/api/quiz/ai-overview/submit", json={"quiz_type": "concept", "answers": self.concept_answers})
        self.assertEqual(concept.status_code, 200)
        self.assertFalse(concept.get_json()["completed"])
        code = self.client.post("/api/quiz/ai-overview/submit", json={"quiz_type": "code", "answers": self.code_answers})
        self.assertEqual(code.status_code, 200)
        self.assertTrue(code.get_json()["completed"])
        progress = self.client.get("/api/progress").get_json()["items"][0]
        self.assertEqual(progress["completed"], 1)
        self.assertEqual(progress["concept_submitted"], 1)
        self.assertEqual(progress["code_submitted"], 1)

    def test_note_persist(self):
        self.assertEqual(self.client.put("/api/notes/ai-overview", json={"content": "# 我的笔记"}).status_code, 200)
        note = self.client.get("/api/notes/ai-overview").get_json()
        self.assertEqual(note["content"], "# 我的笔记")

    def test_project_progress(self):
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

    def test_legacy_score_migration(self):
        legacy_path = Path(self.temp_dir.name) / "legacy.db"
        connection = sqlite3.connect(legacy_path)
        connection.execute(
            """
            CREATE TABLE lesson_progress (
                lesson_id TEXT PRIMARY KEY,
                completed INTEGER NOT NULL DEFAULT 0,
                score INTEGER,
                last_viewed_at TEXT,
                completed_at TEXT
            )
            """
        )
        connection.execute(
            "INSERT INTO lesson_progress (lesson_id, completed, score) VALUES (?, ?, ?)",
            ("ai-overview", 0, 80),
        )
        connection.commit()
        connection.close()

        migrated_app = create_app({"TESTING": True, "DATABASE": str(legacy_path)})
        progress = migrated_app.test_client().get("/api/progress").get_json()["items"][0]
        self.assertEqual(progress["concept_score"], 80)
        self.assertEqual(progress["concept_submitted"], 1)
        self.assertEqual(progress["code_submitted"], 0)
        self.assertEqual(progress["completed"], 0)


if __name__ == "__main__":
    unittest.main()