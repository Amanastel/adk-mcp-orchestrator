#!/bin/bash

# Test Script for MCP Server
# ==========================
# Tests all MCP server endpoints

echo "🧪 Testing MCP Server Endpoints"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test server health
echo -e "${YELLOW}Test 1: Server Health Check${NC}"
echo "GET http://localhost:8001/health"
echo ""
response=$(curl -s -w "\n%{http_code}" http://localhost:8001/health)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

# Test weather tool
echo -e "${YELLOW}Test 2: Weather Tool (Delhi)${NC}"
echo "POST http://localhost:8001/tool/get_weather"
echo '{"city": "Delhi"}'
echo ""
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/tool/get_weather \
    -H "Content-Type: application/json" \
    -d '{"city": "Delhi"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

# Test GitHub trends tool
echo -e "${YELLOW}Test 3: GitHub Trends Tool (Python)${NC}"
echo "POST http://localhost:8001/tool/github_trends"
echo '{"language": "python", "count": 3}'
echo ""
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/tool/github_trends \
    -H "Content-Type: application/json" \
    -d '{"language": "python", "count": 3}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

# Test news tool
echo -e "${YELLOW}Test 4: News Tool${NC}"
echo "POST http://localhost:8001/tool/get_news"
echo '{"count": 3}'
echo ""
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/tool/get_news \
    -H "Content-Type: application/json" \
    -d '{"count": 3}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

# Test with different city
echo -e "${YELLOW}Test 5: Weather Tool (San Francisco)${NC}"
echo "POST http://localhost:8001/tool/get_weather"
echo '{"city": "San Francisco"}'
echo ""
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/tool/get_weather \
    -H "Content-Type: application/json" \
    -d '{"city": "San Francisco"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

# Test with different language
echo -e "${YELLOW}Test 6: GitHub Trends Tool (JavaScript)${NC}"
echo "POST http://localhost:8001/tool/github_trends"
echo '{"language": "javascript", "count": 5}'
echo ""
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/tool/github_trends \
    -H "Content-Type: application/json" \
    -d '{"language": "javascript", "count": 5}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Success (HTTP $http_code)${NC}"
    echo "$body" | python3 -m json.tool
else
    echo -e "${RED}❌ Failed (HTTP $http_code)${NC}"
    echo "$body"
fi
echo ""
echo "----------------------------------------"
echo ""

echo -e "${GREEN}✅ All endpoint tests completed!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review the responses above"
echo "  2. Check server logs for any errors"
echo "  3. Test the ADK agent with: python adk_agent.py --help"

