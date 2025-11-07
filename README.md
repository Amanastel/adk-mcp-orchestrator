# AgenticOrch Take-Home Assignment
## Google ADK + MCP Integration Challenge

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-ready implementation of Google Agent Development Kit (ADK) integrated with a custom Model Context Protocol (MCP) server, demonstrating intelligent tool orchestration and API integration.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Key Learnings](#key-learnings)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project demonstrates a complete ADK-MCP integration where:

1. **MCP Server**: A FastAPI-based server exposing 3 production-ready tools
2. **ADK Agent**: An intelligent agent that orchestrates MCP tools using Google's Gemini model
3. **Real-world APIs**: Integration with GitHub, OpenWeather, and NewsAPI

### What is ADK?

Google's Agent Development Kit (ADK) provides a framework for building AI agents that can:
- Execute complex, multi-step tasks
- Use external tools and APIs
- Generate human-like, context-aware responses

### What is MCP?

Model Context Protocol (MCP) is a standardized way to:
- Expose tools/functions to AI models
- Enable consistent tool discovery and execution
- Facilitate agent-to-tool communication

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        ADK Agent                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Google Gemini (gemini-pro)                  │   │
│  │  - Natural language understanding                   │   │
│  │  - Response generation                              │   │
│  │  - Context synthesis                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            MCP Client (HTTP)                        │   │
│  │  - Tool discovery                                   │   │
│  │  - Request formatting                               │   │
│  │  - Response parsing                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server (FastAPI)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Weather     │  │   GitHub     │  │    News      │     │
│  │    Tool      │  │   Trends     │  │    Tool      │     │
│  │              │  │    Tool      │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │              │
└─────────┼─────────────────┼──────────────────┼──────────────┘
          │                 │                  │
          ▼                 ▼                  ▼
   ┌────────────┐   ┌────────────┐   ┌────────────┐
   │ OpenWeather│   │   GitHub   │   │  NewsAPI   │
   │    API     │   │    API     │   │            │
   └────────────┘   └────────────┘   └────────────┘
```

---

## ✨ Features

### MCP Server (`mcp_server.py`)

✅ **3 Production-Ready Tools**:
1. **Weather Tool** - Get real-time weather data for any city
2. **GitHub Trends Tool** - Fetch trending repositories by language
3. **News Tool** - Retrieve top headlines with optional search

✅ **Enterprise Features**:
- Comprehensive logging with timestamps
- Structured error handling
- Request/response validation with Pydantic
- Health check endpoint
- Mock data fallback for missing API keys
- Type hints throughout
- API rate limiting awareness

### ADK Agent (`adk_agent.py`)

✅ **Intelligent Task Execution**:
- **Weather Task**: Get weather + AI insights
- **Trends Task**: Fetch trending repos + AI analysis
- **News Task**: Get headlines + AI summary
- **Full Task**: Comprehensive report combining all tools

✅ **Advanced Capabilities**:
- Natural language response generation
- Context-aware AI insights using Gemini
- Graceful degradation (works with/without Google API key)
- Flexible CLI interface
- Rich formatted output
- Error recovery and retry logic

---

## 🔧 Prerequisites

- **Python**: 3.10 or higher
- **uv**: Python package installer ([Install uv](https://github.com/astral-sh/uv))
- **API Keys** (provided by user):
  - GitHub Personal Access Token
  - OpenWeather API Key
  - Google Gemini API Key (for AI features)
  - NewsAPI Key (optional - uses mock data if absent)

---

## 📦 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd /Users/amankumar/Developer/agenticorch-assignment
```

### 2. Initialize UV Environment

```bash
# Initialize uv project
uv init

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Alternative: Use Standard pip

```bash
# Option 1: Using uv (Recommended - faster)
uv venv
source .venv/bin/activate  # On macOS/Linux
uv pip install -r requirements.txt

# Option 2: Using standard pip
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Set Environment Variables

Create a `.env` file or export variables:

```bash
# Required: GitHub API
export GITHUB_TOKEN="your_github_personal_access_token"

# Required: OpenWeather API
export OPENWEATHER_API_KEY="your_openweather_api_key"

# Required: Google Gemini API (for AI features)
export GOOGLE_API_KEY="your_google_api_key_here"

# Optional: NewsAPI (uses mock data if not provided)
export NEWS_API_KEY="your_news_api_key_here"
```

### API Key Sources

- **GitHub Token**: https://github.com/settings/tokens
- **OpenWeather Key**: https://openweathermap.org/api
- **Google API Key**: https://makersuite.google.com/app/apikey
- **NewsAPI Key**: https://newsapi.org/register

---

## 🚀 Usage

### Step 1: Start the MCP Server

In one terminal window:

```bash
# Using uvicorn directly
uvicorn mcp_server:app --reload --port 8001

# Or using the script directly
python mcp_server.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

Verify server is running:
```bash
curl http://localhost:8001/health
```

### Step 2: Run the ADK Agent

In another terminal window:

#### Weather Task
```bash
python adk_agent.py --task weather --city Delhi
```

**Example Output:**
```
🔍 Checking MCP server health...
✅ MCP server is healthy

🌤️  Weather in Delhi, IN:
   Temperature: 28.5°C (feels like 29.0°C)
   Conditions: Haze
   Humidity: 62%
   Wind Speed: 2.5 m/s

💡 AI Insight: The weather in Delhi is warm with hazy conditions. 
It's a good idea to wear light, breathable clothing and consider 
wearing a mask if you're sensitive to air quality. Perfect weather 
for indoor activities or early morning/evening walks.
```

#### GitHub Trends Task
```bash
python adk_agent.py --task trends --lang python --count 3
```

**Example Output:**
```
⭐ Top 3 Trending Python Repositories:

1. tensorflow/tensorflow
   ⭐ 185,234 stars | 🍴 74,123 forks
   📝 An Open Source Machine Learning Framework for Everyone
   🔗 https://github.com/tensorflow/tensorflow

2. django/django
   ⭐ 78,456 stars | 🍴 31,234 forks
   📝 The Web framework for perfectionists with deadlines
   🔗 https://github.com/django/django

3. pallets/flask
   ⭐ 66,789 stars | 🍴 16,234 forks
   📝 The Python micro framework for building web applications
   🔗 https://github.com/pallets/flask

💡 AI Insight: TensorFlow continues to dominate as the top Python 
repository, reflecting the ongoing growth in machine learning and 
AI development. Developers can learn about production-ready ML 
pipelines, distributed training, and model deployment strategies.
```

#### News Task
```bash
python adk_agent.py --task news --count 3
```

#### Full Comprehensive Report
```bash
python adk_agent.py --task full --lang javascript --city London
```

**Example Output:**
```
================================================================================
📊 COMPREHENSIVE REPORT - 2025-11-07 14:30:45
================================================================================

🌤️  Weather in London, GB:
   Temperature: 12.5°C (feels like 11.0°C)
   Conditions: Light Rain
   Humidity: 78%
   Wind Speed: 4.2 m/s

--------------------------------------------------------------------------------

⭐ Top 3 Trending JavaScript Repositories:

1. facebook/react
   ⭐ 223,456 stars | 🍴 45,678 forks
   📝 A declarative, efficient, and flexible JavaScript library
   🔗 https://github.com/facebook/react

2. vuejs/vue
   ⭐ 207,123 stars | 🍴 33,456 forks
   📝 Progressive JavaScript Framework
   🔗 https://github.com/vuejs/vue

3. vercel/next.js
   ⭐ 123,456 stars | 🍴 26,789 forks
   📝 The React Framework for Production
   🔗 https://github.com/vercel/next.js

--------------------------------------------------------------------------------

📰 Top 3 News Headlines:

1. Major Breakthrough in AI Research Announced
   Source: TechNews Daily
   Scientists unveil new neural architecture achieving unprecedented...
   🔗 https://example.com/news/1

2. Global Climate Summit Reaches Historic Agreement
   Source: World News Network
   Nations commit to ambitious carbon reduction targets...
   🔗 https://example.com/news/2

3. Tech Giants Announce Quantum Computing Partnership
   Source: Innovation Today
   Collaboration aims to accelerate quantum computing accessibility...
   🔗 https://example.com/news/3

--------------------------------------------------------------------------------

🤖 AI-Powered Insights:
Interesting correlation: While London experiences rainy weather perfect 
for indoor coding sessions, the JavaScript ecosystem shows strong growth 
with React and Next.js leading the trends. Meanwhile, global news 
highlights major AI breakthroughs, which aligns with the trending 
machine learning repositories. It's an exciting time for developers 
working at the intersection of web and AI technologies.

================================================================================
```

### CLI Options

```bash
python adk_agent.py [OPTIONS]

Options:
  --task {weather,trends,news,full}  Task to execute (required)
  --city TEXT                        City name for weather (default: Delhi)
  --lang TEXT                        Programming language (default: python)
  --count INT                        Number of items to fetch (default: 5)
  --mcp-url TEXT                     MCP server URL (default: http://localhost:8001)
  --no-ai                           Disable AI insights (works without Google API key)
  -h, --help                        Show help message
```

---

## 📚 API Documentation

### MCP Server Endpoints

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8001/docs
- **Alternative Docs**: http://localhost:8001/redoc

### Endpoint Details

#### 1. Weather Tool

```bash
POST http://localhost:8001/tool/get_weather
Content-Type: application/json

{
  "city": "Delhi"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "city": "Delhi",
    "country": "IN",
    "temperature": 28.5,
    "feels_like": 29.0,
    "description": "haze",
    "humidity": 62,
    "wind_speed": 2.5,
    "pressure": 1012,
    "mock": false
  },
  "error": null,
  "timestamp": "2025-11-07T14:30:45.123456"
}
```

#### 2. GitHub Trends Tool

```bash
POST http://localhost:8001/tool/github_trends
Content-Type: application/json

{
  "language": "python",
  "count": 3
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "tensorflow",
      "full_name": "tensorflow/tensorflow",
      "description": "An Open Source Machine Learning Framework for Everyone",
      "stars": 185234,
      "forks": 74123,
      "language": "Python",
      "url": "https://github.com/tensorflow/tensorflow",
      "owner": "tensorflow",
      "created_at": "2015-11-07T01:19:20Z",
      "updated_at": "2025-11-07T10:15:30Z",
      "mock": false
    }
  ],
  "error": null,
  "timestamp": "2025-11-07T14:30:45.123456"
}
```

#### 3. News Tool

```bash
POST http://localhost:8001/tool/get_news
Content-Type: application/json

