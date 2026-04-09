#!/bin/bash
# Environment Setup for AgentJAM with your Coverity Assist Deployment

# STAGING ENVIRONMENT (Use this for testing)
export COVERITY_ASSIST_URL="https://coverity-assist-stg.dishtv.technology/chat"
export COVERITY_ASSIST_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6InRlc3R1c2VyIiwidHlwZSI6IlBFUlNPTkFMIiwidmVyc2lvbiI6IjIiLCJqdGkiOiIyZDhmOWIxNC01YzIzLTQ5NTMtYmVkZi0yNWZiYmY2OWVkNjIiLCJzdWIiOiJ0ZXN0dXNlciIsImlzcyI6InRlc3Qtc2VydmljZSJ9.mKpL7NxBHR8lyoC6vw4jGY54r_q228kcCIzdGbTfWYN"

# PRODUCTION ENVIRONMENT (Uncomment when ready for production)
# export COVERITY_ASSIST_URL="http://coverity-assist.dishtv.technology/chat"
# export COVERITY_ASSIST_TOKEN="your-production-token-here"

echo "✅ Environment configured for Coverity Assist"
echo "   URL: $COVERITY_ASSIST_URL"
