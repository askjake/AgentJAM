"""
Model Selector - Sonnet is DEFAULT, Opus for reasoning

Routing Priority:
1. Check for Opus keywords (design, architecture) → Opus
2. Check for Sonnet keywords (analyze, review) → Sonnet  
3. Check for Haiku pattern (is/are + short) → Haiku
4. Default → Sonnet
"""

import re
from typing import Dict, Any, Optional
from agentjam.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelSelector:
    """Model selection with Sonnet as the default workhorse"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize ModelSelector with config"""
        self.config = config
        self.auto_routing = config.get("auto_routing", True)
        
        # Load ARNs from config
        model_arns = config.get("model_arns", {})
        
        self.MODELS = {
            "opus": {
                "name": "Claude Opus 4.6",
                "arn": model_arns.get("opus", ""),
                "use_case": "Complex reasoning, design, architecture"
            },
            "sonnet": {
                "name": "Claude Sonnet 4.6",
                "arn": model_arns.get("sonnet", ""),
                "use_case": "DEFAULT - Standard work, analysis, review"
            },
            "haiku": {
                "name": "Claude Haiku 4.5",
                "arn": model_arns.get("haiku", ""),
                "use_case": "Trivial status checks only"
            }
        }
        
        logger.info(f"✓ ModelSelector: Sonnet (default), Opus (reasoning), Haiku (fast)")
    
    # Tier 1: OPUS keywords (highest complexity)
    OPUS_KEYWORDS = [
        "design", "architect", "strategy", "strategize",
        "propose solution", "recommend approach", "evaluate options",
        "multi-step reasoning", "complex analysis"
    ]
    
    # Tier 2: SONNET keywords (standard complexity - THE DEFAULT)
    SONNET_KEYWORDS = [
        "analyze", "review", "troubleshoot", "investigate", "debug",
        "explain", "describe", "summarize", "optimize", "refactor",
        "compare", "identify", "find", "locate", "fix", "check if"
    ]
    
    # Tier 3: HAIKU patterns (trivial queries only)
    HAIKU_PATTERNS = [
        r"^is .{1,30}\?$",  # "is X?" (short)
        r"^are .{1,30}\?$",  # "are X?" (short)
        r"^check (status|if) .{1,30}$",  # "check status" / "check if"
        r"^(status|list|show|get) .{1,30}$"  # "status of X", "list X"
    ]
    
    def select_model(self, query: str, mode: Optional[str] = None) -> Dict[str, str]:
        """Select model with Sonnet as default"""
        
        # Explicit modes ALWAYS override
        if mode == "reasoning":
            logger.info("🧠 --reasoning → Opus")
            return self._get_model("opus")
        elif mode == "fast":
            logger.info("⚡ --fast → Haiku")
            return self._get_model("haiku")
        elif mode in self.MODELS:
            logger.info(f"🎯 --model {mode}")
            return self._get_model(mode)
        
        # Auto-routing
        if self.auto_routing:
            model = self._auto_route(query)
            return self._get_model(model)
        
        # Fallback
        return self._get_model("sonnet")
    
    def _auto_route(self, query: str) -> str:
        """
        Auto-route based on keyword priority
        
        Order matters! Check high-value keywords first.
        """
        query_lower = query.lower().strip()
        
        # Priority 1: Opus keywords (design, architecture)
        for keyword in self.OPUS_KEYWORDS:
            if keyword in query_lower:
                logger.info(f"🧠 Opus keyword '{keyword}' → Opus")
                return "opus"
        
        # Priority 2: Sonnet keywords (analyze, review, troubleshoot)
        for keyword in self.SONNET_KEYWORDS:
            if keyword in query_lower:
                logger.info(f"📝 Sonnet keyword '{keyword}' → Sonnet")
                return "sonnet"
        
        # Priority 3: Haiku patterns (simple status checks)
        for pattern in self.HAIKU_PATTERNS:
            if re.match(pattern, query_lower, re.IGNORECASE):
                logger.info(f"⚡ Haiku pattern matched → Haiku")
                return "haiku"
        
        # Priority 4: Default to Sonnet
        logger.info(f"📝 No keywords matched → Default (Sonnet)")
        return "sonnet"
    
    def _get_model(self, model_key: str) -> Dict[str, str]:
        """Get model info by key"""
        if model_key not in self.MODELS:
            logger.warning(f"Unknown model '{model_key}', using sonnet")
            model_key = "sonnet"
        
        return {
            "name": self.MODELS[model_key]["name"],
            "arn": self.MODELS[model_key]["arn"]
        }
