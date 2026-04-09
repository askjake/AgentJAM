# AgentJAM Deployment Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git 2.x or higher
- Network access to Coverity Assist endpoint
- Valid Coverity Assist token

### Environment Setup

1. **Install Python Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Set Environment Variables**
```bash
export COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat"
export COVERITY_ASSIST_TOKEN="your-token-here"
```

For persistent configuration:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat"' >> ~/.bashrc
echo 'export COVERITY_ASSIST_TOKEN="your-token-here"' >> ~/.bashrc
source ~/.bashrc
```

## Installation Methods

### Method 1: From Source (Development)

```bash
# Clone repository
git clone https://github.com/askjake/AgentJAM.git
cd AgentJAM

# Install dependencies
pip install -r requirements.txt

# Run directly
python -m agentjam.main "Your query here"
```

### Method 2: Pip Install (Future)

```bash
# Once published to PyPI
pip install agentjam

# Run as command
agentjam "Your query here"
```

### Method 3: Docker (Containerized)

```bash
# Build image
docker build -t agentjam:latest .

# Run container
docker run --rm \
  -e COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat" \
  -e COVERITY_ASSIST_TOKEN="your-token" \
  agentjam:latest "Your query here"
```

## Configuration

### Update Model ARNs

Edit `config/agent_config.json`:

```json
{
  "model_arns": {
    "opus": "arn:aws:bedrock:us-west-2:<account>:application-inference-profile/<opus-id>",
    "sonnet": "arn:aws:bedrock:us-west-2:<account>:application-inference-profile/<sonnet-id>",
    "haiku": "arn:aws:bedrock:us-west-2:<account>:application-inference-profile/<haiku-id>"
  }
}
```

Get ARNs from your AWS Bedrock console or DevOps team.

### Adjust Routing Behavior

```json
{
  "auto_routing": true,              // Enable complexity-based routing
  "complexity_threshold": 0.7,       // Opus activation threshold
  "max_tokens": 800,                 // Standard response limit
  "reasoning_max_tokens": 2000       // Extended limit for Opus
}
```

## Verification

### Test Installation

```bash
# Basic connectivity test
python -m agentjam.main "Echo test: Hello AgentJAM"

# Test each model explicitly
python -m agentjam.main --model haiku "Quick test"
python -m agentjam.main --model sonnet "Standard test"
python -m agentjam.main --model opus "Complex test"

# Test reasoning mode
python -m agentjam.main --reasoning "Design a simple cache"

# Test auto-routing
python -m agentjam.main --verbose "Analyze this complex system" | grep "Model Used"
```

### Verify Environment

```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep requests

# Verify token is set
echo $COVERITY_ASSIST_TOKEN  # Should not be empty

# Test Coverity connectivity
curl -H "Authorization: Bearer $COVERITY_ASSIST_TOKEN" \
     http://coverity-assist.dishtv.technology/health
```

## Production Deployment

### Systemd Service (Linux)

Create `/etc/systemd/system/agentjam.service`:

```ini
[Unit]
Description=AgentJAM Service
After=network.target

[Service]
Type=simple
User=agentjam
WorkingDirectory=/opt/agentjam
Environment="COVERITY_ASSIST_URL=http://coverity-assist.dishtv.technology/chat"
Environment="COVERITY_ASSIST_TOKEN=your-token-here"
ExecStart=/usr/bin/python3 -m agentjam.main --daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable agentjam
sudo systemctl start agentjam
sudo systemctl status agentjam
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  agentjam:
    build: .
    image: agentjam:latest
    environment:
      - COVERITY_ASSIST_URL=http://coverity-assist.dishtv.technology/chat
      - COVERITY_ASSIST_TOKEN=${COVERITY_ASSIST_TOKEN}
    volumes:
      - ./config:/app/config:ro
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
docker-compose logs -f agentjam
```

### Kubernetes Deployment

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentjam
  namespace: ai-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentjam
  template:
    metadata:
      labels:
        app: agentjam
    spec:
      containers:
      - name: agentjam
        image: agentjam:latest
        env:
        - name: COVERITY_ASSIST_URL
          value: "http://coverity-assist.dishtv.technology/chat"
        - name: COVERITY_ASSIST_TOKEN
          valueFrom:
            secretKeyRef:
              name: coverity-token
              key: token
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Secret
metadata:
  name: coverity-token
  namespace: ai-agents
type: Opaque
stringData:
  token: "your-token-here"
```

Deploy:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl get pods -n ai-agents
kubectl logs -f deployment/agentjam -n ai-agents
```

## Monitoring and Logging

### Enable Verbose Logging

```bash
# Temporary (single run)
python -m agentjam.main --verbose "Your query"

