#!/bin/bash

# AgenticOrch Assignment - Automated Setup Script
# ================================================
# This script automates the entire setup process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AgenticOrch Assignment - Setup Script                 ║"
echo "║   ADK + MCP Integration                                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Check Python version
echo -e "${YELLOW}Step 1: Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.10"

if (( $(echo "$python_version >= $required_version" | bc -l) )); then
    echo -e "${GREEN}✅ Python $python_version detected (>= $required_version)${NC}"
else
    echo -e "${RED}❌ Python $python_version is too old. Please install Python 3.10 or higher.${NC}"
    exit 1
fi
echo ""

# Step 2: Check pip
echo -e "${YELLOW}Step 2: Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 is installed${NC}"
else
    echo -e "${RED}❌ pip3 is not installed. Please install pip3.${NC}"
    exit 1
fi
echo ""

# Step 3: Install dependencies
echo -e "${YELLOW}Step 3: Installing dependencies...${NC}"
echo "This may take a minute..."
pip3 install -q fastapi uvicorn requests pydantic google-generativeai python-dotenv httpx typing-extensions pydantic-settings

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Step 4: Set environment variables
echo -e "${YELLOW}Step 4: Setting up environment variables...${NC}"

# Check if API keys are already set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  GITHUB_TOKEN not set. Setting provided token...${NC}"
    export GITHUB_TOKEN="your_github_personal_access_token"
else
    echo -e "${GREEN}✅ GITHUB_TOKEN already set${NC}"
fi

if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  OPENWEATHER_API_KEY not set. Setting provided key...${NC}"
    export OPENWEATHER_API_KEY="your_openweather_api_key"
else
    echo -e "${GREEN}✅ OPENWEATHER_API_KEY already set${NC}"
fi

if [ -z "$NEWS_API_KEY" ]; then
    echo -e "${YELLOW}ℹ️  NEWS_API_KEY not set. Will use mock data.${NC}"
else
    echo -e "${GREEN}✅ NEWS_API_KEY is set${NC}"
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${YELLOW}ℹ️  GOOGLE_API_KEY not set. AI features will be disabled.${NC}"
else
    echo -e "${GREEN}✅ GOOGLE_API_KEY is set${NC}"
fi
echo ""

# Step 5: Create .env file
echo -e "${YELLOW}Step 5: Creating .env file...${NC}"
cat > .env << EOF
# Required API Keys
GITHUB_TOKEN=${GITHUB_TOKEN}
OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}

# Optional API Keys
# NEWS_API_KEY=your_news_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here
EOF
echo -e "${GREEN}✅ .env file created${NC}"
echo ""

# Step 6: Verify files
echo -e "${YELLOW}Step 6: Verifying project files...${NC}"
required_files=("mcp_server.py" "adk_agent.py" "requirements.txt" "README.md")
all_present=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file (missing)${NC}"
        all_present=false
    fi
done

if [ "$all_present" = false ]; then
    echo -e "${RED}Some required files are missing!${NC}"
    exit 1
fi
echo ""

# Step 7: Test MCP Server startup
echo -e "${YELLOW}Step 7: Testing MCP server startup...${NC}"
echo "Starting server in background..."
python3 -m uvicorn mcp_server:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &
server_pid=$!
echo "Server PID: $server_pid"

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Test health endpoint
echo "Testing health endpoint..."
health_response=$(curl -s http://localhost:8001/health || echo "failed")

if [[ $health_response == *"healthy"* ]]; then
    echo -e "${GREEN}✅ MCP server is running and healthy${NC}"
else
    echo -e "${RED}❌ MCP server health check failed${NC}"
    echo "Check server.log for details"
    exit 1
fi
echo ""

# Step 8: Test ADK Agent
echo -e "${YELLOW}Step 8: Testing ADK agent...${NC}"
echo "Running weather task for Delhi..."
python3 adk_agent.py --task weather --city Delhi --no-ai > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ADK agent works correctly${NC}"
else
    echo -e "${RED}❌ ADK agent test failed${NC}"
    exit 1
fi
echo ""

# Success!
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          🎉 SETUP COMPLETED SUCCESSFULLY! 🎉             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}📋 Quick Reference:${NC}"
echo ""
echo "MCP Server (already running in background):"
echo "  URL: http://localhost:8001"
echo "  Docs: http://localhost:8001/docs"
echo "  Health: http://localhost:8001/health"
echo "  PID: $server_pid"
echo ""
echo "To stop the server:"
echo "  kill $server_pid"
echo ""
echo "ADK Agent Usage:"
echo "  python3 adk_agent.py --task weather --city Delhi --no-ai"
echo "  python3 adk_agent.py --task trends --lang python --count 3 --no-ai"
echo "  python3 adk_agent.py --task full --lang javascript --city London --no-ai"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "  README.md - Comprehensive documentation"
echo "  QUICKSTART.md - Quick start guide"
echo "  TEST_RESULTS.md - Test results"
echo "  PROJECT_OVERVIEW.md - Project overview"
echo ""
echo -e "${GREEN}Ready to use! Try running some commands above.${NC}"
echo ""

