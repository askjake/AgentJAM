# AgentJAM Architecture

## Overview

AgentJAM is a multi-model AI agent framework designed for intelligent task routing between Claude Opus 4.6, Sonnet 4.6, and Haiku 4.5 models based on task complexity and explicit user preferences.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AgentJAM System                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              CLI Interface (__main__.py)                    │ │
│  │  • Argument Parsing                                         │ │
│  │  • Mode Selection (--reasoning, --fast, --model)            │ │
│  │  • Output Formatting (JSON, Text)                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           Core Agent (core/agent.py)                        │ │
│  │  • Request Orchestration                                    │ │
│  │  • Coverity Assist Integration                              │ │
│  │  • Error Handling & Logging                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │      Model Selector (models/model_selector.py)              │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │   Complexity Assessment Engine                        │  │ │
│  │  │  • Keyword Analysis                                   │  │ │
│  │  │  • Query Length Heuristics                            │  │ │
│  │  │  • Code Detection                                     │  │ │
│  │  │  • Multi-Question Detection                           │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                      ↓                                       │ │
│  │  ┌──────────────┬──────────────┬──────────────┐            │ │
│  │  │ Opus Route   │ Sonnet Route │ Haiku Route  │            │ │
│  │  │ (Complex)    │  (Standard)  │   (Simple)   │            │ │
│  │  │ Score ≥ 0.7  │ 0.3 < S < 0.7│  Score ≤ 0.3 │            │ │
│  │  └──────────────┴──────────────┴──────────────┘            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           Coverity Assist Gateway                           │ │
│  │  • HTTP/REST API Client                                     │ │
│  │  • Bearer Token Authentication                              │ │
│  │  • Model ARN Routing                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         AWS Bedrock (via Coverity Assist)                   │ │
│  │  ┌──────────────┬──────────────┬──────────────┐            │ │
│  │  │ Claude Opus  │Claude Sonnet │ Claude Haiku │            │ │
│  │  │     4.6      │     4.6      │     4.5      │            │ │
│  │  └──────────────┴──────────────┴──────────────┘            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. CLI Interface (`__main__.py`)

**Purpose**: Entry point for user interactions

**Responsibilities**:
- Parse command-line arguments
- Load configuration from JSON files
- Override config with CLI flags
- Format and display results
- Handle exit codes

**Key Features**:
- `--reasoning`: Force Opus model for deep thinking
- `--fast`: Force Haiku model for quick responses
- `--model <name>`: Explicitly select model
- `--json`: Output structured JSON
- `--verbose`: Enable detailed logging

### 2. Core Agent (`core/agent.py`)

**Purpose**: Orchestrate agent operations

**Responsibilities**:
- Initialize Coverity Assist client
- Validate environment (tokens, URLs)
- Call Model Selector for routing
- Execute HTTP requests to Coverity Assist
- Parse and normalize responses
- Error recovery and logging

**Key Methods**:
- `execute(query, model_mode, system_context)`: Main execution loop
- `_build_request()`: Construct Coverity payload
- `_parse_response()`: Extract content from various formats

### 3. Model Selector (`models/model_selector.py`)

**Purpose**: Intelligent model routing based on query characteristics

**Complexity Scoring Algorithm**:

```python
complexity_score = (
    complex_keywords_score * 0.4 +  # Words like "design", "analyze"
    (1 - simple_keywords_score) * 0.2 +  # Absence of "is", "check"
    length_score * 0.2 +  # Query length / 500 chars
    question_score * 0.1 +  # Number of question marks
    code_presence * 0.1  # Contains code snippets
)
```

**Routing Decision Tree**:

```
┌─────────────────────────────┐
│  User Input Query           │
└────────────┬────────────────┘
             │
             ↓
      ┌──────────────────┐
      │ Explicit Mode?   │
      └──────┬───────────┘
             │
        ┌────┼────┐
        │    │    │
    Reasoning Fast Model
        │    │    │
        ↓    ↓    ↓
       Opus Haiku Specific
                  Model
             │
             ↓ (No explicit mode)
      ┌──────────────────┐
      │ Auto-Routing     │
      │ Enabled?         │
      └──────┬───────────┘
             │
        ┌────┼────┐
       Yes       No
        │         │
        ↓         ↓
   Assess    Use Default
   Complexity  (Sonnet)
        │
   ┌────┼────┐
   │    │    │
  High Med  Low
  ≥0.7 Mid  ≤0.3
   │    │    │
   ↓    ↓    ↓
 Opus Sonnet Haiku
```

**Complexity Indicators**:

| Score Range | Model | Example Queries |
|-------------|-------|-----------------|
| 0.0 - 0.3 | Haiku | "Is service running?", "List pods" |
| 0.3 - 0.7 | Sonnet | "Analyze this log", "Troubleshoot error" |
| 0.7 - 1.0 | Opus | "Design architecture", "Root cause analysis" |

### 4. Utilities

#### Logger (`utils/logger.py`)
- Structured logging with timestamps
- Consistent formatting across modules
- Level control (DEBUG, INFO, WARNING, ERROR)
- Stdout/stderr routing

## Configuration Management

### Configuration Hierarchy (Highest to Lowest Priority)

1. **CLI Arguments**: `--model opus`, `--reasoning`, `--fast`
2. **Environment Variables**: `COVERITY_ASSIST_URL`, `COVERITY_ASSIST_TOKEN`
3. **Config File**: `config/agent_config.json`
4. **Defaults**: Hardcoded in source

