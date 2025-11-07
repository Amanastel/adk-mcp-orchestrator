"""
ADK Agent Implementation with Real MCP Integration
==================================================
Google Agent Development Kit (ADK) agent that connects to FastMCP server
and intelligently uses MCP tools.

Usage examples:
    python adk_agent.py --task weather --city Delhi
    python adk_agent.py --task trends --lang python --count 3
    python adk_agent.py --task full --lang javascript --city London
"""

import os
import sys
import argparse
import logging
import subprocess
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MCP Client for FastMCP Server
# ============================================================================

class FastMCPClient:
    """Client for interacting with FastMCP server tools via stdio."""
    
    def __init__(self, server_script: str = "mcp_server.py"):
        """
        Initialize FastMCP client.
        
        Args:
            server_script: Path to the MCP server script
        """
        self.server_script = server_script
        logger.info(f"Initialized FastMCP client with server script: {server_script}")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the FastMCP server by importing the actual function.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool response data
        """
        logger.info(f"Calling FastMCP tool: {tool_name} with args: {arguments}")
        
        try:
            # Import the actual tool function from mcp_server
            # The FastMCP decorators create callable functions that we can use
            import importlib
            import sys
            
            # Make sure current directory is in path
            if '.' not in sys.path:
                sys.path.insert(0, '.')
            
            # Import or reload the mcp_server module
            if 'mcp_server' in sys.modules:
                mcp_server = importlib.reload(sys.modules['mcp_server'])
            else:
                import mcp_server
            
            # Get the tool (it's a FunctionTool object from FastMCP)
            tool = getattr(mcp_server, tool_name)
            
            # FastMCP wraps functions in FunctionTool, access the underlying function
            if hasattr(tool, 'fn'):
                # It's a FastMCP FunctionTool, get the underlying function
                tool_func = tool.fn
            elif hasattr(tool, '__wrapped__'):
                # It might be wrapped differently
                tool_func = tool.__wrapped__
            else:
                # Try to call it directly
                tool_func = tool
            
            # Call the function
            result = tool_func(**arguments)
            
            logger.info(f"Tool {tool_name} executed successfully")
            return result
            
        except AttributeError as e:
            logger.error(f"Tool {tool_name} not found: {str(e)}")
            return {"success": False, "error": f"Tool {tool_name} not found"}
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """Call the get_weather MCP tool."""
        return self.call_tool("get_weather", {"city": city})
    
    def get_github_trends(self, language: str, count: int = 5) -> Dict[str, Any]:
        """Call the github_trends MCP tool."""
        return self.call_tool("github_trends", {"language": language, "count": count})
    
    def get_news(self, count: int = 3, query: Optional[str] = None) -> Dict[str, Any]:
        """Call the get_news MCP tool."""
        args = {"count": count}
        if query:
            args["query"] = query
        return self.call_tool("get_news", args)
    
    def get_server_info(self) -> Dict[str, Any]:
        """Call the server_info MCP tool."""
        return self.call_tool("server_info", {})


# ============================================================================
# ADK Agent
# ============================================================================

class ADKAgent:
    """
    Google ADK Agent that uses FastMCP tools to provide intelligent responses.
    """
    
    def __init__(self, mcp_client: FastMCPClient, google_api_key: Optional[str] = None):
        """
        Initialize ADK agent.
        
        Args:
            mcp_client: FastMCP client instance
            google_api_key: Google API key for Gemini (optional)
        """
        self.mcp_client = mcp_client
        self.google_api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
        
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Initialized ADK agent with Gemini model")
        else:
            self.model = None
            logger.warning("Google API key not found, agent will work in basic mode")
    
    def format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a readable string."""
        if not weather_data.get("success"):
            return f"❌ Error: {weather_data.get('error', 'Unknown error')}"
        
        mock_note = " [Using mock data]" if weather_data.get("mock") else ""
        country = f", {weather_data.get('country', '')}" if weather_data.get('country') else ""
        
        return f"""
🌤️  Weather in {weather_data['city']}{country}{mock_note}:
   Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
   Conditions: {weather_data['description'].title()}
   Humidity: {weather_data['humidity']}%
   Wind Speed: {weather_data['wind_speed']} m/s
"""
    
    def format_github_response(self, github_data: Dict[str, Any]) -> str:
        """Format GitHub trends data into a readable string."""
        if not github_data.get("success"):
            return f"❌ Error: {github_data.get('error', 'Unknown error')}"
        
        repos = github_data.get("repositories", [])
        if not repos:
            return "No repositories found."
        
        mock_note = " [Using mock data]" if github_data.get("mock") else ""
        language = github_data.get("language", "Unknown")
        
        output = f"\n⭐ Top {len(repos)} Trending {language.title()} Repositories{mock_note}:\n\n"
        
        for i, repo in enumerate(repos, 1):
            output += f"{i}. {repo['full_name']}\n"
            output += f"   ⭐ {repo['stars']:,} stars | 🍴 {repo['forks']:,} forks\n"
            output += f"   📝 {repo['description']}\n"
            output += f"   🔗 {repo['url']}\n\n"
        
        return output
    
    def format_news_response(self, news_data: Dict[str, Any]) -> str:
        """Format news data into a readable string."""
        if not news_data.get("success"):
            return f"❌ Error: {news_data.get('error', 'Unknown error')}"
        
        articles = news_data.get("articles", [])
        if not articles:
            return "No news headlines found."
        
        mock_note = " [Using mock data]" if news_data.get("mock") else ""
        
        output = f"\n📰 Top {len(articles)} News Headlines{mock_note}:\n\n"
        
        for i, article in enumerate(articles, 1):
            output += f"{i}. {article['title']}\n"
            output += f"   Source: {article['source']}\n"
            output += f"   {article['description']}\n"
            output += f"   🔗 {article['url']}\n\n"
        
        return output
    
    def execute_weather_task(self, city: str) -> str:
        """Execute weather task using MCP tool."""
        logger.info(f"Executing weather task for city: {city}")
        
        try:
            weather_data = self.mcp_client.get_weather(city)
            response = self.format_weather_response(weather_data)
            
            if self.model and weather_data.get("success"):
                try:
                    prompt = f"""Based on this weather data for {city}:
Temperature: {weather_data['temperature']}°C
Conditions: {weather_data['description']}
Humidity: {weather_data['humidity']}%

Provide a brief, friendly comment about the weather and suggest appropriate clothing or activities."""
                    
                    ai_response = self.model.generate_content(prompt)
                    response += f"\n💡 AI Insight: {ai_response.text}\n"
                except Exception as e:
                    logger.error(f"Error getting AI insight: {str(e)}")
            
            return response
        except Exception as e:
            logger.error(f"Error executing weather task: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def execute_trends_task(self, language: str, count: int = 5) -> str:
        """Execute GitHub trends task using MCP tool."""
        logger.info(f"Executing trends task for language: {language}, count: {count}")
        
        try:
            trends_data = self.mcp_client.get_github_trends(language, count)
            response = self.format_github_response(trends_data)
            
            if self.model and trends_data.get("success"):
                try:
                    repos = trends_data.get("repositories", [])
                    top_repo = repos[0] if repos else None
                    
                    if top_repo:
                        prompt = f"""The top trending {language} repository is:
Name: {top_repo['full_name']}
Stars: {top_repo['stars']}
Description: {top_repo['description']}

Provide a brief insight about why this might be trending and what developers might learn from it."""
                        
                        ai_response = self.model.generate_content(prompt)
                        response += f"\n💡 AI Insight: {ai_response.text}\n"
                except Exception as e:
                    logger.error(f"Error getting AI insight: {str(e)}")
            
            return response
        except Exception as e:
            logger.error(f"Error executing trends task: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def execute_news_task(self, count: int = 3, query: Optional[str] = None) -> str:
        """Execute news task using MCP tool."""
        logger.info(f"Executing news task, count: {count}, query: {query}")
        
        try:
            news_data = self.mcp_client.get_news(count, query)
            response = self.format_news_response(news_data)
            
            if self.model and news_data.get("success"):
                try:
                    articles = news_data.get("articles", [])
                    titles = [a['title'] for a in articles[:3]]
                    
                    prompt = f"""These are the top news headlines:
{chr(10).join(f'- {t}' for t in titles)}

Provide a brief summary of the common themes or key takeaways."""
                    
                    ai_response = self.model.generate_content(prompt)
                    response += f"\n💡 AI Summary: {ai_response.text}\n"
                except Exception as e:
                    logger.error(f"Error getting AI summary: {str(e)}")
            
            return response
        except Exception as e:
            logger.error(f"Error executing news task: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def execute_full_task(self, language: str, city: str, repo_count: int = 3, news_count: int = 3) -> str:
        """Execute comprehensive task combining all MCP tools."""
        logger.info(f"Executing full task: language={language}, city={city}")
        
        output = f"\n{'='*80}\n"
        output += f"📊 COMPREHENSIVE REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"{'='*80}\n"
        
        # Get weather using MCP tool
        try:
            weather_data = self.mcp_client.get_weather(city)
            output += self.format_weather_response(weather_data)
        except Exception as e:
            output += f"\n❌ Weather Error: {str(e)}\n"
        
        output += f"\n{'-'*80}\n"
        
        # Get GitHub trends using MCP tool
        try:
            trends_data = self.mcp_client.get_github_trends(language, repo_count)
            output += self.format_github_response(trends_data)
        except Exception as e:
            output += f"\n❌ GitHub Trends Error: {str(e)}\n"
        
        output += f"\n{'-'*80}\n"
        
        # Get news using MCP tool
        try:
            news_data = self.mcp_client.get_news(news_count)
            output += self.format_news_response(news_data)
        except Exception as e:
            output += f"\n❌ News Error: {str(e)}\n"
        
        # Use Gemini to create an intelligent summary
        if self.model:
            try:
                logger.info("Generating AI-powered comprehensive summary...")
                prompt = f"""Create a brief, insightful summary connecting these three pieces of information:
1. Current weather in {city}
2. Trending {language} repositories on GitHub
3. Top news headlines

Provide 2-3 sentences about interesting connections or insights."""
                
                ai_response = self.model.generate_content(prompt)
                output += f"\n{'-'*80}\n"
                output += f"\n🤖 AI-Powered Insights:\n{ai_response.text}\n"
            except Exception as e:
                logger.error(f"Error generating comprehensive summary: {str(e)}")
        
        output += f"\n{'='*80}\n"
        
        return output


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ADK Agent with FastMCP Tools Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get weather for a city
  python adk_agent.py --task weather --city Delhi
  
  # Get GitHub trending repositories
  python adk_agent.py --task trends --lang python --count 5
  
  # Get news headlines
  python adk_agent.py --task news --count 3
  
  # Comprehensive report combining all tools
  python adk_agent.py --task full --lang javascript --city London
        """
    )
    
    parser.add_argument(
        "--task",
        required=True,
        choices=["weather", "trends", "news", "full", "info"],
        help="Task to execute"
    )
    parser.add_argument(
        "--city",
        default="Delhi",
        help="City name for weather (default: Delhi)"
    )
    parser.add_argument(
        "--lang",
        default="python",
        help="Programming language for GitHub trends (default: python)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of items to fetch (default: 5)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI-powered insights"
    )
    
    args = parser.parse_args()
    
    # Initialize FastMCP client
    print("\n🔍 Initializing FastMCP client...")
    mcp_client = FastMCPClient()
    
    # Check MCP server tools
    print("✅ FastMCP client initialized\n")
    
    # Initialize ADK agent
    google_api_key = None if args.no_ai else os.getenv("GOOGLE_API_KEY")
    agent = ADKAgent(mcp_client, google_api_key)
    
    # Execute task
    try:
        if args.task == "info":
            info = mcp_client.get_server_info()
            print("📋 MCP Server Information:")
            print(f"   Name: {info.get('name')}")
            print(f"   Version: {info.get('version')}")
            print(f"   Tools: {', '.join(info.get('tools', []))}")
            print(f"   Status: {info.get('status')}")
            print(f"\n🔑 API Keys Configured:")
            for key, value in info.get('api_keys_configured', {}).items():
                status = "✅" if value else "❌"
                print(f"   {status} {key}")
        elif args.task == "weather":
            result = agent.execute_weather_task(args.city)
            print(result)
        elif args.task == "trends":
            result = agent.execute_trends_task(args.lang, args.count)
            print(result)
        elif args.task == "news":
            result = agent.execute_news_task(args.count)
            print(result)
        elif args.task == "full":
            result = agent.execute_full_task(
                language=args.lang,
                city=args.city,
                repo_count=min(args.count, 5),
                news_count=3
            )
            print(result)
        
        logger.info("Task completed successfully")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Task interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
