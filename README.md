# AgentJAM 🤖

**J**ust **A**nother **M**ulti-model **Agent** - A dynamic AI agent framework with adaptive model selection for optimal reasoning and performance.

## 🌟 Features

- **Dynamic Model Selection**: Automatically switches between Claude models based on task complexity
  - **Opus 4.6**: Complex reasoning, critical decisions, novel problem-solving
  - **Sonnet 4.6**: Balanced performance for most tasks
  - **Haiku 4.5**: Fast responses for simple validations
  
- **Reasoning Mode**: Explicit flag to trigger advanced reasoning with Opus
- **Multi-Tool Integration**: Extensible tool system for various capabilities
- **Cost Optimization**: Intelligent model routing to balance quality and cost
- **Production Ready**: Comprehensive error handling and logging

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat"
export COVERITY_ASSIST_TOKEN="your-token-here"

# Run the agent
python -m agentjam.main "What is the best approach for debugging Lambda timeouts?"

# Enable reasoning mode for complex tasks
python -m agentjam.main --reasoning "Design a fault-tolerant microservices architecture"
```

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Model Selection Guide](docs/MODEL_SELECTION.md)
- [API Reference](docs/API_REFERENCE.md)
- [Contributing](docs/CONTRIBUTING.md)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AgentJAM Core                      │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │         Task Analysis & Routing              │   │
│  │  • Complexity Assessment                     │   │
│  │  • Model Selection Logic                     │   │
│  │  • Reasoning Mode Detection                  │   │
│  └─────────────────────────────────────────────┘   │
│                       ↓                              │
│  ┌──────────────┬──────────────┬──────────────┐   │
│  │   Opus 4.6   │  Sonnet 4.6  │  Haiku 4.5   │   │
│  │   (Advanced) │   (Default)  │    (Fast)    │   │
│  └──────────────┴──────────────┴──────────────┘   │
│                       ↓                              │
│  ┌─────────────────────────────────────────────┐   │
│  │            Tool Execution Layer              │   │
│  │  • Web Search • Code Analysis • Workflows   │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 🔧 Configuration

Create `config/agent_config.json`:

```json
{
  "default_model": "sonnet",
  "reasoning_model": "opus",
  "fast_model": "haiku",
  "max_tokens": 800,
  "reasoning_max_tokens": 2000,
  "auto_routing": true,
  "complexity_threshold": 0.7
}
```

## 📊 Model Selection Logic

| Task Type | Complexity | Model | Use Case |
|-----------|-----------|--------|----------|
| Simple Query | Low | Haiku 4.5 | "Is service running?" |
| Standard Analysis | Medium | Sonnet 4.6 | "Analyze this log file" |
| Complex Reasoning | High | Opus 4.6 | "Design disaster recovery plan" |
| Explicit --reasoning | N/A | Opus 4.6 | User-triggered deep analysis |

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/

# Type checking
mypy src/
```

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) first.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/askjake/AgentJAM/issues)
- **Documentation**: [Full Docs](docs/)
- **Contact**: Open an issue or PR

---

**Built with ❤️ for intelligent automation**
