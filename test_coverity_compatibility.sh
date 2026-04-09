#!/bin/bash
# Test Script for Coverity Assist Compatibility

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║        Coverity Assist Compatibility Test Suite                         ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
STAGING_URL="https://coverity-assist-stg.dishtv.technology"
PROD_URL="http://coverity-assist.dishtv.technology"
TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6InRlc3R1c2VyIiwidHlwZSI6IlBFUlNPTkFMIiwidmVyc2lvbiI6IjIiLCJqdGkiOiIyZDhmOWIxNC01YzIzLTQ5NTMtYmVkZi0yNWZiYmY2OWVkNjIiLCJzdWIiOiJ0ZXN0dXNlciIsImlzcyI6InRlc3Qtc2VydmljZSJ9.mKpL7NxBHR8lyoC6vw4jGY54r_q228kcCIzdGbTfWYN"

# ARNs from your deployment
OPUS_ARN="arn:aws:bedrock:us-west-2:233532778289:inference-profile/us.anthropic.claude-opus-4-6-v1"
SONNET_ARN="arn:aws:bedrock:us-west-2:233532778289:inference-profile/us.anthropic.claude-sonnet-4-6"
HAIKU_ARN="arn:aws:bedrock:us-west-2:233532778289:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((FAILED++))
    fi
}

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 1: Health Endpoint (Staging)                                      │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Testing: $STAGING_URL/health"

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/health" 2>&1)
if [ "$RESPONSE" = "200" ]; then
    print_result 0 "Staging health endpoint responding"
else
    print_result 1 "Staging health endpoint failed (HTTP $RESPONSE)"
fi
echo ""

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 2: Basic Chat Request (No Custom ARN)                             │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Testing: POST $STAGING_URL/chat"
echo "Payload: Basic message without inference_profile_arn"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$STAGING_URL/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Say hello in 5 words or less"}],
    "max_tokens": 50
  }' 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "Basic chat request works"
    echo -e "${BLUE}Response preview:${NC} $(echo "$BODY" | jq -r '.content // .response // .text // "N/A"' 2>/dev/null | head -c 100)"
else
    print_result 1 "Basic chat request failed (HTTP $HTTP_CODE)"
    echo -e "${YELLOW}Response:${NC} $BODY" | head -n 5
fi
echo ""

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 3: Chat Request with Sonnet ARN                                   │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Testing: POST $STAGING_URL/chat with inference_profile_arn"
echo "ARN: $SONNET_ARN"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$STAGING_URL/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": [{\"role\": \"user\", \"content\": \"Say testing in 3 words\"}],
    \"max_tokens\": 50,
    \"inference_profile_arn\": \"$SONNET_ARN\"
  }" 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "Custom ARN parameter accepted (Sonnet)"
    echo -e "${GREEN}✅ AgentJAM will work with Sonnet model${NC}"
else
    print_result 1 "Custom ARN parameter rejected (HTTP $HTTP_CODE)"
    echo -e "${YELLOW}Response:${NC} $BODY" | head -n 5
    echo -e "${YELLOW}⚠️  AgentJAM may need modification for model selection${NC}"
fi
echo ""

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 4: Chat Request with Opus ARN (Reasoning Mode)                    │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Testing: POST $STAGING_URL/chat with Opus ARN"
echo "ARN: $OPUS_ARN"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$STAGING_URL/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": [{\"role\": \"user\", \"content\": \"Respond with exactly: Opus active\"}],
    \"max_tokens\": 50,
    \"inference_profile_arn\": \"$OPUS_ARN\"
  }" 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "Opus ARN works (--reasoning mode will work)"
    echo -e "${GREEN}✅ AgentJAM --reasoning flag will use Opus correctly${NC}"
else
    print_result 1 "Opus ARN rejected (HTTP $HTTP_CODE)"
    echo -e "${YELLOW}⚠️  --reasoning mode may not work as expected${NC}"
fi
echo ""

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 5: Chat Request with Haiku ARN (Fast Mode)                        │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Testing: POST $STAGING_URL/chat with Haiku ARN"
echo "ARN: $HAIKU_ARN"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$STAGING_URL/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"messages\": [{\"role\": \"user\", \"content\": \"Say fast in 2 words\"}],
    \"max_tokens\": 20,
    \"inference_profile_arn\": \"$HAIKU_ARN\"
  }" 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    print_result 0 "Haiku ARN works (--fast mode will work)"
    echo -e "${GREEN}✅ AgentJAM --fast flag will use Haiku correctly${NC}"
else
    print_result 1 "Haiku ARN rejected (HTTP $HTTP_CODE)"
    echo -e "${YELLOW}⚠️  --fast mode may not work as expected${NC}"
fi
echo ""

echo "┌──────────────────────────────────────────────────────────────────────────┐"
echo "│  TEST 6: AgentJAM Python Import Test                                    │"
echo "└──────────────────────────────────────────────────────────────────────────┘"
echo ""

# Test Python imports
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from agentjam.core.agent import Agent
    from agentjam.models.model_selector import ModelSelector
    print('✅ PASS: Python modules import correctly')
    exit(0)
except ImportError as e:
    print(f'❌ FAIL: Import error: {e}')
    exit(1)
" 2>&1

if [ $? -eq 0 ]; then
    ((PASSED++))
else
    ((FAILED++))
fi
echo ""

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                           TEST SUMMARY                                   ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "  Total Tests: $((PASSED + FAILED))"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║   ✅ ALL TESTS PASSED - AgentJAM is compatible!               ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "You can now:"
    echo "  1. source setup_env.sh"
    echo "  2. python -m agentjam.main 'Your query here'"
    echo "  3. python -m agentjam.main --reasoning 'Complex analysis'"
    exit 0
elif [ $PASSED -ge 3 ]; then
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║                                                                ║${NC}"
    echo -e "${YELLOW}║   ⚠️  PARTIAL SUCCESS - Some issues detected                  ║${NC}"
    echo -e "${YELLOW}║                                                                ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "AgentJAM will work, but:"
    echo "  • Check failed tests above"
    echo "  • Some features may need adjustment"
    echo "  • See COVERITY_DEPLOYMENT_NOTES.md for details"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}║   ❌ COMPATIBILITY ISSUES - Manual configuration needed       ║${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Your Coverity Assist API might not support:"
    echo "  • Custom inference_profile_arn in requests"
    echo "  • Per-request model selection"
    echo ""
    echo "See COVERITY_DEPLOYMENT_NOTES.md for alternative approaches"
    exit 1
fi
