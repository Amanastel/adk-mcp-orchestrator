# Quick Start Guide - FastMCP Implementation

Get up and running with the ADK + FastMCP integration in 5 minutes!

## 🎯 What is Different with FastMCP?

**Important**: With FastMCP, there's **NO separate server to run**! The ADK agent imports and calls MCP tools directly.

```
Traditional MCP:  Agent → HTTP → MCP Server → Tools
FastMCP:         Agent → Direct Import → Tools
```

---

## Prerequisites

```bash
# Check Python version (must be 3.10+)
python3 --version

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Create Virtual Environment with uv

```bash
cd agenticorch-assignment

# Create venv with uv (FAST!)
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies with uv

```bash
# Install all packages including fastmcp (super fast with uv!)
uv pip install -r requirements.txt

# Verify fastmcp is installed
python3 -c "import fastmcp; print('✅ FastMCP installed!')"
```

### Step 3: Set Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
# The file already has your keys if you're the project owner
```

Your `.env` should contain:
```bash
GITHUB_TOKEN=your_github_token
OPENWEATHER_API_KEY=your_openweather_key
# Optional:
NEWS_API_KEY=your_news_key
GOOGLE_API_KEY=your_google_key
```

---

## ✅ You're Ready! Run the Agent

**No server to start!** Just run the agent directly:

```bash
# Test 1: Check MCP server info
python3 adk_agent.py --task info --no-ai
```

**Expected Output:**
```
🔍 Initializing FastMCP client...
✅ FastMCP client initialized

📋 MCP Server Information:
   Name: Weather, GitHub & News Tools Server
   Version: 1.0.0
   Tools: get_weather, github_trends, get_news, server_info
   Status: running

🔑 API Keys Configured:
   ✅ github
   ✅ openweather
   ❌ news
```

---

## 📝 Example Commands

### 1. Weather Task
```bash
python3 adk_agent.py --task weather --city Delhi --no-ai
```

**Output:**
```
🌤️  Weather in Delhi, IN:
   Temperature: 25.34°C (feels like 24.37°C)
   Conditions: Clear Sky
   Humidity: 17%
   Wind Speed: 2.59 m/s
```

### 2. GitHub Trends Task
```bash
python3 adk_agent.py --task trends --lang python --count 3 --no-ai
```

**Output:**
```
⭐ Top 3 Trending Python Repositories:

1. public-apis/public-apis
   ⭐ 376,423 stars | 🍴 39,815 forks
   📝 A collective list of free APIs
   🔗 https://github.com/public-apis/public-apis
```

### 3. News Task
```bash
python3 adk_agent.py --task news --count 3 --no-ai
```

### 4. Full Comprehensive Report
```bash
python3 adk_agent.py --task full --lang javascript --city London --no-ai
```

**Output:**
```
================================================================================
📊 COMPREHENSIVE REPORT - 2025-11-07 20:39:19
================================================================================

🌤️  Weather in London, GB:
   Temperature: 14.72°C (feels like 14.39°C)
   ...

⭐ Top 5 Trending JavaScript Repositories:
   ...

📰 Top 3 News Headlines:
   ...
================================================================================
```

---

## 🎓 Understanding FastMCP

### How It Works

1. **MCP Server (`mcp_server.py`)**:
   ```python
   from fastmcp import FastMCP
   
   mcp = FastMCP("Server Name")
   
   @mcp.tool()
   def get_weather(city: str) -> dict:
       # Tool implementation
   ```

2. **ADK Agent (`adk_agent.py`)**:
   ```python
   # Import the mcp_server module
   import mcp_server
   
   # Get the tool (decorated with @mcp.tool())
   tool = getattr(mcp_server, "get_weather")
   
   # Access underlying function
   result = tool.fn(city="Delhi")
   ```

### Key Differences from Traditional MCP

| Aspect | Traditional MCP | FastMCP (This Project) |
|--------|----------------|------------------------|
| Server Process | Separate HTTP server | No separate server |
| Communication | HTTP/REST | Direct Python import |
| Tool Registration | Manual | `@mcp.tool()` decorator |
| Latency | Network overhead | Direct function call |
| Setup | Start server first | Just run agent |

---

## 🔧 CLI Options Reference

```bash
python3 adk_agent.py [OPTIONS]

