import tempfile
from pathlib import Path
import unittest

import app as tracker_app


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        tracker_app.DB_PATH = Path(self.tmpdir.name) / "test.db"
        tracker_app.app.config.update(TESTING=True, SECRET_KEY="test")
        tracker_app.init_db()
        self.client = tracker_app.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_register_login_and_create_card(self):
        self.client.post("/register", data={"username": "demo", "password": "pass"})
        self.client.post("/login", data={"username": "demo", "password": "pass"})
        response = self.client.post(
            "/cards/new",
            data={
                "title": "Two Sum",
                "tag": "arrays",
                "prompt": "How would you solve Two Sum?",
                "answer": "Hash map in O(n)",
                "confidence": "3",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Card created", response.data)


if __name__ == "__main__":
    unittest.main()
