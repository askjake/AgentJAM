# AgentJAM - Intelligent Chat Agent

**Production-ready AI agent with self-improvement capabilities, streaming responses, and markdown rendering.**

## 🎯 Features

### Core Capabilities
- ✅ **Streaming Responses** - Token-by-token SSE streaming
- ✅ **Markdown Rendering** - Beautiful formatted text with syntax highlighting
- ✅ **Self-Improvement** - Persistent memory, journal, and methodology evolution
- ✅ **Long-term Memory** - Importance-scored message retention beyond sessions
- ✅ **Methodology Evolution** - Self-improving rule effectiveness tracking
- ✅ **Tool Execution** - Shell commands, Python scripts, file operations
- ✅ **Vision Support** - Image analysis and processing
- ✅ **Multi-model LLM** - Routes through Coverity Assist (Claude, Haiku, Opus)

### Self-Improvement Features
- **Self-Reflection Journal** - Auto-reflection every 10 messages, persisted to database
- **Methodology Rules** - Effectiveness tracking with usage statistics
- **Long-term Memory** - Unlimited message history with importance scoring
- **Personality Profile** - Evolution tracking across 4 dimensions
- **Tool Analytics** - Success rates and performance metrics

### Technical Features
- **504 Timeout Mitigation** - Adaptive token estimation and throttling
- **Message Compression** - Smart summarization for context management
- **Persistent Storage** - SQLite database for all self-improvement data
- **Error Handling** - Graceful degradation and retry logic

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────────┐
│  Frontend   │────────▶│   Backend    │────────▶│ Coverity       │
│  (Port 3000)│  HTTP   │  (Port 8000) │  HTTPS  │ Assist API     │
│             │◀────────│   Flask      │◀────────│ (Multi-model)  │
│  - Dashboard│  SSE    │   + Tools    │         │                │
│  - Markdown │ Stream  │   + Memory   │         │ - Claude 4.6   │
│  - Chat UI  │         │   + Journal  │         │ - Haiku 4.5    │
└─────────────┘         └──────────────┘         │ - Opus 4.6     │
                              │                   └────────────────┘
                              │
                        ┌─────▼──────┐
                        │  SQLite    │
                        │  Database  │
                        │            │
                        │ - Journal  │
                        │ - Memory   │
                        │ - Rules    │
                        └────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.11+
- Git
- Access to Coverity Assist API (or configure alternative LLM)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/askjake/AgentJAM.git
   cd AgentJAM
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment** (see Environment Variables section)
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Initialize database**
   ```bash
   python3 init_db.py
   ```

5. **Start backend**
   ```bash
   ./start-backend.sh
   # Or manually:
   source .venv/bin/activate
   python intelligent_backend.py
   ```

6. **Start frontend** (in new terminal)
   ```bash
   cd frontend
   python3 server.py
   ```

7. **Access the UI**
   - Frontend: http://localhost:3000/enhanced/
   - Backend API: http://localhost:8000/health

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory. **See ENVIRONMENT.md for all required variables.**

Key variables:
- `COVERITY_ASSIST_TOKEN` - Authentication token
- `COVERITY_ASSIST_URL` - API endpoint
- `REQUEST_TIMEOUT` - Request timeout in seconds
- `ENABLE_JOURNALING` - Enable self-reflection (true/false)
- `MAX_CONTEXT` - Maximum context window size

**Full environment configuration provided in separate `ENVIRONMENT.md` file.**

## 📊 Database Schema

The agent uses SQLite for persistence with 5 tables:

1. **journal_entries** - Self-reflection journal
2. **methodology_rules** - Effectiveness tracking
3. **long_term_memory** - Message history with importance scores
4. **personality_profile** - Evolution tracking
5. **tool_usage_analytics** - Tool performance metrics

## 🚀 Usage

### Basic Chat
1. Open http://localhost:3000/enhanced/
2. Type your message
3. Watch the streaming response appear token-by-token
4. Markdown is automatically rendered (code blocks, lists, etc.)

### Advanced Features

**Reasoning Mode:**
- Enable in chat settings for detailed chain-of-thought

**Tool Execution:**
- Agent can run shell commands (if enabled)
- Python script execution
- File operations

**Self-Improvement:**
- Journal reflects every 10 messages
- Methodology rules evolve with usage
- Long-term memory retained with importance scores

## 🗂️ Project Structure

```
AgentJAM/
├── backend/
│   ├── intelligent_backend.py       # Main Flask application
│   ├── agent_persistence.py         # Database persistence layer
│   ├── init_db.py                   # Database initialization
│   ├── enhanced_agent_504_mitigation.py  # Timeout handling
│   ├── requirements.txt             # Python dependencies
│   └── .venv/                       # Virtual environment
├── frontend/
│   ├── server.py                    # Frontend server
│   ├── enhanced/
│   │   ├── index.html               # Main UI
│   │   └── static/
│   │       ├── js/
│   │       │   ├── dashboard.js     # Main application logic
│   │       │   └── custom_tools.js  # Tool management
│   │       └── css/
│   │           └── dashboard.css    # Styling + markdown
├── docs/                            # Documentation
├── custom_tools/                    # Custom tool definitions
├── .env.example                     # Environment template
├── .gitignore                       # Git exclusions
└── README.md                        # This file
```

## 📝 API Endpoints

### Health Check
```bash
GET /health
```

### Chat (Non-streaming)
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Your question",
  "chat_id": "optional-chat-id",
  "reasoning_mode": false
}
```

### Chat (Streaming)
```bash
POST /api/chat/stream
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your question"}
  ],
  "chat_id": "optional-chat-id"
}
```

### Statistics
```bash
GET /api/statistics
```

## 🧪 Testing

Test the streaming endpoint:
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Test database:
```bash
python3 backend/agent_persistence.py
```

## 🔧 Troubleshooting

### Backend won't start
- Check `.env` file exists with valid credentials
- Verify virtual environment is activated
- Check logs: `tail -f /tmp/backend.log`

### No streaming responses
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check browser console for errors

### Database errors
```bash
cd backend
python3 init_db.py  # Reinitialize database
```

### Port already in use
```bash
# Find process on port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill if needed
kill -9 <PID>
```

## 📈 Performance

- **Streaming Latency:** ~50-200ms first token
- **Token Throughput:** ~20-50 tokens/second
- **Context Window:** Up to 200k tokens
- **Memory Overhead:** ~50MB base + context
- **Database Size:** Grows with usage (~1KB per message)

## 🔒 Security

- ✅ Environment variables for secrets
- ✅ No credentials in code
- ✅ .gitignore excludes sensitive files
- ✅ Database access only via context managers
- ⚠️ Shell execution disabled by default (enable with caution)

## 🤝 Contributing

This agent is configured for DISH internal use. For contributions:
1. Create feature branch
2. Test thoroughly
3. Submit PR with description

## 📄 License

Internal DISH project - proprietary.

## 🙏 Acknowledgments

Built with:
- Flask (backend)
- marked.js (markdown rendering)
- Coverity Assist API (multi-model LLM)
- SQLite (persistence)

## 📞 Support

For issues or questions:
- Check logs: `/tmp/backend.log`, `/tmp/frontend.log`
- Review documentation in `docs/`
- Test with `python3 agent_persistence.py`

---

**Version:** 1.0.0  
**Last Updated:** 2026-04-09  
**Status:** ✅ Production Ready
