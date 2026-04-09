# AgentJAM Quick Start Guide

Get up and running with AgentJAM in 5 minutes!

## Installation

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/askjake/AgentJAM.git
cd AgentJAM

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat"
export COVERITY_ASSIST_TOKEN="your-token-here"

# Test installation
python -m agentjam.main "Hello, AgentJAM!"
```

### Option 2: Docker

```bash
# Pull and run
docker build -t agentjam:latest .
docker run --rm \
  -e COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat" \
  -e COVERITY_ASSIST_TOKEN="your-token" \
  agentjam:latest "Your query here"
```

## Basic Usage

### Simple Query (Auto-Routing)

```bash
# Let AgentJAM choose the best model
python -m agentjam.main "Analyze this error: Connection timeout"
```

### Fast Mode (Use Haiku)

```bash
# Quick responses for simple queries
python -m agentjam.main --fast "Is the API healthy?"
```

### Reasoning Mode (Use Opus)

```bash
# Deep analysis for complex problems
python -m agentjam.main --reasoning "Design a disaster recovery strategy"
```

### Explicit Model Selection

```bash
# Force a specific model
python -m agentjam.main --model opus "Complex query"
python -m agentjam.main --model sonnet "Standard query"
python -m agentjam.main --model haiku "Simple query"
```

## Configuration

### Update Model ARNs

Edit `config/agent_config.json`:

```json
{
  "model_arns": {
    "opus": "arn:aws:bedrock:us-west-2:ACCOUNT:application-inference-profile/OPUS-ID",
    "sonnet": "arn:aws:bedrock:us-west-2:ACCOUNT:application-inference-profile/SONNET-ID",
    "haiku": "arn:aws:bedrock:us-west-2:ACCOUNT:application-inference-profile/HAIKU-ID"
  }
}
```

### Adjust Routing Behavior

```json
{
  "auto_routing": true,           // Enable/disable auto-routing
  "complexity_threshold": 0.7,    // Opus activation threshold (0.0-1.0)
  "max_tokens": 800,              // Standard response limit
  "reasoning_max_tokens": 2000    // Extended limit for reasoning mode
}
```

## Common Use Cases

### 1. Code Review

```bash
python -m agentjam.main "Review this Python function for security issues:

def process_user_input(data):
    query = 'SELECT * FROM users WHERE id = ' + data
    return db.execute(query)
"
```

### 2. Troubleshooting

```bash
python -m agentjam.main --reasoning "Our Lambda functions are timing out intermittently. 
The timeout is set to 30s, but CloudWatch shows execution times around 25-28s before failure. 
What could be causing this?"
```

### 3. System Design

```bash
python -m agentjam.main --reasoning "Design a microservices architecture for an e-commerce 
platform that needs to handle 10,000 requests per second with 99.99% uptime"
```

### 4. Quick Status Checks

```bash
python -m agentjam.main --fast "Is Kubernetes cluster healthy?"
```

### 5. Log Analysis

```bash
# Use standard mode (Sonnet)
python -m agentjam.main "Analyze this error log:

2026-04-09 10:15:23 ERROR: Connection refused
2026-04-09 10:15:24 WARN: Retry attempt 1 of 3
2026-04-09 10:15:25 ERROR: Connection refused
2026-04-09 10:15:26 FATAL: Max retries exceeded
"
```

## Advanced Features

### JSON Output

```bash
# Get structured JSON response
python -m agentjam.main --json "Analyze this code" > output.json
```

### Verbose Logging

```bash
# See model selection reasoning
python -m agentjam.main --verbose "Your query" | grep "Model Used"
```

### Custom Token Limits

```bash
# Shorter responses
python -m agentjam.main --max-tokens 400 "Brief summary needed"

# Longer responses
python -m agentjam.main --max-tokens 2000 "Detailed explanation required"
```

## Troubleshooting

### "COVERITY_ASSIST_TOKEN not set"

```bash
# Set the environment variable
export COVERITY_ASSIST_TOKEN="your-token-here"

# Or add to ~/.bashrc for persistence
echo 'export COVERITY_ASSIST_TOKEN="your-token"' >> ~/.bashrc
source ~/.bashrc
```

### "Connection refused"

```bash
# Verify Coverity Assist is accessible
curl http://coverity-assist.dishtv.technology/health

# Check your network connection
ping coverity-assist.dishtv.technology
```

### "Invalid model ARN"

```bash
# Update config/agent_config.json with correct ARNs
# Get ARNs from AWS console or your DevOps team
```

## Next Steps

- **Full Documentation**: See [docs/](docs/) for detailed guides
- **Examples**: Check [examples/](examples/) for code samples
- **Issues**: Report bugs at [GitHub Issues](https://github.com/askjake/AgentJAM/issues)

## Model Selection Cheat Sheet

| Query Type | Command | Model Used | Response Time |
|------------|---------|------------|---------------|
| Simple status | `--fast` | Haiku | 0.5-2s |
| Standard analysis | (none) | Sonnet | 2-5s |
| Complex reasoning | `--reasoning` | Opus | 5-15s |
| Explicit choice | `--model <name>` | Specified | Varies |

## Cost Optimization Tips

1. **Use `--fast` for simple queries** → 90% cost savings
2. **Let auto-routing decide** → Optimal cost/quality balance
3. **Reserve `--reasoning` for critical decisions** → Use Opus sparingly
4. **Set appropriate `--max-tokens`** → Don't pay for unused tokens

## Support

- **Documentation**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Model Guide**: [docs/MODEL_SELECTION.md](docs/MODEL_SELECTION.md)
- **Deployment**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **GitHub**: https://github.com/askjake/AgentJAM

---

**Happy Agent Jamming! 🎸**
