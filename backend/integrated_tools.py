"""
Integrated tool implementations for intelligent_backend.py
Simplified wrappers around app/tools/ modules
"""

import os
import sys
import asyncio
import subprocess
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# ============================================================================
# CLUSTER INSPECT
# ============================================================================

def cluster_inspect_sync(task: str) -> str:
    """
    Synchronous wrapper for cluster_inspect tool
    Runs kubectl commands based on task description
    """
    task_lower = task.lower().strip()
    
    # Map common tasks to kubectl commands
    if 'sentry pods' in task_lower or 'pods in sentry' in task_lower:
        cmd = ['kubectl', 'get', 'pods', '-n', 'sentry']
    elif 'list sentry' in task_lower and 'claim' in task_lower:
        cmd = ['kubectl', 'get', 'pvc', '-n', 'sentry']
    elif 'list all pods' in task_lower:
        cmd = ['kubectl', 'get', 'pods', '--all-namespaces']
    elif 'list namespaces' in task_lower:
        cmd = ['kubectl', 'get', 'namespaces']
    elif 'list nodes' in task_lower:
        cmd = ['kubectl', 'get', 'nodes']
    elif 'list deployments' in task_lower:
        cmd = ['kubectl', 'get', 'deployments', '--all-namespaces']
    elif 'list services' in task_lower:
        cmd = ['kubectl', 'get', 'services', '--all-namespaces']
    elif 'describe pod' in task_lower:
        # Extract pod name and namespace
        parts = task.split()
        pod_name = parts[parts.index('pod') + 1] if 'pod' in parts else ''
        namespace = parts[parts.index('namespace') + 1] if 'namespace' in parts else 'default'
        cmd = ['kubectl', 'describe', 'pod', pod_name, '-n', namespace]
    elif 'logs from' in task_lower:
        parts = task.split()
        pod_name = parts[parts.index('from') + 1] if 'from' in parts else ''
        namespace = parts[parts.index('namespace') + 1] if 'namespace' in parts else 'default'
        cmd = ['kubectl', 'logs', pod_name, '-n', namespace, '--tail=100']
    else:
        return f"❌ Unsupported cluster inspect task: {task}"
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"❌ Command failed: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "❌ Command timed out (30s)"
    except FileNotFoundError:
        return """❌ kubectl not found on this system

This AgentPi003 node does not have kubectl installed.

To enable cluster inspection:
1. Install kubectl: sudo apt-get install kubectl
2. Configure kubeconfig: kubectl config view
3. Or use agent_run_shell with ssh to a node that has kubectl

Alternative: Use shell_execution to SSH to ops host:
  ssh ops-host 'kubectl get namespaces'
"""
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============================================================================
# PUBLIC WEB SEARCH
# ============================================================================

def public_web_search_sync(query: str, max_results: int = 6) -> str:
    """
    Synchronous wrapper for public web search
    Uses DuckDuckGo as search backend
    """
    try:
        import requests
        from urllib.parse import quote_plus
        
        # DuckDuckGo instant answer API
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant results
            results = []
            
            # Abstract (main answer)
            if data.get('AbstractText'):
                results.append(f"**Answer:** {data['AbstractText']}")
                if data.get('AbstractURL'):
                    results.append(f"Source: {data['AbstractURL']}")
            
            # Related topics
            if data.get('RelatedTopics'):
                results.append("\n**Related Topics:**")
                for i, topic in enumerate(data['RelatedTopics'][:max_results], 1):
                    if isinstance(topic, dict) and 'Text' in topic:
                        results.append(f"{i}. {topic['Text']}")
                        if 'FirstURL' in topic:
                            results.append(f"   {topic['FirstURL']}")
            
            if results:
                return "\n".join(results)
            else:
                return f"No instant results found for: {query}\n\nNote: This is a simplified search. For full results, use a web browser."
        else:
            return f"❌ Search failed: HTTP {response.status_code}"
            
    except ImportError:
        return "❌ requests library not available"
    except Exception as e:
        return f"❌ Search error: {str(e)}"


# ============================================================================
# INTERNAL SEARCH
# ============================================================================

def internal_search_sync(query: str, top_k: int = 5) -> str:
    """
    Synchronous wrapper for internal search
    Searches Confluence, JIRA, GitLab
    """
    # Check for environment configuration
    confluence_url = os.getenv('CONFLUENCE_URL')
    gitlab_url = os.getenv('GITLAB_URL')
    jira_url = os.getenv('JIRA_URL')
    
    available_sources = []
    if confluence_url:
        available_sources.append('Confluence')
    if gitlab_url:
        available_sources.append('GitLab')
    if jira_url:
        available_sources.append('JIRA')
    
    if not available_sources:
        return f"""❌ Internal search not configured

To enable internal search, set environment variables:
- CONFLUENCE_URL
- CONFLUENCE_TOKEN
- GITLAB_URL
- GITLAB_TOKEN
- JIRA_URL
- JIRA_TOKEN

Query: {query}
Top K: {top_k}
"""
    
    # If configured, attempt async search
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Already in async context, can't run nested
            return f"⚠️ Internal search requires async context (sources: {', '.join(available_sources)})"
        else:
            # Run async search
            from app.tools.internal_search import internal_search
            result = loop.run_until_complete(internal_search(query, top_k))
            return result
    except ImportError:
        return f"⚠️ Internal search module not available (query: {query})"
    except Exception as e:
        return f"❌ Internal search error: {str(e)}"


# ============================================================================
# TOOL EXECUTOR
# ============================================================================

def execute_integrated_tool(tool_name: str, params: Dict[str, Any]) -> str:
    """
    Execute integrated tools with proper error handling
    """
    try:
        if tool_name == 'cluster_inspect':
            task = params.get('task', '')
            return cluster_inspect_sync(task)
        
        elif tool_name == 'public_web_search':
            query = params.get('query', '')
            max_results = params.get('max_results', 6)
            return public_web_search_sync(query, max_results)
        
        elif tool_name == 'internal_search':
            query = params.get('query', '')
            top_k = params.get('top_k', 5)
            return internal_search_sync(query, top_k)
        
        else:
            return f"❌ Unknown tool: {tool_name}"
            
    except Exception as e:
        logger.error(f"Tool execution failed: {tool_name} - {e}")
        return f"❌ Tool execution error: {str(e)}"

