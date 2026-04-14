# Backend Version Guide

## CURRENT PRODUCTION VERSION

**File:** `intelligent_backend.py`  
**Size:** ~3000 lines (114 KB)
**Last Modified:** 2026-04-14

### Features (Latest Enhancements):
- ✅ **Artifact Relay** - Dynamic IP detection, inline base64, cloud relay
- ✅ **Implicit Tool Parser** - Fallback that executes code blocks automatically
- ✅ **Streaming Tool Detection** - Tools work in streaming responses
- ✅ **Enhanced System Prompt** - Explicit tool usage protocol
- ✅ **Agentic Loop** - Multi-turn tool execution
- ✅ **Message Summarization** - Intelligent context compression
- ✅ **504 Timeout Mitigation** - Adaptive retry logic
- ✅ **Auto-decomposition Monitoring** - Complexity analysis

### Startup Configuration:
- **Systemd Service:** `dishchat-backend.service`
- **Service File:** `/etc/systemd/system/dishchat-backend.service`
- **Working Directory:** `/home/agentpi003/dish-chat/backend`
- **Python Env:** `/home/agentpi003/dish-chat-venv/bin/python3`
- **Log File:** `/home/agentpi003/dish-chat/logs/intelligent_backend.log`

### Service Management:
```bash
# Status
sudo systemctl status dishchat-backend.service

# Restart
sudo systemctl restart dishchat-backend.service

# Logs
sudo journalctl -u dishchat-backend.service -f
tail -f /home/agentpi003/dish-chat/logs/intelligent_backend.log
```

## ⚠️ BACKUPS (DO NOT USE FOR STARTUP)

All files matching `intelligent_backend.py.backup*` are historical backups.
**These are kept for rollback purposes ONLY.**

### Recent Important Backups:
- `intelligent_backend.py.backup-pre-streaming-fix-*` - Before streaming tool detection (2026-04-14)
- `intelligent_backend.py.backup-pre-tool-usage-fix-*` - Before implicit parser (2026-04-13)
- `intelligent_backend.py.backup-pre-artifact-relay-*` - Before artifact enhancements (2026-04-13)
- `intelligent_backend.py.backup-parser-*` - Before parser integration (2026-04-13)

### To Rollback to a Previous Version:
```bash
# Stop the service
sudo systemctl stop dishchat-backend.service

# Restore from backup
cd /home/agentpi003/dish-chat/backend
cp intelligent_backend.py.backup-TIMESTAMP intelligent_backend.py

# Restart
sudo systemctl start dishchat-backend.service

# Verify
sudo systemctl status dishchat-backend.service
```

## ⚠️ OLD/DEPRECATED LOCATIONS

### DO NOT USE These Directories:
- `/home/agentpi003/dishchat/backend/` - **OLD LOCATION (deprecated)**
- Any backend outside `/home/agentpi003/dish-chat/backend/` - **OUTDATED**

### Why They Exist:
These are remnants from earlier deployments before the systemd service was configured.
They may contain old code without the latest enhancements.

## ✅ CORRECT BACKEND LOCATION

**Always use this location:**
```
/home/agentpi003/dish-chat/backend/intelligent_backend.py
```

**Verify it's being used:**
```bash
systemctl cat dishchat-backend.service | grep WorkingDirectory
# Should show: WorkingDirectory=/home/agentpi003/dish-chat/backend

ps aux | grep intelligent_backend
# Should show process running from /home/agentpi003/dish-chat/backend
```

## Version History

### v3.0 (2026-04-14) - Streaming Tool Detection
- Added implicit tool detection to streaming endpoint
- Tools now execute in both regular and streaming modes

### v2.0 (2026-04-13) - Major Enhancements
- Artifact relay with dynamic IP
- Implicit tool parser (markdown code block execution)
- Enhanced system prompt
- Multiple delivery methods for files

### v1.0 (2026-04-09) - Production Base
- Message summarization
- 504 mitigation
- Agentic loop
- Tool execution framework

## Troubleshooting

### Tools Not Executing
1. Check logs: `tail -100 /home/agentpi003/dish-chat/logs/intelligent_backend.log`
2. Look for: "📝 Detected implicit" or "🔧 Executing tool"
3. Verify modules exist:
   - `ls /home/agentpi003/dish-chat/backend/artifact_relay.py`
   - `ls /home/agentpi003/dish-chat/backend/implicit_tool_parser.py`

### Service Won't Start
1. Check syntax: `python3 -m py_compile /home/agentpi003/dish-chat/backend/intelligent_backend.py`
2. Check imports: `cd /home/agentpi003/dish-chat/backend && python3 -c "from artifact_relay import *; from implicit_tool_parser import *"`
3. Check journal: `sudo journalctl -u dishchat-backend.service -n 50`

### Wrong Version Running
1. Verify systemd points to correct file:
   ```bash
   systemctl cat dishchat-backend.service | grep WorkingDirectory
   ```
2. Restart service:
   ```bash
   sudo systemctl restart dishchat-backend.service
   ```

## Git Information

**Repository:** askjake/AgentJAM  
**Branch:** agentpi003-updates  
**Last Commit:** 7df8103 - "Fix: Implement artifact relay and implicit tool execution"

---

**Last Updated:** 2026-04-14 07:34:10  
**Maintained By:** Agent Enhancement Protocol
