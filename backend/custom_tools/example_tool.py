"""
Example custom tool that demonstrates the basic structure.
This tool takes a name and returns a greeting.
"""

from typing import Dict, Any

def example_tool(name: str = "World") -> Dict[str, Any]:
    """
    A simple example tool that creates a greeting.
    
    Args:
        name: The name to greet (default: "World")
    
    Returns:
        Dictionary with status, data, and message
    """
    try:
        greeting = f"Hello, {name}! Welcome to custom tools."
        
        return {
            "status": "success",
            "data": {
                "greeting": greeting,
                "name": name
            },
            "message": "Greeting created successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to create greeting"
        }