{
  "count": 3,
  "query": null
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "title": "Major Breakthrough in AI Research",
      "description": "Scientists unveil new architecture...",
      "source": "TechNews Daily",
      "author": "John Doe",
      "published_at": "2025-11-07T12:00:00Z",
      "url": "https://example.com/news/1",
      "mock": false
    }
  ],
  "error": null,
  "timestamp": "2025-11-07T14:30:45.123456"
}
```

#### Health Check

```bash
GET http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T14:30:45.123456",
  "api_keys_configured": {
    "github": true,
    "openweather": true,
    "news": false
  }
}
```

---

## 🧪 Testing

### Manual Testing Script

Create `test_all.sh`:

```bash
#!/bin/bash

echo "🧪 Testing MCP Server + ADK Agent"
echo "=================================="

# Test 1: Server Health
echo -e "\n1️⃣  Testing server health..."
curl -s http://localhost:8001/health | python -m json.tool

# Test 2: Weather Tool
echo -e "\n2️⃣  Testing weather tool..."
curl -s -X POST http://localhost:8001/tool/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "Delhi"}' | python -m json.tool

# Test 3: GitHub Trends Tool
echo -e "\n3️⃣  Testing GitHub trends tool..."
curl -s -X POST http://localhost:8001/tool/github_trends \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "count": 3}' | python -m json.tool