# Persistent (environment variable)
export AGENTJAM_LOG_LEVEL=DEBUG
```

### Log Output Structure

```
2026-04-09 14:30:15 - agentjam.core.agent - INFO - Agent initialized
2026-04-09 14:30:16 - agentjam.models.model_selector - INFO - Complexity score: 0.75
2026-04-09 14:30:16 - agentjam.models.model_selector - INFO - High complexity detected - routing to Opus
2026-04-09 14:30:16 - agentjam.core.agent - INFO - Selected Model: Claude Opus 4.6
2026-04-09 14:30:21 - agentjam.core.agent - INFO - Response received (1250 tokens)
```

### Prometheus Metrics (Future)

Planned metrics endpoints:
- `/metrics` - Prometheus-compatible metrics
- `agentjam_requests_total{model="opus|sonnet|haiku"}`
- `agentjam_request_duration_seconds{model="..."}`
- `agentjam_request_tokens_total{model="..."}`

## Troubleshooting

### Common Issues

#### "COVERITY_ASSIST_TOKEN not set"
```bash
# Solution: Set environment variable
export COVERITY_ASSIST_TOKEN="your-token-here"
```

#### "Connection refused"
```bash
# Solution: Verify Coverity Assist is running
curl http://coverity-assist.dishtv.technology/health

# Check firewall rules
telnet coverity-assist.dishtv.technology 80
```

#### "401 Unauthorized"
```bash
# Solution: Token expired or invalid
# Request new token from DevOps team
# Update environment variable
```

#### "Model ARN not found"
```bash
# Solution: Update config/agent_config.json with correct ARNs
# Get ARNs from: aws bedrock list-inference-profiles
```

### Debug Mode

```bash
# Maximum verbosity
python -m agentjam.main --verbose "Your query" 2>&1 | tee debug.log

# Check Python traceback
python -m agentjam.main "Your query" 2>&1 | grep -A 20 "Traceback"
```

### Network Diagnostics

```bash
# Test DNS resolution
nslookup coverity-assist.dishtv.technology

# Test HTTP connectivity
curl -v http://coverity-assist.dishtv.technology/health

# Test with token
curl -H "Authorization: Bearer $COVERITY_ASSIST_TOKEN" \
     http://coverity-assist.dishtv.technology/chat \
     -d '{"messages": [{"role": "user", "content": "test"}]}' \
     -H "Content-Type: application/json"
```

## Security Best Practices

### Token Management

❌ **Never**:
- Commit tokens to git
- Log tokens in plain text
- Share tokens in chat/email
- Store tokens in code

✅ **Always**:
- Use environment variables
- Rotate tokens regularly
- Use separate tokens per environment
- Revoke compromised tokens immediately

### Network Security

```bash
# Use HTTPS in production
export COVERITY_ASSIST_URL="https://coverity-assist.dishtv.technology/chat"

# Verify SSL certificates
curl --cacert /path/to/ca-bundle.crt https://coverity-assist.dishtv.technology/health
```

### Access Control

```bash
# Restrict file permissions
chmod 600 config/agent_config.json
chmod 700 /opt/agentjam

# Run as non-root user
useradd -r -s /bin/false agentjam
chown -R agentjam:agentjam /opt/agentjam
```

## Maintenance

### Update AgentJAM

```bash
# Pull latest code
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart agentjam
```

### Backup Configuration

```bash
# Backup config directory
tar -czf agentjam-config-$(date +%Y%m%d).tar.gz config/

# Store securely (not in git!)
mv agentjam-config-*.tar.gz /secure/backup/location/
```

### Log Rotation

Create `/etc/logrotate.d/agentjam`:

```
/var/log/agentjam/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 agentjam agentjam
    sharedscripts
    postrotate
        systemctl reload agentjam > /dev/null 2>&1 || true
    endscript
}
```

## Performance Tuning

### Optimize Response Time

```bash
# Use fast mode for simple queries
python -m agentjam.main --fast "Quick check"

# Reduce max_tokens for shorter responses
python -m agentjam.main --max-tokens 400 "Brief answer needed"

# Disable auto-routing for predictable performance
# Edit config: "auto_routing": false
```

### Concurrent Requests

```python
# Example: Parallel queries
import concurrent.futures
from agentjam.core.agent import Agent

agent = Agent(config=config)

queries = ["Query 1", "Query 2", "Query 3"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(agent.execute, queries))
```

## Support and Resources

- **GitHub**: https://github.com/askjake/AgentJAM
- **Issues**: https://github.com/askjake/AgentJAM/issues
- **Documentation**: https://github.com/askjake/AgentJAM/tree/main/docs
- **Examples**: https://github.com/askjake/AgentJAM/tree/main/examples

For DISH-specific support:
- **Slack**: #dish-chat-support
- **Coverity Assist Status**: http://coverity-assist.dishtv.technology/health
