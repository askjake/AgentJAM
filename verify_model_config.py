#!/usr/bin/env python3
"""
Verify AgentJAM configuration and model selection logic
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from agentjam.models.model_selector import ModelSelector

# Load config
with open('config/agent_config.json') as f:
    config = json.load(f)

print("="*80)
print("AGENTJAM MODEL CONFIGURATION VERIFICATION")
print("="*80)
print()

# Initialize selector
selector = ModelSelector(config)

print("📋 Configuration:")
print(f"   Default Model: {config['default_model']}")
print(f"   Reasoning Model: {config['reasoning_model']}")
print(f"   Fast Model: {config['fast_model']}")
print(f"   Auto-Routing: {config['auto_routing']}")
print(f"   Complexity Threshold: {config['complexity_threshold']}")
print()

print("🎯 Model ARNs:")
for model_name, arn in config['model_arns'].items():
    print(f"   {model_name.capitalize()}: {arn}")
print()

print("="*80)
print("MODEL SELECTION TESTS")
print("="*80)
print()

# Test 1: Default (no mode, medium complexity)
test_queries = [
    ("Is the API healthy?", None, "haiku", "Simple query"),
    ("Analyze this error log", None, "sonnet", "Standard query (default)"),
    ("Design a disaster recovery strategy", None, "opus", "Complex query"),
    ("Quick check", "fast", "haiku", "Explicit --fast"),
    ("Any query", "reasoning", "opus", "Explicit --reasoning"),
    ("Something", "sonnet", "sonnet", "Explicit --model sonnet"),
]

passed = 0
failed = 0

for query, mode, expected_model, description in test_queries:
    result = selector.select_model(query, mode=mode)
    actual_model = "opus" if "opus" in result['arn'].lower() else                    "sonnet" if "sonnet" in result['arn'].lower() else                    "haiku" if "haiku" in result['arn'].lower() else "unknown"
    
    status = "✅" if actual_model == expected_model else "❌"
    
    if actual_model == expected_model:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} {description}")
    print(f"   Query: '{query}'")
    print(f"   Mode: {mode or 'auto'}")
    print(f"   Expected: {expected_model}")
    print(f"   Actual: {actual_model} ({result['name']})")
    print()

print("="*80)
print(f"RESULTS: {passed} passed, {failed} failed")
print("="*80)

if failed == 0:
    print()
    print("✅ ALL TESTS PASSED!")
    print()
    print("Model Selection Summary:")
    print("  • Default queries → Sonnet (balanced)")
    print("  • --reasoning flag → Opus (advanced)")
    print("  • --fast flag → Haiku (quick)")
    print("  • High complexity (auto) → Opus")
    print("  • Low complexity (auto) → Haiku")
    sys.exit(0)
else:
    print()
    print("❌ SOME TESTS FAILED")
    print("Check the configuration and model selector logic")
    sys.exit(1)
