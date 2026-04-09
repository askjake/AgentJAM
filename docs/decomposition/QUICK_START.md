# AUTO-DECOMPOSER QUICK START
## agentpi003@10.73.184.61

## Current Status
✅ DEPLOYED - Phase 1 (Monitoring Mode)
📍 Location: /home/agentpi003/dish-chat/backend/app/core/decomposition/

## Quick Test

```bash
cd /home/agentpi003/dish-chat/backend
python3 << EOF
from app.core.decomposition import RequestAnalyzer

analyzer = RequestAnalyzer()
analysis = analyzer.analyze("Play through 20 levels of this game")

print(f"Task Type: {analysis.task_type.value}")
print(f"Complexity: {analysis.complexity.value}")
print(f"Steps: {analysis.estimated_steps}")
EOF
```

## Module Structure

- **RequestAnalyzer** - Analyzes complexity and intent
- **IntelligentDecomposer** - Breaks down complex requests
- **SequentialOrchestrator** - Executes with dependencies
- **ResponseSynthesizer** - Assembles responses
- **AutoDecomposingAgent** - Main interface

## Task Types Detected

1. SIMPLE - Single-shot response
2. SEQUENTIAL - Must execute in order
3. INTERACTIVE - Requires iteration (games, challenges)
4. EXPLORATORY - Research/discovery
5. PARALLEL - Can execute concurrently
6. MULTI_PHASE - Distinct phases

## Complexity Levels

1. TRIVIAL (1) - Single call
2. SIMPLE (2) - Few steps
3. MODERATE (3) - Multiple steps
4. COMPLEX (4) - Many dependencies
5. VERY_COMPLEX (5) - Extensive orchestration

## Example Usage

```python
from app.core.decomposition import AutoDecomposingAgent

# Initialize (monitoring mode)
agent = AutoDecomposingAgent(enable_auto_decompose=False)

# Analyze without execution
result = agent.analyze_without_execution(user_message)

print(f"Should decompose: {result['should_decompose']}")
print(f"Task type: {result['analysis']['task_type']}")
print(f"Subtasks: {result['subtask_count']}")
```

## Rollback

```bash
cd /home/agentpi003/dish-chat/backend
rm -rf app/core/decomposition
tar -xzf /home/agentpi003/backups/decomposer_deploy_20260406_165100/backend_pre_decomposer.tar.gz
```

## Support Files

- DEPLOYMENT_REPORT.md - Full deployment details
- /home/agentpi003/backups/ - Backup location

## Next Phase

Phase 2: Integration with agent.py for request monitoring
