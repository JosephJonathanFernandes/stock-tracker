import requests
import streamlit as st

SERPAPI_KEY = "83a797dd6b54afb51050fbe8a91b922c9de4c514e744e5b700dc0eb33465b3b4" 

def fetch_news(query):
    """
    Fetches news using SerpAPI. Returns a list of dictionaries.
    """

    params = {
        "engine": "google_news",
        "q": f"{query} stock news",
        "gl": "in",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        results = response.json()
        
        news_items = []
        if "news_results" in results:
            for item in results["news_results"][:5]: # Top 5 news
                news_items.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "source": item.get("source"),
                    "date": item.get("date"),
                    "snippet": item.get("snippet"),
                    "thumbnail": item.get("thumbnail")
                })
        return news_items
    except Exception as e:
        st.warning(f"Failed to fetch news: {e}")
        return get_mock_news(query)

def get_mock_news(stock_name):
    """Returns mock news data for demonstration."""
    return [
        {
            "title": f"{stock_name} reports strong Q3 earnings",
            "link": "#",
            "source": "Financial Times",
            "date": "2 hours ago",
            "snippet": f"{stock_name} has exceeded market expectations with a 15% rise in net profit...",
            "thumbnail": "https://via.placeholder.com/100"
        },
        {
            "title": f"Market analysis: Is {stock_name} a buy right now?",
            "link": "#",
            "source": "Bloomberg",
            "date": "5 hours ago",
            "snippet": "Analysts are divided on the short-term outlook, but long-term fundamentals remain strong...",
            "thumbnail": "https://via.placeholder.com/100"
        },
        {
            "title": f"{stock_name} announces new strategic partnership",
            "link": "#",
            "source": "Reuters",
            "date": "1 day ago",
            "snippet": "The company has entered into a joint venture to expand its footprint in the renewable energy sector...",
            "thumbnail": "https://via.placeholder.com/100"
        }
    ]