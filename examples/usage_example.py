#!/usr/bin/env python3
"""
Example usage of AgentJAM
"""

import os
from agentjam.core.agent import Agent

# Setup environment
os.environ["COVERITY_ASSIST_URL"] = "http://coverity-assist.dishtv.technology/chat"
os.environ["COVERITY_ASSIST_TOKEN"] = "your-token-here"

# Load config
config = {
    "default_model": "sonnet",
    "reasoning_model": "opus",
    "fast_model": "haiku",
    "max_tokens": 800,
    "reasoning_max_tokens": 2000,
    "auto_routing": True,
    "complexity_threshold": 0.7
}

# Initialize agent
agent = Agent(config=config, verbose=True)

# Example 1: Simple query (will use Haiku or Sonnet)
result = agent.execute("What is the status of the API?")
print(f"Simple Query Result: {result['content']}")

# Example 2: Standard query (will use Sonnet)
result = agent.execute("Analyze this error log and suggest fixes")
print(f"Standard Query Result: {result['content']}")

# Example 3: Complex reasoning (will use Opus)
result = agent.execute(
    "Design a fault-tolerant microservices architecture for e-commerce",
    model_mode="reasoning"
)
print(f"Reasoning Result: {result['content']}")

# Example 4: Explicit model selection
result = agent.execute(
    "Quick validation check",
    model_mode="fast"
)
print(f"Fast Mode Result: {result['content']}")
