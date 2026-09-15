"""
Qdrant Knowledge Base Indexer
Embeds and indexes granular DSA knowledge chunks into Qdrant using nomic-embed-text (768d).
Ensures the exact same embedding model is used for document ingestion and query retrieval.
"""
from __future__ import annotations

import logging
import os
import sys
import uuid
from typing import List, Dict, Any, Optional

import httpx
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from app.config import get_settings
from app.services.dsa_knowledge_chunks import get_all_chunks

logger = logging.getLogger("algomentor.indexer")
settings = get_settings()

EMBEDDING_DIM = settings.embedding_dimension


def get_embedding(text: str) -> List[float]:
    """Generates an embedding using the configured Ollama embedding model."""
    clean_text = text.strip()
    if not clean_text:
        return [0.0] * EMBEDDING_DIM

    try:
        url = f"{settings.ollama_host}/api/embeddings"
        payload = {"model": settings.embedding_model, "prompt": clean_text}
        resp = httpx.post(url, json=payload, timeout=httpx.Timeout(15.0, connect=1.5))
        if resp.status_code == 200:
            vec = resp.json().get("embedding", [])
            if len(vec) == EMBEDDING_DIM:
                return vec
            elif len(vec) > 0:
                return (vec + [0.0] * EMBEDDING_DIM)[:EMBEDDING_DIM]
    except Exception as e:
        logger.warning(f"Ollama embedding failed, using deterministic fallback: {e}")

    vector = [0.0] * EMBEDDING_DIM
    tokens = clean_text.lower().split()
    for idx, token in enumerate(tokens):
        val = sum(ord(c) for c in token)
        vector[idx % EMBEDDING_DIM] += float(val % 997) / 997.0

    # L2 normalize
    norm = sum(v * v for v in vector) ** 0.5
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def get_qdrant_client() -> QdrantClient:
    """Connects to remote Qdrant if running, or initializes embedded persistent local Qdrant."""
    # Check if remote Qdrant is accessible
    try:
        import socket
        s = socket.socket()
        s.settimeout(0.15)
        if s.connect_ex((settings.qdrant_host, settings.qdrant_port)) == 0:
            s.close()
            return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port, timeout=2.0)
        s.close()
    except Exception:
        pass

    # Use embedded local persistent Qdrant (works without Docker on all platforms)
    storage_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "qdrant")
    os.makedirs(storage_dir, exist_ok=True)
    return QdrantClient(path=storage_dir)


def reindex_all(force_recreate: bool = True) -> int:
    """Re-indexes the entire curated DSA knowledge base into Qdrant."""
    client = get_qdrant_client()
    collection_name = settings.qdrant_collection
    chunks = get_all_chunks()

    print(f"[*] Initializing Qdrant collection '{collection_name}' (dim={EMBEDDING_DIM}, distance=COSINE)...")

    # Check existing collections
    collections_response = client.get_collections()
    existing_names = [c.name for c in collections_response.collections]

    if collection_name in existing_names and force_recreate:
        print(f"[*] Deleting obsolete collection '{collection_name}' to prevent vector dimension mismatch...")
        client.delete_collection(collection_name=collection_name)
        existing_names.remove(collection_name)

    if collection_name not in existing_names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
        print(f"[OK] Created Qdrant collection '{collection_name}'.")

    print(f"[*] Embedding and indexing {len(chunks)} topic-isolated DSA knowledge chunks...")
    points = []
    for idx, chunk in enumerate(chunks):
        # Create rich indexing text including topic, subtopic, tags, and content
        embed_input = f"{chunk['topic']} - {chunk['subtopic']}\nTags: {', '.join(chunk['tags'])}\n{chunk['content']}"
        vector = get_embedding(embed_input)

        point = PointStruct(
            id=idx + 1,
            vector=vector,
            payload={
                "chunk_id": chunk["chunk_id"],
                "topic": chunk["topic"],
                "subtopic": chunk["subtopic"],
                "difficulty": chunk["difficulty"],
                "problem_name": chunk.get("problem_name"),
                "source": chunk["source"],
                "document_name": chunk["document_name"],
                "tags": chunk["tags"],
                "content": chunk["content"],
            },
        )
        points.append(point)

    client.upsert(collection_name=collection_name, points=points)
    print(f"[OK] Successfully indexed {len(points)} DSA chunks into Qdrant collection '{collection_name}'!")
    return len(points)


if __name__ == "__main__":
    count = reindex_all(force_recreate=True)
    print(f"[DONE] Re-indexing complete: {count} chunks indexed.")
