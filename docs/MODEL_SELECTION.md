# Model Selection Guide

## Overview

AgentJAM uses intelligent routing to select the optimal Claude model for each task, balancing quality, speed, and cost.

## Available Models

### Claude Opus 4.6 (Advanced)

**Best For**:
- Complex system design and architecture
- Root cause analysis of multi-component failures
- Novel problem-solving without precedent
- Critical decision-making with high stakes
- Deep code review and optimization
- Strategic planning and recommendations

**Characteristics**:
- Highest reasoning capability
- Best at handling ambiguity
- Excellent at breaking down complex problems
- Slower response time (5-15 seconds)
- 3x cost of Sonnet

**Example Queries**:
```bash
# Explicitly trigger Opus
python -m agentjam.main --reasoning "Design a fault-tolerant microservices architecture"

# Auto-triggered by complexity
python -m agentjam.main "Investigate why our distributed cache is causing race conditions"
```

### Claude Sonnet 4.6 (Default)

**Best For**:
- Standard code analysis and review
- Log file analysis and troubleshooting
- Documentation generation
- General Q&A about systems
- Workflow automation
- Most production use cases

**Characteristics**:
- Balanced speed and quality
- Cost-effective for high volume
- Excellent at structured outputs (JSON, CSV)
- Medium response time (2-5 seconds)
- Baseline cost (1x)

**Example Queries**:
```bash
# Default behavior (no flag needed)
python -m agentjam.main "Analyze this error log and suggest fixes"

# Explicit selection
python -m agentjam.main --model sonnet "Review this Python function"
```

### Claude Haiku 4.5 (Fast)

**Best For**:
- Simple validations ("Is X running?")
- Boolean questions
- Quick status checks
- Simple transformations
- High-frequency polling
- Rapid iteration checks

**Characteristics**:
- Fastest response time (0.5-2 seconds)
- Lowest cost (0.1x Sonnet)
- Good for yes/no answers
- Limited reasoning depth
- Excellent for simple, well-defined tasks

**Example Queries**:
```bash
# Explicitly trigger Haiku
python -m agentjam.main --fast "Is the API endpoint healthy?"

# Auto-triggered by simplicity
python -m agentjam.main "List all running pods"
```

## Model Selection Logic

### Explicit Mode Selection

**Priority 1**: User-specified flags always override auto-routing

```bash
# Force Opus (reasoning mode)
--reasoning

# Force Haiku (fast mode)
--fast

# Force specific model
--model opus|sonnet|haiku
```

### Auto-Routing (Default)

When no explicit mode is specified, AgentJAM assesses query complexity using multiple heuristics:

#### Complexity Scoring Formula

```python
complexity_score = (
    complex_keywords * 0.4 +      # "design", "analyze", "investigate"
    (1 - simple_keywords) * 0.2 + # absence of "is", "check", "list"
    length_factor * 0.2 +         # query length / 500 chars
    question_count * 0.1 +        # number of questions
    code_present * 0.1            # contains code/technical syntax
)
```

#### Routing Thresholds

| Score Range | Model | Rationale |
|-------------|-------|-----------|
| 0.0 - 0.3 | Haiku | Simple query, fast response sufficient |
| 0.3 - 0.7 | Sonnet | Standard complexity, balanced approach |
| 0.7 - 1.0 | Opus | High complexity, deep reasoning required |

### Complexity Indicators

#### High Complexity (Opus) - Score ≥ 0.7

**Keywords**:
- design, architecture, strategy, plan
- investigate, root cause, debug deeply
- analyze thoroughly, optimize, refactor
- evaluate, compare, recommend, propose
- solution, fault-tolerant, scalable

**Query Characteristics**:
- Multiple interdependent questions
- Requires synthesis of concepts
- Involves trade-off analysis
- No clear precedent or template
- Long-form explanation needed

**Examples**:
```
✅ "Design a disaster recovery strategy for our multi-region deployment"
✅ "Investigate why our Lambda functions timeout intermittently"
✅ "Compare service mesh solutions for our architecture"
✅ "Propose optimization strategy for database query performance"
```

#### Medium Complexity (Sonnet) - Score 0.3-0.7

**Keywords**:
- analyze, review, troubleshoot
- explain, describe, summarize
- configure, setup, implement
- identify, find, locate

**Query Characteristics**:
- Single clear question or task
- Standard troubleshooting workflow
- Well-defined scope
- Moderate length response needed

**Examples**:
```
✅ "Analyze this error log and identify the issue"
✅ "Review this Kubernetes config for best practices"
✅ "Explain how to configure AWS Lambda timeouts"
✅ "Summarize the recent changes in deployment"
```

#### Low Complexity (Haiku) - Score ≤ 0.3

**Keywords**:
- is, are, check, status
- list, show, display, get, view
- what is, tell me, quick
- yes/no questions

**Query Characteristics**:
- Simple factual question
- Boolean answer possible
- Quick status check
- No analysis required