### Configuration Schema

```json
{
  "default_model": "sonnet",           // Default when no routing
  "reasoning_model": "opus",           // Model for --reasoning
  "fast_model": "haiku",               // Model for --fast
  "max_tokens": 800,                   // Standard response limit
  "reasoning_max_tokens": 2000,        // Extended limit for Opus
  "auto_routing": true,                // Enable complexity routing
  "complexity_threshold": 0.7,         // Opus activation threshold
  "model_arns": {
    "opus": "arn:aws:bedrock:...",
    "sonnet": "arn:aws:bedrock:...",
    "haiku": "arn:aws:bedrock:..."
  }
}
```

## Data Flow

### Standard Query Flow

```
1. User Input
   ↓
2. CLI Parsing
   ↓
3. Config Loading
   ↓
4. Agent Initialization
   ↓
5. Model Selection
   ├─ Check explicit mode flags
   ├─ Assess complexity (if auto-routing)
   └─ Select model ARN
   ↓
6. Build Request Payload
   ├─ Add messages
   ├─ Add model ARN
   ├─ Add system context (optional)
   └─ Set max_tokens
   ↓
7. HTTP POST to Coverity Assist
   ↓
8. Response Parsing
   ├─ Extract content
   ├─ Extract metadata (tokens, model)
   └─ Handle errors
   ↓
9. Format Output
   └─ JSON or Text
   ↓
10. Display to User
```

### Reasoning Mode Flow

```
1. User: --reasoning "Complex query"
   ↓
2. Mode Detection: reasoning = True
   ↓
3. Model Selection: Force Opus 4.6
   ↓
4. Max Tokens: Set to 2000 (extended)
   ↓
5. Execute with Opus ARN
   ↓
6. Return detailed response
```

## Error Handling Strategy

### Error Types and Responses

| Error Type | Handling Strategy | User Impact |
|------------|------------------|-------------|
| Missing Token | Immediate exit with clear message | Actionable error |
| Network Timeout | Retry once, then fail gracefully | Partial degradation |
| Invalid Model ARN | Fall back to default (Sonnet) | Transparent fallback |
| Malformed Response | Parse alternatives (content/response/text) | Robust parsing |
| Rate Limiting | Log and return 429 status | User notified |

### Logging Levels

- **DEBUG**: Complexity scores, model selection reasoning
- **INFO**: Model used, request sent, response received
- **WARNING**: Fallbacks activated, retries attempted
- **ERROR**: Request failures, invalid config, missing credentials

## Performance Considerations

### Response Time Expectations

| Model | Avg Response Time | Use Case |
|-------|------------------|----------|
| Haiku | 0.5 - 2 seconds | Quick validations |
| Sonnet | 2 - 5 seconds | Standard analysis |
| Opus | 5 - 15 seconds | Deep reasoning |

### Cost Optimization

**Cost Multipliers** (relative to Sonnet):
- Haiku: 0.1x (90% savings)
- Sonnet: 1.0x (baseline)
- Opus: 3.0x (3x cost)

**Optimization Strategies**:
1. Use complexity routing to minimize Opus usage
2. Prefer Haiku for boolean/validation queries
3. Set appropriate max_tokens limits
4. Cache frequently asked questions (future)

## Security Model

### Authentication Flow

```
1. User sets COVERITY_ASSIST_TOKEN env var
   ↓
2. Agent reads token at initialization
   ↓
3. Token included in Authorization header
   ↓
4. Coverity Assist validates token
   ↓
5. Token used for all subsequent requests
```

### Sensitive Data Handling

- **Never log tokens**: Tokens excluded from all logs
- **No credential storage**: Tokens ephemeral (env vars only)
- **HTTPS enforced**: All Coverity communication over TLS
- **No request caching**: Responses not persisted by default

## Extensibility Points

### Adding New Models

1. Update `ModelSelector.MODELS` dict with new entry
2. Add ARN to `config/agent_config.json`
3. Define complexity range or explicit flag
4. Document new model in user guide

### Adding Tools

Future architecture for tool integration:

```python
# src/agentjam/tools/base.py
class Tool:
    def execute(self, **kwargs): pass

# src/agentjam/tools/web_search.py
class WebSearchTool(Tool):
    def execute(self, query): 
        # Implementation
        pass
```

### Custom Complexity Scoring

Users can subclass `ModelSelector` and override `_assess_complexity()`:

```python
class CustomModelSelector(ModelSelector):
    def _assess_complexity(self, query: str) -> float:
        # Custom logic
        return custom_score
```

## Testing Strategy

### Unit Tests
- Model selection logic
- Complexity scoring algorithm
- Configuration loading
- Error handling

### Integration Tests
- End-to-end query execution
- Coverity Assist connectivity
- All model variants (Opus, Sonnet, Haiku)

### Performance Tests
- Response time benchmarks
- Concurrent request handling
- Memory usage under load

## Future Enhancements

### Planned Features
1. **Streaming Responses**: Real-time token streaming
2. **Conversation Memory**: Multi-turn context retention
3. **Tool Integration**: Web search, code execution, file I/O
4. **Custom Prompts**: User-defined system contexts
5. **Response Caching**: Reduce duplicate API calls
6. **Batch Processing**: Multi-query execution

### Experimental Ideas
- **Ensemble Mode**: Query multiple models, aggregate results
- **Cost Budgets**: User-defined spending limits
- **Audit Logs**: Persistent query/response history
- **Plugin System**: User-contributed tools