Required:
  --task {weather,trends,news,full,info}  Task to execute

Optional:
  --city TEXT           City for weather (default: Delhi)
  --lang TEXT          Language for GitHub (default: python)
  --count INT          Number of items (default: 5)
  --no-ai             Disable AI insights
  -h, --help          Show help
```

---

## 🎯 Common Use Cases

### For Developers
```bash
# Find trending repos in your language
python3 adk_agent.py --task trends --lang rust --count 10 --no-ai

# Get full report for your city
python3 adk_agent.py --task full --lang go --city "San Francisco" --no-ai
```

### For Testing
```bash
# Test each MCP tool individually
python3 adk_agent.py --task info --no-ai
python3 adk_agent.py --task weather --city Tokyo --no-ai
python3 adk_agent.py --task trends --lang typescript --count 3 --no-ai
```

### With AI Insights (if you have Google API key)
```bash
# Set your Google API key
export GOOGLE_API_KEY="your_key"

# Run without --no-ai flag for AI insights
python3 adk_agent.py --task weather --city Delhi
python3 adk_agent.py --task full --lang python --city Paris
```

---

## 🐛 Troubleshooting

### Import Error: No module named 'fastmcp'

```bash
# Make sure you're in the venv
source .venv/bin/activate

# Reinstall fastmcp
uv pip install fastmcp

# Or reinstall everything
uv pip install -r requirements.txt
```

### ModuleNotFoundError: No module named 'mcp_server'

```bash
# Make sure you're in the project directory
cd agenticorch-assignment

# Run the agent from the project root
python3 adk_agent.py --task info --no-ai
```

### API Key Errors

```bash
# Check if .env file exists
cat .env

# Check if variables are loaded
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GitHub:', bool(os.getenv('GITHUB_TOKEN')))"

# Re-export manually if needed
export GITHUB_TOKEN="your_token"
export OPENWEATHER_API_KEY="your_key"
```

### Tool Execution Errors

```bash
# Check if all MCP tools are accessible
python3 -c "from mcp_server import get_weather, github_trends, get_news, server_info; print('✅ All tools imported successfully')"
```

---

## 📊 Verify Installation

Run this complete verification:

```bash
# 1. Check Python version
python3 --version  # Should be 3.10+

# 2. Activate venv
source .venv/bin/activate

# 3. Check fastmcp
python3 -c "import fastmcp; print('FastMCP version:', fastmcp.__version__)"

# 4. Check environment
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Env loaded')"

# 5. Test MCP tools
python3 adk_agent.py --task info --no-ai

# 6. Test full flow
python3 adk_agent.py --task weather --city Delhi --no-ai
```

If all commands work, you're ready to go! ✅

---

## 🚀 Next Steps

1. **Try different tasks**: Experiment with weather, trends, news, and full reports
2. **Change parameters**: Try different cities, languages, and counts
3. **Add Google API key**: Get AI-powered insights with Gemini
4. **Explore the code**: Look at `mcp_server.py` to see FastMCP decorators
5. **Read README.md**: For comprehensive documentation

---

## 📚 Quick Reference

### Essential Commands
```bash
# Setup
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt

# Run
python3 adk_agent.py --task info --no-ai
python3 adk_agent.py --task weather --city Delhi --no-ai
python3 adk_agent.py --task full --lang python --city London --no-ai
```

### File Structure
```
agenticorch-assignment/
├── mcp_server.py       # FastMCP tools (decorated with @mcp.tool())
├── adk_agent.py        # ADK agent (imports MCP tools directly)
├── requirements.txt    # Dependencies (includes fastmcp)
├── .env               # Your API keys (not in git)
└── .env.example       # Template
```

---

**That's it! With FastMCP, setup is simple and fast.** 🚀

**Key Takeaway**: No separate server process needed. The agent imports and calls MCP tools directly!
