import unittest

from app.schemas import ChatMessage
from app.services.agent import generate_response, rewrite_query, _generate_progressive_hint


class AgentEnhancedTests(unittest.TestCase):
    def test_query_rewriting_with_history(self):
        history = [
            {"role": "user", "content": "Explain Trapping Rain Water"},
            {"role": "assistant", "content": "Trapping Rain Water uses two pointers to compute trapped elevation."},
        ]
        rewritten = rewrite_query("What is its time complexity?", history)
        self.assertIn("Trapping Rain Water", rewritten)

    def test_progressive_hint_level_progression(self):
        chat1 = ChatMessage(message="Give me hint 1 for Two Sum", mode="hint")
        res1 = generate_response(chat1)
        self.assertEqual(res1.hint_level, 1)
        self.assertIn("Level 1", res1.response)

        chat2 = ChatMessage(message="Give me hint 3 for Two Sum", mode="hint", hint_level=3)
        res2 = generate_response(chat2)
        self.assertEqual(res2.hint_level, 3)
        self.assertIn("Level 3", res2.response)

    def test_problem_analysis_returns_pattern_and_similar(self):
        chat = ChatMessage(message="How do I solve Trapping Rain Water?", mode="problem-analysis")
        res = generate_response(chat)
        self.assertTrue(res.pattern)
        self.assertIn("Two Pointers", res.pattern)
        self.assertTrue(res.suggested_next_actions)

    def test_multi_language_code_selection(self):
        chat_java = ChatMessage(message="Binary Search", mode="code", language="java")
        res_java = generate_response(chat_java)
        self.assertIn("java", res_java.response.lower())

        chat_py = ChatMessage(message="Binary Search", mode="code", language="python")
        res_py = generate_response(chat_py)
        self.assertIn("def ", res_py.response)

    def test_personalized_progress_and_practice_plan(self):
        chat = ChatMessage(message="Create a practice plan for my next interview", mode="practice-plan", user_email="student@algomentor.com")
        res = generate_response(chat)
        self.assertIn("student@algomentor.com", res.response)
        self.assertIn("Two Sum", res.response)


if __name__ == "__main__":
    unittest.main()
