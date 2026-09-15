import unittest
import uuid

from app.schemas import ChatMessage
from app.services.agent import generate_response
from app.services.auth import authenticate_user, register_user
from app.services.knowledge import add_knowledge, list_knowledge
from app.services.progress import add_progress, get_progress_summary


class SRSFeatureTests(unittest.TestCase):
    def test_register_login_flow(self):
        email = f"alice_{uuid.uuid4().hex[:8]}@example.com"
        register_user("alice", email, "password123")
        user = authenticate_user(email, "password123")

        self.assertIsNotNone(user)
        self.assertEqual(user["email"], email)

    def test_progress_summary_identifies_weak_areas(self):
        email = f"alice_{uuid.uuid4().hex[:8]}@example.com"
        add_progress(
            email,
            {
                "problem_id": "p-101",
                "name": "Two Sum",
                "topic": "Arrays",
                "difficulty": "Easy",
                "status": "solved",
                "attempts": 1,
            },
        )
        add_progress(
            email,
            {
                "problem_id": "p-102",
                "name": "Binary Search",
                "topic": "Binary Search",
                "difficulty": "Medium",
                "status": "attempted",
                "attempts": 2,
            },
        )
        summary = get_progress_summary(email)

        self.assertGreaterEqual(summary["solved_count"], 1)
        self.assertIn("weak_topics", summary)

    def test_knowledge_management_and_practice_plan(self):
        add_knowledge(
            {
                "id": "doc-001",
                "title": "Dynamic Programming Basics",
                "content_type": "concept",
                "topic": "Dynamic Programming",
                "subtopic": "Memoization",
                "pattern": "DP",
                "difficulty": "Medium",
                "content": "Use memoization to store subproblem answers."
            }
        )
        docs = list_knowledge()
        self.assertTrue(any(doc["title"] == "Dynamic Programming Basics" for doc in docs))

        result = generate_response(ChatMessage(message="Create a 3-problem medium dynamic programming practice plan", mode="practice-plan"))
        self.assertIn("practice", result.response.lower())
        self.assertIn("dynamic programming", result.response.lower())


if __name__ == "__main__":
    unittest.main()
