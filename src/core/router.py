import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelRouterEngine:
    """
    Intelligent Model Routing Core Engine.
    Implements deterministic orchestration logic evaluating query payload weight to programmatic 
    execution bindings (SLM vs. Enterprise Cloud LLM APIs), enforcing FinOps cost containment strategies.
    """
    def __init__(self, local_model_name: str = "llama3.2:3b", cloud_model_name: str = "gpt-4o"):
        self.local_model = local_model_name
        self.cloud_model = cloud_model_name
        # Structural lexical tokens hinting complex logical chains requiring higher analytical capability
        self.complexity_indicators = [
            "arquitetura", "architect", "benchmark", "optimize", 
            "refactor", "pipeline", "etl", "financial", "analytics"
        ]

    async def determine_optimal_route(self, user_prompt: str) -> Dict[str, Any]:
        """
        Parses raw string metadata properties to classify operational constraints.
        Returns a configuration map designating the target engine route and underlying orchestration model.
        """
        normalized_prompt = user_prompt.lower()
        prompt_length = len(normalized_prompt)
        
        # Condition 1: Evaluate structural token intersections indicative of complex execution needs
        requires_high_cognitive_load = any(token in normalized_prompt for token in self.complexity_indicators)
        
        # Condition 2: Evaluate raw payload bulk input weight (e.g. prompts longer than 600 characters)
        is_heavy_payload = prompt_length > 600

        if requires_high_cognitive_load or is_heavy_payload:
            logger.info(f"[FinOps] [Route Approved] -> UPSTREAM CLOUD INFRASTRUCTURE ({self.cloud_model}) chosen. Reason: High Complexity / Weight.")
            return {
                "execution_tier": "cloud",
                "target_model": self.cloud_model,
                "token_cost_optimized": False
            }

        logger.info(f"[FinOps] [Route Approved] -> INTERNAL EDGE RUNTIME ({self.local_model}) chosen. Reason: Lightweight Operational Query.")
        return {
            "execution_tier": "local_edge",
            "target_model": self.local_model,
            "token_cost_optimized": True
        }
