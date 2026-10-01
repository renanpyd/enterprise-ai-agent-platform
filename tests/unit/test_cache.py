import pytest
import numpy as np
from src.core.cache import SemanticCache

def test_cosine_similarity_perfect_match():
    """Validates that two identical multi-dimensional arrays return an absolute correlation score of 1.0."""
    cache = SemanticCache()
    vector_a = np.array([1.0, 2.0, 3.0, 4.0])
    vector_b = np.array([1.0, 2.0, 3.0, 4.0])
    
    score = cache._cosine_similarity(vector_a, vector_b)
    assert pytest.approx(score, rel=1e-5) == 1.0

def test_cosine_similarity_orthogonal():
    """Validates that perpendicular orientation structures produce an exact orthogonal response of 0.0."""
    cache = SemanticCache()
    vector_a = np.array([1.0, 0.0])
    vector_b = np.array([0.0, 1.0])
    
    score = cache._cosine_similarity(vector_a, vector_b)
    assert pytest.approx(score, abs=1e-5) == 0.0

@pytest.mark.asyncio
async def test_cache_hit_and_miss_mechanisms():
    """Verifies that async lookup layers successfully triage execution pipelines based on strict threshold margins."""
    # Instancia o cache com limite estrito de 0.92
    cache = SemanticCache(similarity_threshold=0.92)
    
    base_embedding = np.array([1.0, 0.5, -0.2])
    test_response = "Simulated Analytical Report Payload"
    
    # 1. Armazena o registro inicial no cache vetorial
    await cache.set(cache_key_id="test_key_001", query_embedding=base_embedding, response_text=test_response)
    
    # 2. Cenário de Cache Hit: Busca usando o mesmo vetor exato (similaridade = 1.0)
    hit_payload, hit_score = await cache.get(base_embedding)
    assert hit_payload == test_response
    assert hit_score is not None
    assert hit_score >= 0.92
    
    # 3. Cenário de Cache Miss: Busca usando um vetor completamente diferente
    different_embedding = np.array([-1.0, -0.5, 0.2])
    miss_payload, miss_score = await cache.get(different_embedding)
    assert miss_payload is None
    assert miss_score is None