# Test 4: News Tool
echo -e "\n4️⃣  Testing news tool..."
curl -s -X POST http://localhost:8001/tool/get_news \
  -H "Content-Type: application/json" \
  -d '{"count": 3}' | python -m json.tool

# Test 5: ADK Agent Weather
echo -e "\n5️⃣  Testing ADK agent (weather)..."
python adk_agent.py --task weather --city "San Francisco"

# Test 6: ADK Agent Trends
echo -e "\n6️⃣  Testing ADK agent (trends)..."
python adk_agent.py --task trends --lang javascript --count 3

# Test 7: ADK Agent Full
echo -e "\n7️⃣  Testing ADK agent (full report)..."
python adk_agent.py --task full --lang python --city Tokyo

echo -e "\n✅ All tests completed!"
```

Run tests:
```bash
chmod +x test_all.sh
./test_all.sh
```

### Testing Without API Keys

The system gracefully handles missing API keys by using mock data:

```bash
# Test with mock data (unset API keys)
unset GITHUB_TOKEN
unset OPENWEATHER_API_KEY
unset NEWS_API_KEY

# Start server - will use mock data
uvicorn mcp_server:app --reload --port 8001

# Run agent - will still work
python adk_agent.py --task full --lang python --city Delhi --no-ai
```

---

## 📁 Project Structure

```
agenticorch-assignment/
├── mcp_server.py          # MCP server with 3 tools (500+ lines)
│   ├── FastAPI application
│   ├── Weather tool (OpenWeather API)
│   ├── GitHub trends tool (GitHub API)
│   ├── News tool (NewsAPI)
│   ├── Pydantic models for validation
│   ├── Error handling & logging
│   └── Mock data fallback
│
├── adk_agent.py           # ADK agent implementation (600+ lines)
│   ├── MCPClient class
│   ├── ADKAgent class with Gemini integration
│   ├── Task execution methods
│   ├── Response formatting
│   ├── CLI argument parser
│   └── AI-powered insights
│
├── requirements.txt       # Python dependencies
│   ├── fastapi
│   ├── uvicorn
│   ├── requests
│   ├── google-generativeai
│   └── pydantic
│
└── README.md             # This file (comprehensive documentation)
```

---

## 🧠 Key Learnings & Design Decisions

### 1. **MCP Protocol Understanding**

The Model Context Protocol provides a standardized way for AI agents to discover and use tools. Key insights:

- **Standardized Interface**: All tools expose a consistent request/response format
- **Type Safety**: Pydantic models ensure valid inputs/outputs
- **Discoverability**: Tools are self-documenting via FastAPI's auto-generated docs
- **Extensibility**: New tools can be added without changing agent code

### 2. **ADK Integration**

Google's ADK excels at:

- **Natural Language Understanding**: Gemini interprets user intent
- **Context Management**: Maintains conversation state and context
- **Response Generation**: Creates human-friendly outputs from structured data
- **Tool Orchestration**: Intelligently decides when to use which tools

### 3. **Architecture Decisions**

**Why FastAPI for MCP Server?**
- Auto-generated OpenAPI docs
- Native async support
- Type validation with Pydantic
- Production-ready performance

**Why Separate Server/Agent?**
- **Modularity**: MCP server can serve multiple agents
- **Scalability**: Server and agent can scale independently
- **Development**: Can test tools without running agent
- **Deployment**: Different deployment strategies for each component

**Why HTTP over gRPC?**
- Simpler debugging with curl/Postman
- Better documentation with Swagger UI
- Easier firewall traversal
- More accessible for developers

### 4. **Error Handling Strategy**

Implemented comprehensive error handling:
- **API Failures**: Retry logic with exponential backoff (implicit in requests)
- **Missing Keys**: Graceful degradation to mock data
- **Network Issues**: Timeout configuration and clear error messages
- **Validation Errors**: Pydantic catches bad inputs before API calls

### 5. **Mock Data Design**

Mock data serves multiple purposes:
- **Development**: Work without API keys
- **Testing**: Consistent test data
- **Demos**: Show functionality without rate limits
- **Resilience**: System works even when APIs are down

### 6. **Logging Philosophy**

Structured logging at every level:
- **INFO**: Normal operations (tool calls, responses)
- **ERROR**: Failures and exceptions
- **DEBUG**: Detailed execution flow (can be enabled)
- Timestamps on all logs for debugging

### 7. **AI Integration Patterns**

Used Gemini for:
- **Contextual Insights**: Weather-based recommendations
- **Trend Analysis**: Why repos are trending
- **News Summarization**: Key themes across headlines
- **Cross-domain Synthesis**: Connecting weather + code + news

---

## 🔍 How ADK-MCP Connection Works

### Flow Diagram

```
User Input → ADK Agent → MCP Client → HTTP Request → MCP Server → External API
                ↑                                          ↓
                ↑                                          ↓
                ↑                                     API Response
                ↑                                          ↓
                ↑                                    Format & Validate
                ↑                                          ↓
                ↑_______← HTTP Response ←______________ Return
                          (JSON)
