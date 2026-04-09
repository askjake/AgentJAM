#!/usr/bin/env python3
"""
AgentJAM Main Entry Point
Handles CLI interface and agent orchestration
"""

import argparse
import sys
import json
from pathlib import Path
from agentjam.core.agent import Agent
from agentjam.models.model_selector import ModelSelector
from agentjam.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main CLI entry point for AgentJAM"""
    parser = argparse.ArgumentParser(
        description="AgentJAM - Intelligent Multi-Model AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard query (auto-selects model)
  python -m agentjam.main "Analyze this error log"
  
  # Explicit reasoning mode (uses Opus)
  python -m agentjam.main --reasoning "Design a distributed caching strategy"
  
  # Fast mode (uses Haiku)
  python -m agentjam.main --fast "Is the API endpoint healthy?"
  
  # Custom config
  python -m agentjam.main --config myconfig.json "Your query"
        """
    )
    
    parser.add_argument("query", help="The task or question for the agent")
    parser.add_argument(
        "--reasoning",
        action="store_true",
        help="Enable deep reasoning mode (uses Claude Opus 4.6)"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode for simple queries (uses Claude Haiku 4.5)"
    )
    parser.add_argument(
        "--model",
        choices=["opus", "sonnet", "haiku"],
        help="Explicitly specify model to use"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/agent_config.json"),
        help="Path to agent configuration file"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum tokens for response"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output response as JSON"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with CLI args
    if args.max_tokens:
        config["max_tokens"] = args.max_tokens
    
    # Determine model selection mode
    model_mode = None
    if args.reasoning:
        model_mode = "reasoning"
        logger.info("🧠 Reasoning mode activated - Using Claude Opus 4.6")
    elif args.fast:
        model_mode = "fast"
        logger.info("⚡ Fast mode activated - Using Claude Haiku 4.5")
    elif args.model:
        model_mode = args.model
        logger.info(f"🎯 Explicit model selected: {args.model}")
    
    # Initialize agent
    try:
        agent = Agent(config=config, verbose=args.verbose)
        
        # Execute query
        result = agent.execute(
            query=args.query,
            model_mode=model_mode
        )
        
        # Output result
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*80)
            print("AGENT RESPONSE")
            print("="*80)
            print(f"\nModel Used: {result.get('model_used', 'unknown')}")
            print(f"Tokens Used: {result.get('tokens_used', 'N/A')}")
            print(f"\nResponse:\n{result.get('content', 'No response')}")
            print("\n" + "="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Agent execution failed: {e}", exc_info=args.verbose)
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


def load_config(config_path: Path) -> dict:
    """Load agent configuration from file"""
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    
    # Default configuration
    return {
        "default_model": "sonnet",
        "reasoning_model": "opus",
        "fast_model": "haiku",
        "max_tokens": 800,
        "reasoning_max_tokens": 2000,
        "auto_routing": True,
        "complexity_threshold": 0.7
    }


if __name__ == "__main__":
    sys.exit(main())