**Examples**:
```
✅ "Is the API endpoint healthy?"
✅ "List all running pods in namespace"
✅ "Check if service is deployed"
✅ "What is the current version?"
```

## Cost Optimization Strategies

### Understand Model Costs

| Model | Cost Multiplier | When to Use |
|-------|----------------|-------------|
| Haiku | 0.1x | 90% of simple queries |
| Sonnet | 1.0x | 80% of standard work |
| Opus | 3.0x | <10% of complex tasks |

### Best Practices

1. **Use --fast for Validations**
   ```bash
   # Bad: Using default for simple check
   python -m agentjam.main "Is pod running?"
   
   # Good: Explicit fast mode
   python -m agentjam.main --fast "Is pod running?"
   ```

2. **Trust Auto-Routing for Standard Queries**
   ```bash
   # Let complexity scoring decide
   python -m agentjam.main "Analyze this log file"
   ```

3. **Reserve --reasoning for Critical Decisions**
   ```bash
   # Only when deep thinking is required
   python -m agentjam.main --reasoning "Design our DR strategy"
   ```

4. **Set Appropriate max_tokens**
   ```bash
   # Don't pay for unused tokens
   python -m agentjam.main --max-tokens 400 "Quick status check"
   ```

### Cost Estimation

**Example Daily Usage**:
```
100 Haiku queries  = 10 Sonnet-equivalent
50 Sonnet queries  = 50 Sonnet-equivalent
5 Opus queries     = 15 Sonnet-equivalent
                   ─────────────────────
Total              = 75 Sonnet-equivalent
```

**Optimization Opportunity**:
- If 20 Sonnet queries could be Haiku: Save 18 Sonnet-equivalent
- New total: 57 Sonnet-equivalent (24% cost reduction)

## Tuning Complexity Threshold

### Adjust in Config

```json
{
  "complexity_threshold": 0.7,  // Default: Opus at ≥0.7
  "auto_routing": true
}
```

### Threshold Tuning Guidelines

| Threshold | Effect | Use Case |
|-----------|--------|----------|
| 0.5 | More Opus usage | Quality-critical applications |
| 0.7 | Balanced (default) | Most production systems |
| 0.9 | Minimal Opus usage | Cost-sensitive environments |

### Disable Auto-Routing

```json
{
  "auto_routing": false,
  "default_model": "sonnet"
}
```

Forces all queries to default model unless explicit flag used.

## Model Selection Decision Tree

```
                    User Query
                        ↓
              ┌─────────┴─────────┐
              │ Explicit Flag?    │
              └─────────┬─────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   --reasoning       --fast          --model X
        │               │               │
        ↓               ↓               ↓
      OPUS            HAIKU        [Selected]
        
        │ (None)
        ↓
   Auto-Routing
   Enabled?
        │
    ┌───┴───┐
   No      Yes
    │       │
    ↓       ↓
  Default  Assess
  SONNET   Complexity
            │
       ┌────┼────┐
       │    │    │
     High  Mid  Low
     ≥0.7  Mid  ≤0.3
       │    │    │
       ↓    ↓    ↓
     OPUS SONNET HAIKU
```

## Testing Model Selection

### Verify Routing Behavior

```bash
# Test high complexity auto-route
python -m agentjam.main --verbose "Design a caching strategy" | grep "Model Used"
# Expected: Opus

# Test medium complexity
python -m agentjam.main --verbose "Analyze this error" | grep "Model Used"
# Expected: Sonnet

# Test low complexity
python -m agentjam.main --verbose "Is service running?" | grep "Model Used"
# Expected: Haiku

# Force reasoning mode
python -m agentjam.main --reasoning --verbose "Simple question" | grep "Model Used"
# Expected: Opus (overrides complexity)
```

### Complexity Score Debugging

```bash
# Enable verbose logging to see scores
python -m agentjam.main --verbose "Your query here"
# Output includes: "Complexity score: 0.75"
```

## When to Override Auto-Routing

### Use --reasoning When:
- System design or architecture decisions
- Debugging novel or rare issues
- Critical production incidents
- Complex trade-off analysis required
- No precedent or template available

### Use --fast When:
- Polling for status in loops
- Simple validations in pipelines
- Boolean checks (yes/no answers)
- Quick information lookups
- High-frequency monitoring queries

### Use --model sonnet When:
- Standard troubleshooting
- Code reviews
- Log analysis
- Documentation tasks
- Most day-to-day operations

## Model Capabilities Comparison

| Capability | Haiku | Sonnet | Opus |
|------------|-------|--------|------|
| Code Analysis | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| System Design | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Debugging | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Status Checks | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Cost Efficiency | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Reasoning Depth | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Summary

**Quick Reference**:
- **Simple query** → Haiku (or let auto-route)
- **Standard work** → Sonnet (default)
- **Complex analysis** → Opus (use --reasoning)
- **Unsure?** → Let auto-routing decide
- **Cost-sensitive?** → Lower complexity_threshold
- **Quality-critical?** → Raise complexity_threshold or use --reasoning
