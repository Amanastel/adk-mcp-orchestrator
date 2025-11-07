# Quick Start Guide

Get up and running with the ADK + MCP integration in 5 minutes!

## Prerequisites

```bash
# Check Python version (must be 3.10+)
python3 --version

# Check pip is installed
python3 -m pip --version
```

## Step 1: Install Dependencies

```bash
cd /Users/amankumar/Developer/agenticorch-assignment

# Install all required packages
python3 -m pip install fastapi uvicorn requests pydantic google-generativeai python-dotenv
```

## Step 2: Set Environment Variables

```bash
# Required API keys
export GITHUB_TOKEN="your_github_personal_access_token"
export OPENWEATHER_API_KEY="your_openweather_api_key"

# Optional: Add Google API key for AI features
# export GOOGLE_API_KEY="your_google_api_key"

# Optional: Add News API key for real news data
# export NEWS_API_KEY="your_news_api_key"
```

## Step 3: Start MCP Server

**Terminal 1:**
```bash
cd /Users/amankumar/Developer/agenticorch-assignment

# Start the server
python3 -m uvicorn mcp_server:app --reload --port 8001

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8001
# INFO:     Application startup complete.
```

**Test it works:**
```bash
# In another terminal
curl http://localhost:8001/health
```

## Step 4: Run ADK Agent

**Terminal 2:**

### Example 1: Get Weather
```bash
python3 adk_agent.py --task weather --city Delhi --no-ai
```

**Expected Output:**
```
🌤️  Weather in Delhi, IN:
   Temperature: 25.34°C (feels like 24.37°C)
   Conditions: Clear Sky
   Humidity: 17%
   Wind Speed: 2.59 m/s
```

### Example 2: GitHub Trends
```bash
python3 adk_agent.py --task trends --lang python --count 3 --no-ai
```

**Expected Output:**
```
⭐ Top 3 Trending Python Repositories:

1. public-apis/public-apis
   ⭐ 376,423 stars | 🍴 39,815 forks
   ...
```

### Example 3: News Headlines
```bash
python3 adk_agent.py --task news --count 3 --no-ai
```

### Example 4: Full Report
```bash
python3 adk_agent.py --task full --lang javascript --city London --no-ai
```

**Expected Output:**
```
================================================================================
📊 COMPREHENSIVE REPORT - 2025-11-07 20:39:19
================================================================================

🌤️  Weather in London, GB:
   ...

⭐ Top 5 Trending JavaScript Repositories:
   ...

📰 Top 3 News Headlines:
   ...
================================================================================
```

## Common Commands

### Different Cities
```bash
# US City
python3 adk_agent.py --task weather --city "San Francisco" --no-ai

# European City
python3 adk_agent.py --task weather --city Paris --no-ai

# Asian City
python3 adk_agent.py --task weather --city Tokyo --no-ai
```

### Different Programming Languages
```bash
# JavaScript
python3 adk_agent.py --task trends --lang javascript --count 5 --no-ai

# TypeScript
python3 adk_agent.py --task trends --lang typescript --count 5 --no-ai

# Rust
python3 adk_agent.py --task trends --lang rust --count 5 --no-ai

# Go
python3 adk_agent.py --task trends --lang go --count 5 --no-ai
```

### Vary the Count
```bash
# Top 10 repositories
python3 adk_agent.py --task trends --lang python --count 10 --no-ai

# Just the top one
python3 adk_agent.py --task trends --lang python --count 1 --no-ai
```

## Troubleshooting

### Server not starting?
```bash
# Check if port 8001 is in use
lsof -ti:8001

# Kill the process if needed
lsof -ti:8001 | xargs kill -9

# Restart server
python3 -m uvicorn mcp_server:app --reload --port 8001
```

### Connection refused?
```bash
# Make sure server is running
curl http://localhost:8001/health

# If not, start it in Terminal 1
```

### Missing modules?
```bash
# Reinstall dependencies
python3 -m pip install -r requirements.txt
```

## Using AI Features

If you have a Google API key:

```bash
# Set the key
export GOOGLE_API_KEY="your_actual_key_here"

# Run WITHOUT --no-ai flag
python3 adk_agent.py --task weather --city Delhi

# Output will include AI insights:
# 💡 AI Insight: The weather in Delhi is warm...
```

## Testing the Server Directly

### Health Check
```bash
curl http://localhost:8001/health | python3 -m json.tool
```

### Weather Tool
```bash
curl -X POST http://localhost:8001/tool/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "Delhi"}' | python3 -m json.tool
```

### GitHub Trends Tool
```bash
curl -X POST http://localhost:8001/tool/github_trends \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "count": 3}' | python3 -m json.tool
```

### News Tool
```bash
curl -X POST http://localhost:8001/tool/get_news \
  -H "Content-Type: application/json" \
  -d '{"count": 3}' | python3 -m json.tool
```

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

These provide interactive documentation where you can test all endpoints directly from your browser!

## Help Command

```bash
python3 adk_agent.py --help
```

## Success Indicators

✅ Server is healthy if `curl http://localhost:8001/health` returns 200
✅ Agent works if you see "✅ MCP server is healthy" message
✅ APIs working if you see real data (not mock)
✅ Proper output if you see emojis and formatted text

## Next Steps

1. ✅ Try different cities and languages
2. ✅ Explore the interactive docs at http://localhost:8001/docs
3. ✅ Add Google API key for AI insights
4. ✅ Read the full README.md for advanced usage
5. ✅ Check TEST_RESULTS.md to see all test cases

---

**That's it! You're ready to use the ADK + MCP integration!** 🚀

