import logging
import numpy as np
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)

class SemanticCache:
    """
    Enterprise Semantic Caching Core Layer.
    Simulates high-performance cosine similarity lookup over historical model inference runs
    to avoid redundant high-cost token consumption from commercial upstream APIs.
    """
    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold
        # In-memory vectors storage acting as a hot-tier cache mock (Redis Semantic Vector Simulation)
        self.vector_store: Dict[str, Dict[str, Any]] = {}

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Computes the cosine similarity metric between two spatial vector arrays."""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(dot_product / (norm_v1 * norm_v2))

    async def get(self, query_embedding: np.ndarray) -> Tuple[Optional[str], Optional[float]]:
        """
        Scans the historical hot-tier vector store to resolve similar requests.
        Returns a Tuple containing the cached string resolution and the exact confidence match.
        """
        best_match_response: Optional[str] = None
        highest_score: float = 0.0

        for cache_id, payload in self.vector_store.items():
            cached_embedding = payload["embedding"]
            similarity = self._cosine_similarity(query_embedding, cached_embedding)
            
            if similarity > highest_score:
                highest_score = similarity
                best_match_response = payload["response"]

        if highest_score >= self.similarity_threshold:
            logger.info(f"[FinOps] [Cache Hit] Similarity score: {highest_score:.4f} >= Threshold ({self.similarity_threshold})")
            return best_match_response, highest_score

        logger.info(f"[FinOps] [Cache Miss] Top score found: {highest_score:.4f} < Threshold ({self.similarity_threshold})")
        return None, None

    async def set(self, cache_key_id: str, query_embedding: np.ndarray, response_text: str) -> None:
        """Stores a newly evaluated prompt execution context along with its multidimensional embedding array."""
        self.vector_store[cache_key_id] = {
            "embedding": query_embedding,
            "response": response_text
        }
        logger.info(f"[FinOps] [Cache Store] Key '{cache_key_id}' successfully mapped inside vector space registry.")
