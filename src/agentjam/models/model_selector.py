"""
Model Selector - Dynamic model routing based on task complexity
"""

import re
from typing import Dict, Any, Optional
from agentjam.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelSelector:
    """
    Intelligent model selection based on query complexity and explicit modes
    """
    
    # Model ARN mappings (update these with actual ARNs)
    MODELS = {
        "opus": {
            "name": "Claude Opus 4.6",
            "arn": "arn:aws:bedrock:us-west-2:account:application-inference-profile/opus-46",
            "cost_multiplier": 3.0,
            "complexity": "high"
        },
        "sonnet": {
            "name": "Claude Sonnet 4.6",
            "arn": "arn:aws:bedrock:us-west-2:account:application-inference-profile/sonnet-46",
            "cost_multiplier": 1.0,
            "complexity": "medium"
        },
        "haiku": {
            "name": "Claude Haiku 4.5",
            "arn": "arn:aws:bedrock:us-west-2:account:application-inference-profile/haiku-45",
            "cost_multiplier": 0.1,
            "complexity": "low"
        }
    }
    
    # Keywords indicating high complexity / reasoning requirement
    COMPLEX_KEYWORDS = [
        "design", "architecture", "strategy", "plan", "analyze deeply",
        "investigate", "root cause", "debug", "optimize", "refactor",
        "compare", "evaluate", "recommend", "proposal", "solution"
    ]
    
    # Keywords indicating simple queries
    SIMPLE_KEYWORDS = [
        "is", "are", "check", "status", "list", "show", "get",
        "display", "view", "what is", "quick"
    ]
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ModelSelector
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.auto_routing = config.get("auto_routing", True)
        self.complexity_threshold = config.get("complexity_threshold", 0.7)
    
    def select_model(
        self,
        query: str,
        mode: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Select appropriate model based on query and mode
        
        Args:
            query: User query
            mode: Explicit mode ('reasoning', 'fast', or specific model name)
        
        Returns:
            Dict with 'name' and 'arn' of selected model
        """
        # Explicit mode overrides
        if mode == "reasoning":
            return self._get_model("opus")
        elif mode == "fast":
            return self._get_model("haiku")
        elif mode in self.MODELS:
            return self._get_model(mode)
        
        # Auto-routing based on complexity
        if self.auto_routing:
            complexity_score = self._assess_complexity(query)
            
            logger.debug(f"📊 Complexity score: {complexity_score:.2f}")
            
            if complexity_score >= self.complexity_threshold:
                logger.info("🧠 High complexity detected - routing to Opus")
                return self._get_model("opus")
            elif complexity_score <= 0.3:
                logger.info("⚡ Low complexity detected - routing to Haiku")
                return self._get_model("haiku")
        
        # Default to Sonnet
        logger.info("📝 Standard complexity - routing to Sonnet")
        return self._get_model(self.config.get("default_model", "sonnet"))
    
    def _get_model(self, model_key: str) -> Dict[str, str]:
        """Get model info by key"""
        if model_key not in self.MODELS:
            logger.warning(f"Unknown model '{model_key}', falling back to sonnet")
            model_key = "sonnet"
        
        return {
            "name": self.MODELS[model_key]["name"],
            "arn": self.MODELS[model_key]["arn"]
        }
    
    def _assess_complexity(self, query: str) -> float:
        """
        Assess query complexity using heuristics
        
        Returns:
            Float between 0.0 (simple) and 1.0 (complex)
        """
        query_lower = query.lower()
        
        # Simple query detection
        simple_score = sum(
            1 for keyword in self.SIMPLE_KEYWORDS
            if keyword in query_lower
        ) / len(self.SIMPLE_KEYWORDS)
        
        # Complex query detection
        complex_score = sum(
            1 for keyword in self.COMPLEX_KEYWORDS
            if keyword in query_lower
        ) / len(self.COMPLEX_KEYWORDS)
        
        # Length factor (longer queries tend to be more complex)
        length_score = min(len(query) / 500, 1.0)
        
        # Question complexity (multiple questions = more complex)
        question_marks = query.count("?")
        question_score = min(question_marks / 3, 1.0)
        
        # Code/technical content (presence of code = more complex)
        has_code = bool(re.search(r'```|{|}|\(.*\)|function|class|def ', query))
        code_score = 0.5 if has_code else 0.0
        
        # Weighted combination
        final_score = (
            complex_score * 0.4 +
            (1 - simple_score) * 0.2 +
            length_score * 0.2 +
            question_score * 0.1 +
            code_score * 0.1
        )
        
        return min(final_score, 1.0)