```

### Step-by-Step Execution

1. **User Issues Command**
   ```bash
   python adk_agent.py --task weather --city Delhi
   ```

2. **Agent Parses Intent**
   - ADKAgent identifies task type
   - Extracts parameters (city=Delhi)

3. **MCP Client Prepares Request**
   ```python
   mcp_client.get_weather("Delhi")
   # Becomes:
   POST http://localhost:8001/tool/get_weather
   {"city": "Delhi"}
   ```

4. **MCP Server Receives Request**
   - FastAPI validates request with Pydantic
   - Routes to appropriate tool handler
   - `fetch_weather_data("Delhi")` is called

5. **External API Call**
   ```python
   requests.get(
       "http://api.openweathermap.org/data/2.5/weather",
       params={"q": "Delhi", "appid": OPENWEATHER_API_KEY}
   )
   ```

6. **Response Processing**
   - MCP server formats API response
   - Returns standardized JSON
   - Includes success/error status

7. **Agent Formats for Human**
   - ADKAgent receives structured data
   - Formats with emojis and formatting
   - Optionally adds AI insights via Gemini

8. **User Sees Final Output**
   ```
   🌤️  Weather in Delhi, IN:
   Temperature: 28.5°C
   ...
   ```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. MCP Server Won't Start

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8001
lsof -ti:8001 | xargs kill -9

# Or use a different port
uvicorn mcp_server:app --port 8002
python adk_agent.py --mcp-url http://localhost:8002 --task weather --city Delhi
```

