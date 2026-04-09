"""
AgentJAM Core Agent
Main orchestration logic with dynamic model selection
"""

import os
import requests
from typing import Dict, Any, Optional
from agentjam.models.model_selector import ModelSelector
from agentjam.utils.logger import setup_logger

logger = setup_logger(__name__)


class Agent:
    """
    Main Agent class with dynamic model selection based on task complexity
    and explicit reasoning mode support.
    """
    
    def __init__(self, config: Dict[str, Any], verbose: bool = False):
        """
        Initialize the Agent
        
        Args:
            config: Agent configuration dictionary
            verbose: Enable verbose logging
        """
        self.config = config
        self.verbose = verbose
        
        # Initialize model selector
        self.model_selector = ModelSelector(config)
        
        # Get Coverity Assist credentials
        self.coverity_url = os.environ.get(
            "COVERITY_ASSIST_URL",
            "http://coverity-assist.dishtv.technology/chat"
        )
        self.coverity_token = os.environ.get("COVERITY_ASSIST_TOKEN")
        
        if not self.coverity_token:
            raise ValueError("COVERITY_ASSIST_TOKEN environment variable not set")
        
        logger.info(f"🤖 Agent initialized - Coverity URL: {self.coverity_url}")
    
    def execute(
        self,
        query: str,
        model_mode: Optional[str] = None,
        system_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute agent query with appropriate model selection
        
        Args:
            query: User query or task
            model_mode: Override model selection ('reasoning', 'fast', 'opus', 'sonnet', 'haiku')
            system_context: Optional system context/instructions
        
        Returns:
            Dict with 'content', 'model_used', 'tokens_used', etc.
        """
        # Select appropriate model
        model_info = self.model_selector.select_model(
            query=query,
            mode=model_mode
        )
        
        logger.info(
            f"📊 Selected Model: {model_info['name']} "
            f"(ARN: {model_info['arn']})"
        )
        
        # Determine max tokens based on model and config
        if model_mode == "reasoning":
            max_tokens = self.config.get("reasoning_max_tokens", 2000)
        else:
            max_tokens = self.config.get("max_tokens", 800)
        
        # Build request payload
        payload = {
            "messages": [{"role": "user", "content": query}],
            "max_tokens": max_tokens,
            "inference_profile_arn": model_info["arn"]
        }
        
        if system_context:
            payload["system"] = system_context
        
        # Execute request
        try:
            response = requests.post(
                self.coverity_url,
                headers={
                    "Authorization": f"Bearer {self.coverity_token}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content from various response formats
            content = (
                result.get("content") or
                result.get("response") or
                result.get("text") or
                str(result)
            )
            
            return {
                "content": content,
                "model_used": model_info["name"],
                "model_arn": model_info["arn"],
                "tokens_used": result.get("usage", {}).get("total_tokens", "N/A"),
                "success": True
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {e}")
            return {
                "content": f"Error: Failed to communicate with Coverity Assist - {e}",
                "model_used": model_info["name"],
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}", exc_info=True)
            return {
                "content": f"Error: {e}",
                "model_used": model_info["name"],
                "success": False,
                "error": str(e)
            }
