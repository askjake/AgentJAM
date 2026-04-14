#!/usr/bin/env python3
"""
Implicit Tool Call Parser - Fallback for LLMs that don't support function calling

This module detects markdown code blocks in LLM responses and converts them to
structured tool calls. This allows the agentic loop to execute code even when
the LLM doesn't return explicit tool_calls.

Author: Enhancement based on diagnostic report chat_1776112389566_r3dmnalqg
Date: 2026-04-13
"""

import re
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def detect_implicit_tool_calls(response_text: str, chat_id: str = None) -> List[Dict[str, Any]]:
    """
    Parse markdown code blocks as implicit tool calls
    
    Detects:
    - ```bash ... ``` → agent_run_shell
    - ```sh ... ``` → agent_run_shell
    - ```shell ... ``` → agent_run_shell
    - ```python ... ``` → agent_run_python
    
    Args:
        response_text: LLM response text
        chat_id: Chat ID for Python execution context
    
    Returns:
        List of tool_call dicts compatible with agentic loop
    """
    if not response_text:
        return []
    
    tool_calls = []

    # First, detect Coverity Assist XML-style tool calls
    # Pattern: <tool_call>{"name": "agent_run_shell", "arguments": {"command": "..."}}</tool_call>
    xml_tool_pattern = r'<tool_call>\s*(\{[^}]+\})\s*</tool_call>'
    
    for match in re.finditer(xml_tool_pattern, response_text, re.DOTALL):
        try:
            tool_data = json.loads(match.group(1))
            tool_name = tool_data.get('name', '')
            tool_args = tool_data.get('arguments', {})
            
            if tool_name:
                tool_calls.append({
                    'id': f'xml_tool_{len(tool_calls)}',
                    'name': tool_name,
                    'function': {
                        'name': tool_name,
                        'arguments': json.dumps(tool_args)
                    },
                    'arguments': tool_args,
                    'implicit': True,
                    'source': 'xml_parser'
                })
                
                logger.info(f"📝 Detected XML tool call: {tool_name}")
        except Exception as e:
            logger.warning(f"Failed to parse XML tool call: {e}")
    

    
    # Pattern for shell commands
    shell_patterns = [
        r'```bash\n(.+?)\n```',
        r'```sh\n(.+?)\n```',
        r'```shell\n(.+?)\n```',
        r'```\n([^`]*(?:ls|cd|cp|mv|rm|mkdir|cat|grep|find|ps|kill|lsusb|hackrf|apt|yum)\b[^`]*)\n```'  # Generic shell commands
    ]
    
    # Pattern for Python code
    python_pattern = r'```python\n(.+?)\n```'
    
    # Extract shell commands
    for pattern in shell_patterns:
        for match in re.finditer(pattern, response_text, re.DOTALL | re.IGNORECASE):
            command = match.group(1).strip()
            
            # Skip if empty or just comments
            if not command or command.startswith('#'):
                continue
            
            # Skip if it's actually Python code misidentified
            if 'import ' in command or 'def ' in command:
                continue
            
            tool_calls.append({
                'id': f'implicit_shell_{len(tool_calls)}',
                'name': 'agent_run_shell',
                'function': {
                    'name': 'agent_run_shell',
                    'arguments': json.dumps({'command': command})
                },
                'arguments': {'command': command},
                'implicit': True,
                'source': 'markdown_parser'
            })
            
            logger.info(f"📝 Detected implicit shell command: {command[:80]}...")
    
    # Extract Python code
    for match in re.finditer(python_pattern, response_text, re.DOTALL):
        code = match.group(1).strip()
        
        if not code:
            continue
        
        # Use chat_id if provided, otherwise generate a temporary one
        arguments = {
            'code': code,
            'chat_id': chat_id or 'implicit_exec'
        }
        
        tool_calls.append({
            'id': f'implicit_python_{len(tool_calls)}',
            'name': 'agent_run_python',
            'function': {
                'name': 'agent_run_python',
                'arguments': json.dumps(arguments)
            },
            'arguments': arguments,
            'implicit': True,
            'source': 'markdown_parser'
        })
        
        logger.info(f"📝 Detected implicit Python code: {len(code)} chars")
    
    if tool_calls:
        logger.info(f"✨ Parsed {len(tool_calls)} implicit tool calls from response")
    
    return tool_calls


def should_enable_fallback(llm_response: Dict[str, Any]) -> bool:
    """
    Determine if fallback parser should be used
    
    Use fallback if:
    - No explicit tool_calls in response
    - Response contains code blocks
    - Not an error response
    
    Args:
        llm_response: Response from LLM
    
    Returns:
        True if fallback should be used
    """
    # Don't use fallback if explicit tool calls exist
    if llm_response.get('tool_calls'):
        return False
    
    # Don't use fallback for error responses
    if 'error' in llm_response.get('response', '').lower():
        return False
    
    response_text = llm_response.get('response', '')
    
    # Check if response contains code blocks
    has_code_blocks = '```' in response_text
    
    return has_code_blocks


def enhance_response_with_implicit_tools(
    llm_response: Dict[str, Any],
    chat_id: str = None,
    auto_execute: bool = True
) -> Dict[str, Any]:
    """
    Enhance LLM response with implicit tool calls
    
    If the response contains code blocks but no explicit tool_calls,
    parse the code blocks and add them as tool_calls.
    
    Args:
        llm_response: Original LLM response
        chat_id: Chat ID for context
        auto_execute: If True, add tool_calls (triggers execution)
                     If False, just add metadata
    
    Returns:
        Enhanced response dict
    """
    if not should_enable_fallback(llm_response):
        return llm_response
    
    response_text = llm_response.get('response', '')
    implicit_tools = detect_implicit_tool_calls(response_text, chat_id)
    
    if not implicit_tools:
        return llm_response
    
    if auto_execute:
        # Add implicit tool calls to trigger execution
        llm_response['tool_calls'] = implicit_tools
        llm_response['implicit_execution'] = True
        logger.info(f"🔄 Enabled implicit execution for {len(implicit_tools)} tools")
    else:
        # Just add metadata, don't execute
        llm_response['detected_code_blocks'] = len(implicit_tools)
        llm_response['implicit_tools_available'] = implicit_tools
        logger.info(f"📋 Detected {len(implicit_tools)} tools (execution disabled)")
    
    return llm_response


# Convenience function for backward compatibility
parse_code_blocks = detect_implicit_tool_calls


if __name__ == '__main__':
    # Test the parser
    logging.basicConfig(level=logging.INFO)
    
    test_response = """Let me check for the HackRF device:

```bash
lsusb | grep -i 'great scott'
```

And get device info:

```bash
hackrf_info
```

Now let's analyze the signal:

```python
import subprocess
result = subprocess.run(['hackrf_transfer', '-r', '/tmp/capture.bin'], 
                       capture_output=True)
print(result.stdout)
```
"""
    
    tool_calls = detect_implicit_tool_calls(test_response, 'test_chat')
    
    print(f"\nParsed {len(tool_calls)} tool calls:")
    for i, call in enumerate(tool_calls, 1):
        print(f"\n{i}. {call['name']}")
        print(f"   Arguments: {call['arguments']}")
    
    print("\n✅ Parser test complete!")
