# AgentJAM Configuration for Your Coverity Assist Deployment

## ⚠️ IMPORTANT DIFFERENCES

Your Coverity Assist deployment uses different model naming than AgentJAM's defaults:

| AgentJAM Name | Coverity Config Name | Model | ARN |
|---------------|---------------------|-------|-----|
| `opus` | `advanced_reasoning` | Claude Opus 4.6 | ...opus-4-6-v1 |
| `sonnet` | `reasoning` | Claude Sonnet 4.6 | ...sonnet-4-6 |
| `haiku` | `simple` | Claude Haiku 4.5 | ...haiku-4-5-20251001-v1:0 |

## ✅ CONFIGURATION CORRECTED

The `config/agent_config.json` has been updated with:

1. **Correct ARNs** from your Kubernetes deployment
2. **Correct endpoint** (staging): https://coverity-assist-stg.dishtv.technology/chat
3. **Correct token** from your Secret
4. **Correct max_tokens** matching your deployment (8192 for Sonnet, 128000 for Opus)

## 🚀 HOW TO USE

### Setup Environment

```bash
# Source the environment setup
source setup_env.sh

# Or set manually:
export COVERITY_ASSIST_URL="https://coverity-assist-stg.dishtv.technology/chat"
export COVERITY_ASSIST_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6InRlc3R1c2VyIiwidHlwZSI6IlBFUlNPTkFMIiwidmVyc2lvbiI6IjIiLCJqdGkiOiIyZDhmOWIxNC01YzIzLTQ5NTMtYmVkZi0yNWZiYmY2OWVkNjIiLCJzdWIiOiJ0ZXN0dXNlciIsImlzcyI6InRlc3Qtc2VydmljZSJ9.mKpL7NxBHR8lyoC6vw4jGY54r_q228kcCIzdGbTfWYN"
```

### Test Connection

```bash
# Test health endpoint
curl https://coverity-assist-stg.dishtv.technology/health

# Test chat endpoint with your token
curl -X POST https://coverity-assist-stg.dishtv.technology/chat \
  -H "Authorization: Bearer $COVERITY_ASSIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello, test!"}],
    "max_tokens": 100
  }'
```

### Use AgentJAM

```bash
# Simple query (uses Sonnet via auto-routing)
python -m agentjam.main "Is the API healthy?"

# Complex reasoning (uses Opus via advanced_reasoning)
python -m agentjam.main --reasoning "Design a disaster recovery strategy"

# Fast mode (uses Haiku via simple)
python -m agentjam.main --fast "Quick status check"
```

## 🔧 MODEL ROUTING

When you use `--reasoning`, AgentJAM will:
1. Set `inference_profile_arn` to the Opus ARN in the request
2. Send to: https://coverity-assist-stg.dishtv.technology/chat
3. Coverity Assist will route to Claude Opus 4.6 (advanced_reasoning)

## ⚠️ COMPATIBILITY CHECK

### ✅ WILL WORK IF:
- Your Coverity Assist API accepts `inference_profile_arn` in POST body
- The `/chat` endpoint supports model selection via ARN parameter

### ❓ MIGHT NEED ADJUSTMENT IF:
- Your API only uses pre-configured environment variables (PLLM, SLLM, ALLM)
- Model selection is handled server-side by routing rules

### 🧪 TEST TO VERIFY:

```bash
# Test if custom ARN works
curl -X POST https://coverity-assist-stg.dishtv.technology/chat \
  -H "Authorization: Bearer $COVERITY_ASSIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Test"}],
    "inference_profile_arn": "arn:aws:bedrock:us-west-2:233532778289:inference-profile/us.anthropic.claude-opus-4-6-v1",
    "max_tokens": 100
  }'
```

If this returns an error about `inference_profile_arn`, then the API might not support per-request model selection.

## 🔄 ALTERNATIVE APPROACH

If your Coverity Assist API doesn't accept `inference_profile_arn` in requests, you have two options:

### Option 1: Use Server-Side Routing
Let Coverity Assist's routing rules decide (based on complexity_score):
```python
# Don't pass inference_profile_arn
# Let server-side routing handle model selection
```

### Option 2: Multiple Endpoint Approach
Configure different URLs for different models:
```json
{
  "endpoints": {
    "opus": "https://coverity-assist-stg.dishtv.technology/chat?model=advanced_reasoning",
    "sonnet": "https://coverity-assist-stg.dishtv.technology/chat?model=reasoning",
    "haiku": "https://coverity-assist-stg.dishtv.technology/chat?model=simple"
  }
}
```

## 📊 EXPECTED BEHAVIOR

| AgentJAM Mode | Request ARN | Coverity Routes To | Model |
|---------------|-------------|-------------------|-------|
| --reasoning | opus-4-6-v1 | advanced_reasoning | Opus 4.6 |
| (default) | sonnet-4-6 | reasoning | Sonnet 4.6 |
| --fast | haiku-4-5 | simple | Haiku 4.5 |

## 🔒 SECURITY NOTES

- ⚠️ The token in your Secret is a TEST TOKEN (contains "testuser")
- ✅ For production, request a proper token from your security team
- ✅ Token is already in your Kubernetes Secret, no need to hardcode

## 🐛 TROUBLESHOOTING

### "Connection refused"
```bash
# Check if service is running
kubectl get pods -n coverity-assist-stg
kubectl logs -n coverity-assist-stg deployment/deployment
```

### "401 Unauthorized"
```bash
# Verify token is correct
echo $COVERITY_ASSIST_TOKEN
```

### "Model not found" or "Invalid ARN"
```bash
# Your API might not support per-request model selection
# Try without inference_profile_arn parameter
```

## 📝 NEXT STEPS

1. Test the health endpoint: `curl https://coverity-assist-stg.dishtv.technology/health`
2. Test basic chat: `curl -X POST ... (see above)`
3. Test with custom ARN: Verify `inference_profile_arn` parameter works
4. If custom ARN works: You're good to go! ✅
5. If not: We'll need to modify AgentJAM to use server-side routing

---

**Generated**: 2026-04-09
**Target Environment**: coverity-assist-stg (Staging)