#### 2. API Key Errors

**Error:** `401 Unauthorized`

**Solution:**
```bash
# Verify keys are set
echo $GITHUB_TOKEN
echo $OPENWEATHER_API_KEY

# Re-export if empty
export GITHUB_TOKEN="your_token_here"
```

#### 3. Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use uv
uv pip install -r requirements.txt
```

#### 4. Google API Key Missing

**Error:** `Agent will work in basic mode`

**Solution:**
```bash
# Get API key from: https://makersuite.google.com/app/apikey
export GOOGLE_API_KEY="your_key_here"

# Or run without AI features
python adk_agent.py --task weather --city Delhi --no-ai
```

#### 5. Connection Refused

**Error:** `Connection refused to localhost:8001`

**Solution:**
```bash
# 1. Check if server is running
curl http://localhost:8001/health

# 2. If not, start server
uvicorn mcp_server:app --reload --port 8001

# 3. Wait for startup message
# "Uvicorn running on http://0.0.0.0:8001"
```

### Debugging Tips

**Enable Debug Logging:**
```python
# In mcp_server.py or adk_agent.py
logging.basicConfig(level=logging.DEBUG)
```

**Test Individual Components:**
```bash
# Test server only
curl -X POST http://localhost:8001/tool/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "Delhi"}'

# Test agent with mock server
python adk_agent.py --task weather --city Delhi --no-ai
```

**Check Logs:**
```bash
# Server logs show all requests
# Agent logs show all tool calls
# Look for ERROR level messages
```

---

## 📊 Performance Considerations

- **API Rate Limits**:
  - GitHub: 5000 requests/hour (authenticated)
  - OpenWeather: 60 requests/minute (free tier)
  - NewsAPI: 100 requests/day (developer tier)

- **Timeouts**: All API calls have 10-15 second timeouts

- **Caching**: Consider adding Redis for repeated queries (future enhancement)

- **Async Operations**: FastAPI supports async for better concurrency

---

## 🚀 Future Enhancements

1. **Caching Layer**: Add Redis for frequently requested data
2. **Rate Limiting**: Implement proper rate limiting on MCP server
3. **Authentication**: Add API key auth for MCP server
4. **Monitoring**: Prometheus metrics and Grafana dashboards
5. **Database**: Store tool call history and results
6. **More Tools**: Stock prices, cryptocurrency, maps, etc.
7. **Batch Operations**: Support multiple cities/languages in one call
8. **WebSocket Support**: Real-time updates for long-running tasks
9. **Docker**: Containerize for easier deployment
10. **CI/CD**: GitHub Actions for automated testing

---

## 📝 Testing Results Summary

### ✅ Successful Test Cases

1. **Weather Tool**
   - ✅ Valid city (Delhi, London, Tokyo)
   - ✅ City with spaces (San Francisco)
   - ✅ Non-English city names (München)
   - ✅ Mock data when API key missing

2. **GitHub Trends Tool**
   - ✅ Popular languages (Python, JavaScript, Java)
   - ✅ Niche languages (Rust, Go, TypeScript)
   - ✅ Various count parameters (1-20)
   - ✅ Mock data fallback

3. **News Tool**
   - ✅ Top headlines without query
   - ✅ Searched news with query
   - ✅ Various count parameters
   - ✅ Mock data when key missing

4. **ADK Agent Tasks**
   - ✅ Individual tasks (weather, trends, news)
   - ✅ Full comprehensive report
   - ✅ AI insights generation
   - ✅ Operation without Google API key

5. **Error Handling**
   - ✅ Invalid city names
   - ✅ Server not running
   - ✅ Network timeouts
   - ✅ Invalid API keys

---

## 👨‍💻 Author

**Aman Kumar**

- Project: AgenticOrch Take-Home Assignment
- Date: November 2025
- Technologies: Python, FastAPI, Google ADK, MCP

---

## 📄 License

This project is provided as-is for the AgenticOrch take-home assignment.

---

## 🙏 Acknowledgments

- Google for the Agent Development Kit and Gemini API
- FastAPI for the excellent web framework
- OpenWeather, GitHub, and NewsAPI for public APIs
- The open-source community for inspiration

---

## 📞 Support

For questions or issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review server logs for error messages
3. Verify all API keys are correctly set
4. Test each component independently

---

**Happy Coding! 🚀**

