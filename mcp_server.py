"""
MCP Server Implementation using FastMCP
========================================
Proper Model Context Protocol (MCP) server with 3 tools:
1. get_weather - Fetch current weather for a city
2. github_trends - Fetch trending GitHub repositories
3. get_news - Fetch top news headlines

Run with: python mcp_server.py
Or as MCP server: mcp run mcp_server.py
"""

import os
import logging
from typing import Optional
from datetime import datetime

import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Weather, GitHub & News Tools Server")

# Load API keys from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


# ============================================================================
# Tool 1: Weather Tool
# ============================================================================

@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather information for a specified city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Dictionary containing weather information including temperature,
        humidity, wind speed, and weather description
    """
    logger.info(f"Weather tool called for city: {city}")
    
    if not OPENWEATHER_API_KEY:
        logger.warning("OpenWeather API key not found, using mock data")
        return {
            "city": city,
            "temperature": 22.5,
            "feels_like": 21.0,
            "description": "partly cloudy",
            "humidity": 65,
            "wind_speed": 3.5,
            "mock": True,
            "success": True
        }
    
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        result = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            "mock": False,
            "success": True
        }
        logger.info(f"Weather data retrieved successfully for {city}")
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch weather: {str(e)}",
            "city": city
        }


# ============================================================================
# Tool 2: GitHub Trends Tool
# ============================================================================

@mcp.tool()
def github_trends(language: str = "python", count: int = 5) -> dict:
    """
    Fetch trending GitHub repositories by programming language.
    
    Args:
        language: Programming language to filter repositories (default: python)
        count: Number of repositories to return (1-20, default: 5)
        
    Returns:
        Dictionary containing list of trending repositories with stars,
        forks, description, and URLs
    """
    logger.info(f"GitHub trends tool called: language={language}, count={count}")
    
    # Validate count
    count = max(1, min(count, 20))
    
    if not GITHUB_TOKEN:
        logger.warning("GitHub token not found, using mock data")
        return {
            "success": True,
            "language": language,
            "count": count,
            "repositories": [
                {
                    "name": f"awesome-{language}-project-{i}",
                    "full_name": f"user{i}/awesome-{language}-project-{i}",
                    "description": f"An awesome {language} project for demonstration",
                    "stars": 1000 - (i * 100),
                    "forks": 200 - (i * 20),
                    "language": language,
                    "url": f"https://github.com/user{i}/awesome-{language}-project-{i}",
                    "mock": True
                }
                for i in range(1, count + 1)
            ],
            "mock": True
        }
    
    try:
        url = "https://api.github.com/search/repositories"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        params = {
            "q": f"language:{language}",
            "sort": "stars",
            "order": "desc",
            "per_page": count
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        repositories = []
        for repo in data.get("items", [])[:count]:
            repositories.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"] or "No description provided",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "url": repo["html_url"],
                "owner": repo["owner"]["login"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "mock": False
            })
        
        logger.info(f"Retrieved {len(repositories)} trending {language} repositories")
        return {
            "success": True,
            "language": language,
            "count": len(repositories),
            "repositories": repositories,
            "mock": False
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching GitHub trends: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch GitHub trends: {str(e)}",
            "language": language
        }


# ============================================================================
# Tool 3: News Tool
# ============================================================================

@mcp.tool()
def get_news(count: int = 3, query: Optional[str] = None) -> dict:
    """
    Fetch top news headlines.
    
    Args:
        count: Number of news headlines to return (1-10, default: 3)
        query: Optional search query to filter news (default: None for top headlines)
        
    Returns:
        Dictionary containing list of news articles with title, description,
        source, and URLs
    """
    logger.info(f"News tool called: count={count}, query={query}")
    
    # Validate count
    count = max(1, min(count, 10))
    
    if not NEWS_API_KEY:
        logger.warning("NewsAPI key not found, using mock data")
        topics = ["AI", "Climate", "Technology", "Space", "Economy"]
        return {
            "success": True,
            "count": count,
            "query": query,
            "articles": [
                {
                    "title": f"Breaking: Major development in {topics[i % len(topics)]}",
                    "description": f"Latest updates on {topics[i % len(topics)]} that everyone is talking about",
                    "source": f"News Source {i + 1}",
                    "published_at": datetime.utcnow().isoformat(),
                    "url": f"https://example.com/news/{i + 1}",
                    "mock": True
                }
                for i in range(count)
            ],
            "mock": True
        }
    
    try:
        url = "https://newsapi.org/v2/top-headlines" if not query else "https://newsapi.org/v2/everything"
        headers = {"X-Api-Key": NEWS_API_KEY}
        params = {
            "pageSize": count,
            "language": "en"
        }
        
        if query:
            params["q"] = query
        else:
            params["country"] = "us"
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get("articles", [])[:count]:
            articles.append({
                "title": article["title"],
                "description": article["description"] or "No description available",
                "source": article["source"]["name"],
                "author": article.get("author", "Unknown"),
                "published_at": article["publishedAt"],
                "url": article["url"],
                "mock": False
            })
        
        logger.info(f"Retrieved {len(articles)} news headlines")
        return {
            "success": True,
            "count": len(articles),
            "query": query,
            "articles": articles,
            "mock": False
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news headlines: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch news: {str(e)}",
            "query": query
        }


# ============================================================================
# Server Info
# ============================================================================

@mcp.tool()
def server_info() -> dict:
    """
    Get information about the MCP server and configured API keys.
    
    Returns:
        Dictionary with server information and API key configuration status
    """
    return {
        "name": "Weather, GitHub & News Tools Server",
        "version": "1.0.0",
        "tools": ["get_weather", "github_trends", "get_news", "server_info"],
        "api_keys_configured": {
            "github": bool(GITHUB_TOKEN),
            "openweather": bool(OPENWEATHER_API_KEY),
            "news": bool(NEWS_API_KEY)
        },
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting MCP server with FastMCP...")
    logger.info(f"Configured API keys: GitHub={bool(GITHUB_TOKEN)}, OpenWeather={bool(OPENWEATHER_API_KEY)}, News={bool(NEWS_API_KEY)}")
    
    # Run the MCP server
    mcp.run()
