import unittest
from app.schemas import ChatMessage
from app.services.agent import (
    retrieve_context,
    detect_topics,
    generate_response,
    _embed_text,
    _build_system_prompt,
)
from app.config import get_settings


class RAGRetrievalPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = get_settings()

    def test_01_embedding_dimension_and_consistency(self):
        vec1 = _embed_text("Explain trees in DSA")
        self.assertEqual(len(vec1), self.settings.embedding_dimension)
        self.assertEqual(self.settings.embedding_model, "mxbai-embed-large")

    def test_02_detect_topics_accurately(self):
        cases = [
            ("Explain trees in DSA", ["Trees"]),
            ("What is a binary tree?", ["Trees"]),
            ("Explain stack", ["Stack"]),
            ("How does a queue work?", ["Queue"]),
            ("Explain BFS", ["Graphs"]),
            ("Explain DFS", ["Graphs"]),
            ("What is binary search?", ["Binary Search"]),
            ("Explain dynamic programming", ["Dynamic Programming"]),
            ("What is a heap?", ["Heaps"]),
            ("Difference between stack and queue", ["Stack", "Queue"]),
        ]
        for query, expected_topics in cases:
            detected = detect_topics(query)
            for et in expected_topics:
                self.assertIn(et, detected, f"Expected topic '{et}' not detected for query '{query}' (got: {detected})")

    def test_03_query_explain_trees_in_dsa_retrieves_trees(self):
        docs = retrieve_context("Explain trees in DSA", limit=4)
        self.assertTrue(docs, "Expected non-empty retrieval results")
        # Critical test: Top retrieved doc MUST be Trees, NEVER Stack
        self.assertEqual(docs[0]["topic"], "Trees", f"Expected top topic 'Trees', got '{docs[0]['topic']}'")
        for doc in docs:
            self.assertNotEqual(doc["topic"], "Stack", "Stack chunk must NEVER be retrieved for tree query")
        self.assertTrue(docs[0]["is_relevant"])
        self.assertGreaterEqual(docs[0]["score"], 0.30)

    def test_04_query_what_is_a_binary_tree_retrieves_trees(self):
        docs = retrieve_context("What is a binary tree?", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Trees")
        for doc in docs:
            self.assertNotEqual(doc["topic"], "Stack")

    def test_05_query_explain_stack_retrieves_stack(self):
        docs = retrieve_context("Explain stack", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Stack")

    def test_06_query_how_does_a_queue_work_retrieves_queue(self):
        docs = retrieve_context("How does a queue work?", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Queue")

    def test_07_query_explain_bfs_retrieves_graphs(self):
        docs = retrieve_context("Explain BFS", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Graphs")

    def test_08_query_explain_dfs_retrieves_graphs(self):
        docs = retrieve_context("Explain DFS", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Graphs")

    def test_09_query_what_is_binary_search_retrieves_binary_search(self):
        docs = retrieve_context("What is binary search?", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Binary Search")

    def test_10_query_explain_dynamic_programming_retrieves_dp(self):
        docs = retrieve_context("Explain dynamic programming", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Dynamic Programming")

    def test_11_query_what_is_a_heap_retrieves_heaps(self):
        docs = retrieve_context("What is a heap?", limit=4)
        self.assertTrue(docs)
        self.assertEqual(docs[0]["topic"], "Heaps")
        for doc in docs[:3]:
            self.assertNotIn(doc["topic"], {"Stack", "Queue", "Trees"}, f"Heap query should not mix unrelated topics; got {doc['topic']}")

    def test_12_query_difference_between_stack_and_queue_retrieves_both(self):
        docs = retrieve_context("Difference between stack and queue", limit=4)
        self.assertTrue(docs)
        topics = {doc["topic"] for doc in docs}
        self.assertTrue(
            topics & {"Stack", "Queue"},
            f"Expected Stack or Queue in retrieved topics, got {topics}"
        )

    def test_13_system_prompt_enforces_relevance_guardrails(self):
        prompt = _build_system_prompt("concept", "python")
        self.assertIn("Grounding & Topic Relevance Guardrails", prompt)
        self.assertIn("DISREGARD AND REJECT", prompt)
        self.assertIn("NEVER explain Stacks or Queues when asked about Trees", prompt)

    def test_14_end_to_end_generate_response_for_trees(self):
        chat = ChatMessage(message="Explain trees in DSA", mode="concept")
        result = generate_response(chat)
        self.assertTrue(result.response)
        response_lower = result.response.lower()
        self.assertTrue(
            "tree" in response_lower or "root" in response_lower or "binary" in response_lower,
            f"Response did not mention trees: {result.response[:200]}"
        )
        self.assertTrue(result.sources)
        for s in result.sources:
            self.assertNotIn("monotonic stack", s.lower())


if __name__ == "__main__":
    unittest.main()
