import sys
import types
import unittest
import uuid
from unittest.mock import patch

from app.schemas import ChatMessage
from app.services import agent as agent_service
from app.services.agent import generate_response, retrieve_context


class AgentRAGTests(unittest.TestCase):
    def test_generate_response_uses_retrieval_context(self):
        chat = ChatMessage(message="Explain binary search and its time complexity", mode="concept")
        result = generate_response(chat)

        self.assertTrue(result.sources)
        self.assertIn("binary search", result.response.lower())
        self.assertIn("retrieved", result.response.lower())
        self.assertIn("complexity", result.response.lower())

    def test_generate_response_routes_problem_queries(self):
        chat = ChatMessage(message="Solve a two-sum problem and give hints", mode="concept")
        result = generate_response(chat)

        self.assertIn(result.mode, {"problem-analysis", "hint-generation"})
        self.assertTrue(result.response)

    def test_retrieve_context_prefers_best_matching_document(self):
        docs = retrieve_context("binary search and time complexity")

        self.assertTrue(docs)
        self.assertIn("Binary Search", [doc["title"] for doc in docs])

    def test_retrieve_context_uses_embedding_vector_search(self):
        class DummyResponse:
            def __init__(self, payload):
                self.payload = payload

        class DummyCollection:
            def __init__(self, *args, **kwargs):
                self.calls = []

            def get_collection(self, collection_name):
                raise RuntimeError("missing collection")

            def create_collection(self, *args, **kwargs):
                pass

            def upsert(self, *args, **kwargs):
                pass

            def search(self, *args, **kwargs):
                return [DummyResponse({"title": "Binary Search", "content": "Binary search uses the middle element.", "tags": ["search"]})]

        qdrant = types.SimpleNamespace(QdrantClient=lambda *args, **kwargs: DummyCollection())
        qdrant_models = types.SimpleNamespace(
            VectorParams=lambda *args, **kwargs: object(),
            Distance=types.SimpleNamespace(COSINE="cosine"),
            PointStruct=lambda **kwargs: kwargs,
        )

        with patch.dict(sys.modules, {"qdrant_client": qdrant, "qdrant_client.http": types.SimpleNamespace(models=qdrant_models), "qdrant_client.http.models": qdrant_models}):
            with patch.object(agent_service, "_embed_text", return_value=[0.1] * 768, create=True) as mock_embed:
                docs = retrieve_context("How do I search an ordered array efficiently?")

        self.assertTrue(docs)
        self.assertIn("Binary Search", [doc["title"] for doc in docs])
        self.assertGreaterEqual(mock_embed.call_count, 1)
        self.assertIn("How do I search an ordered array efficiently?", [call.args[0] for call in mock_embed.call_args_list])

    def test_generate_response_guides_beginner_ds_roadmap(self):
        chat = ChatMessage(message="I want to start my DS journey in my BTech 2nd year, guide me", mode="concept")
        result = generate_response(chat)

        self.assertEqual(result.mode, "beginner-roadmap")
        answer = result.response.lower()
        self.assertIn("start", answer)
        self.assertIn("arrays", answer)
        self.assertIn("binary search", answer)

    def test_generate_response_uses_langgraph_workflow(self):
        workflow = agent_service.build_agent_workflow()
        state = workflow.invoke({"message": "Explain binary search and its time complexity", "mode": "concept"})

        self.assertIn("route", state)
        self.assertIn("answer", state)
        self.assertTrue(state["answer"])

    def test_persistence_round_trips_user_and_progress(self):
        from app.services.auth import register_user, authenticate_user
        from app.services.progress import add_progress, get_progress_summary

        email = f"bob_{uuid.uuid4().hex[:8]}@example.com"
        register_user("bob", email, "securepass")
        add_progress(email, {"problem_id": "p-222", "name": "Binary Search", "topic": "Binary Search", "difficulty": "Medium", "status": "solved", "attempts": 2})

        user = authenticate_user(email, "securepass")
        summary = get_progress_summary(email)

        self.assertIsNotNone(user)
        self.assertEqual(summary["solved_count"], 1)


if __name__ == "__main__":
    unittest.main()
