"""
Custom Tools API Endpoints
"""
import os
import shutil
import time
import importlib.util
from datetime import datetime
from flask import jsonify, request


def parse_tool_file(file_path):
    """Parse a tool file and extract metadata"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract docstring
        docstring = ''
        if '"""' in content:
            parts = content.split('"""')
            if len(parts) >= 3:
                docstring = parts[1].strip()
        
        # Extract function names
        functions = []
        for line in content.split('\n'):
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                functions.append(func_name)
        
        filename = os.path.basename(file_path)
        tool_name = filename.replace('.py', '')
        
        from intelligent_backend import TOOL_DEFINITIONS
        
        return {
            'name': tool_name,
            'path': file_path,
            'description': docstring,
            'functions': functions,
            'active': tool_name in TOOL_DEFINITIONS,
            'size': os.path.getsize(file_path),
            'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        }
    except Exception as e:
        return {
            'name': 'unknown',
            'error': str(e)
        }
