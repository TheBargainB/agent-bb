"""This module provides specialized tools for grocery shopping research and deal hunting.

It includes optimized tools for store-specific searches, promotion hunting, product comparison,
and news updates, all following Tavily API best practices for maximum relevance and performance.

These tools are designed specifically for grocery shopping assistants with regional awareness,
store preferences, and time-sensitive deal detection.
"""

import re
import asyncio
from typing import Callable, Optional, cast, Any, Dict, List
from datetime import datetime

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

# Store domain mappings by country/region
STORE_DOMAINS = {
    "US": ["walmart.com", "target.com", "kroger.com", "safeway.com", "costco.com", "wholefoods.com"],
    "UK": ["tesco.com", "sainsburys.co.uk", "asda.com", "aldi.co.uk", "lidl.co.uk", "morrisons.com"],
    "DE": ["rewe.de", "edeka.de", "aldi.de", "lidl.de", "kaufland.de", "bio-company.de"],
    "NL": ["ah.nl", "jumbo.com", "lidl.nl", "dirk.nl", "hoogevliet.com", "plus.nl"],
    "FR": ["carrefour.fr", "leclerc.fr", "auchan.fr", "monoprix.fr", "franprix.fr"],
}

# News domains for grocery/retail industry
NEWS_DOMAINS = ["reuters.com", "bloomberg.com", "cnbc.com", "retaildive.com", "progressivegrocer.com"]

def validate_query(query: str) -> str:
    """Validate and optimize query according to Tavily best practices."""
    if len(query) > 400:
        raise ValueError("Query is too long. Max query length is 400 characters.")
    
    # Remove excessive whitespace and normalize
    query = re.sub(r'\s+', ' ', query.strip())
    return query

def get_user_store_domains(user_config: Dict[str, Any]) -> List[str]:
    """Extract relevant store domains based on user configuration."""
    country_code = user_config.get("country_code", "US")
    store_websites = user_config.get("store_websites", "")
    
    # Get country-specific domains
    domains = STORE_DOMAINS.get(country_code, STORE_DOMAINS["US"])
    
    # Add user-specified store websites
    if store_websites:
        custom_domains = [domain.strip() for domain in store_websites.split(",")]
        domains.extend(custom_domains)
    
    return list(set(domains))  # Remove duplicates

def optimize_grocery_query(query: str, search_type: str = "general") -> str:
    """Optimize query for grocery shopping searches."""
    query = validate_query(query)
    
    # Add context keywords based on search type
    if search_type == "promotions":
        if not any(word in query.lower() for word in ["deal", "promotion", "discount", "offer", "sale"]):
            query = f"deals promotions {query}"
    elif search_type == "products":
        if not any(word in query.lower() for word in ["product", "price", "buy", "grocery"]):
            query = f"grocery products {query}"
    elif search_type == "news":
        query = f"latest news {query}"
    
    return query

@tool
async def store_specific_search(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Search for products and deals specifically within user's preferred stores.
    
    This tool focuses searches on the user's preferred stores and regional domains
    for maximum relevance to their shopping options.
    
    Args:
        query: Search query (max 400 characters)
        user_config: User configuration with store preferences and country
    """
    try:
        query = optimize_grocery_query(query, "products")
        store_domains = get_user_store_domains(user_config or {})
        
        # Focus search on user's store domains
        wrapped = TavilySearchResults(
            max_results=8,
            search_depth="advanced",
            include_domains=store_domains[:5],  # Limit to top 5 domains for efficiency
            include_raw_content=True,
            chunks_per_source=2
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        # Post-process results for grocery relevance
        filtered_results = []
        for item in result:
            score = item.get("score", 0)
            if score > 0.3:  # Filter low-relevance results
                filtered_results.append(item)
        
        return cast(List[Dict[str, Any]], filtered_results)
        
    except Exception as e:
        print(f"Store search failed: {e}")
        # Fallback to basic search
        return await basic_research_tool(query, user_config)

@tool
async def promotion_hunter(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Hunt for current deals, promotions, and discounts at grocery stores.
    
    Optimized for finding time-sensitive deals with recent publication dates
    and discount-focused content.
    
    Args:
        query: Search query for promotions (max 400 characters)
        user_config: User configuration with store preferences
    """
    try:
        query = optimize_grocery_query(query, "promotions")
        store_domains = get_user_store_domains(user_config or {})
        
        wrapped = TavilySearchResults(
            max_results=10,
            search_depth="advanced",
            include_domains=store_domains,
            time_range="week",  # Focus on recent deals
            include_raw_content=True,
            chunks_per_source=3
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        # Enhanced post-processing for promotions
        promotion_results = []
        for item in result:
            content = item.get("content", "").lower()
            title = item.get("title", "").lower()
            
            # Score boost for promotion-related content
            promotion_keywords = ["sale", "deal", "discount", "offer", "coupon", "promo", "%", "off"]
            keyword_matches = sum(1 for keyword in promotion_keywords if keyword in content or keyword in title)
            
            if keyword_matches > 0:
                item["promotion_score"] = keyword_matches
                promotion_results.append(item)
        
        # Sort by promotion relevance
        promotion_results.sort(key=lambda x: x.get("promotion_score", 0), reverse=True)
        
        return cast(List[Dict[str, Any]], promotion_results[:8])
        
    except Exception as e:
        print(f"Promotion search failed: {e}")
        return None

@tool
async def product_comparison_search(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Compare products and prices across multiple grocery stores.
    
    Searches across various store domains to help users compare prices
    and product availability.
    
    Args:
        query: Product search query (max 400 characters)
        user_config: User configuration with regional preferences
    """
    try:
        query = optimize_grocery_query(f"price compare {query}", "products")
        store_domains = get_user_store_domains(user_config or {})
        
        wrapped = TavilySearchResults(
            max_results=12,
            search_depth="advanced",
            include_domains=store_domains,
            include_raw_content=False,  # Faster for price comparisons
            chunks_per_source=1
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        # Filter for price-relevant content
        price_results = []
        for item in result:
            content = item.get("content", "").lower()
            title = item.get("title", "").lower()
            
            # Look for price indicators
            price_patterns = [r'\$\d+', r'£\d+', r'€\d+', r'\d+\.\d{2}', 'price', 'cost']
            has_price_info = any(re.search(pattern, content + title) for pattern in price_patterns)
            
            if has_price_info or item.get("score", 0) > 0.4:
                price_results.append(item)
        
        return cast(List[Dict[str, Any]], price_results)
        
    except Exception as e:
        print(f"Product comparison search failed: {e}")
        return None

@tool
async def grocery_news_search(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Search for latest grocery industry news, store announcements, and new products.
    
    Focuses on recent news from retail industry sources and store websites
    for the most current information.
    
    Args:
        query: News search query (max 400 characters)
        user_config: User configuration for regional relevance
    """
    try:
        query = optimize_grocery_query(query, "news")
        store_domains = get_user_store_domains(user_config or {})
        all_domains = store_domains + NEWS_DOMAINS
        
        wrapped = TavilySearchResults(
            max_results=8,
            search_depth="advanced",
            topic="news",
            days=7,  # Last week's news
            include_domains=all_domains,
            include_raw_content=False
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        # Sort by publication date (most recent first)
        sorted_results = sorted(
            result,
            key=lambda x: x.get("published_date", ""),
            reverse=True
        )
        
        return cast(List[Dict[str, Any]], sorted_results)
        
    except Exception as e:
        print(f"News search failed: {e}")
        return None

@tool
async def regional_deals_search(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Search for region-specific deals and local store promotions.
    
    Optimized for finding location-based deals and regional store chains
    relevant to the user's area.
    
    Args:
        query: Regional deals search query (max 400 characters)
        user_config: User configuration with country and regional preferences
    """
    try:
        country_code = user_config.get("country_code", "US") if user_config else "US"
        query = optimize_grocery_query(f"{country_code} local {query}", "promotions")
        
        # Use country-specific domain filtering
        country_domains = [f"*.{country_code.lower()}", f"*.co.{country_code.lower()}"]
        if country_code == "US":
            country_domains = ["*.com"]
        elif country_code == "UK":
            country_domains = ["*.co.uk", "*.uk"]
        elif country_code == "DE":
            country_domains = ["*.de"]
        elif country_code == "NL":
            country_domains = ["*.nl"]
        
        wrapped = TavilySearchResults(
            max_results=10,
            search_depth="advanced",
            include_domains=country_domains,
            time_range="week",
            include_raw_content=True,
            chunks_per_source=2
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        return cast(List[Dict[str, Any]], result)
        
    except Exception as e:
        print(f"Regional deals search failed: {e}")
        return None

@tool
async def advanced_research_tool(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Perform comprehensive research with advanced search parameters.
    
    High-quality, in-depth search for complex queries requiring detailed analysis.
    Uses user configuration for regional and language preferences.
    
    Args:
        query: Research query (max 400 characters)
        user_config: User configuration for personalized results
    """
    try:
        query = validate_query(query)
        
        # Get user-specific store domains if available
        store_domains = get_user_store_domains(user_config or {})
        
        # Optimize query based on user preferences
        country_code = user_config.get("country_code", "US") if user_config else "US"
        language_code = user_config.get("language_code", "en") if user_config else "en"
        
        # Add regional context to query if not already present
        if country_code and country_code not in query.lower():
            query = f"{country_code} {query}"
        
        wrapped = TavilySearchResults(
            max_results=10,
            search_depth="advanced",
            include_raw_content=True,
            chunks_per_source=3,
            include_domains=store_domains if store_domains else None
        )
        
        result = await wrapped.ainvoke({"query": query})
        
        # Filter by relevance score
        high_quality_results = [
            item for item in result 
            if item.get("score", 0) > 0.4
        ]
        
        return cast(List[Dict[str, Any]], high_quality_results)
        
    except Exception as e:
        print(f"Advanced research failed: {e}")
        return None

@tool
async def basic_research_tool(query: str, user_config: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    """Quick research for simple queries with fast response times.
    
    Optimized for speed with basic search depth and fewer results.
    Uses user configuration for regional preferences.
    
    Args:
        query: Research query (max 400 characters)
        user_config: User configuration for personalized results
    """
    try:
        query = validate_query(query)
        
        # Get user-specific store domains if available
        store_domains = get_user_store_domains(user_config or {})
        
        # Optimize query based on user preferences
        country_code = user_config.get("country_code", "US") if user_config else "US"
        
        # Add regional context to query if not already present
        if country_code and country_code not in query.lower():
            query = f"{country_code} {query}"
        
        wrapped = TavilySearchResults(
            max_results=5,
            search_depth="basic",
            include_raw_content=False,
            include_images=True,
            include_domains=store_domains if store_domains else None
        )
        
        result = await wrapped.ainvoke({"query": query})
        return cast(List[Dict[str, Any]], result)
        
    except Exception as e:
        print(f"Basic research failed: {e}")
        return []

@tool
async def get_todays_date() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

@tool
async def multi_angle_research(query: str, user_config: Dict[str, Any] = None) -> Optional[Dict[str, List[Dict[str, Any]]]]:
    """Perform comprehensive multi-angle research combining multiple search strategies.
    
    Runs store-specific, promotion, and comparison searches concurrently
    for comprehensive coverage of the topic.
    
    Args:
        query: Research query (max 400 characters)
        user_config: User configuration for personalized results
    """
    try:
        query = validate_query(query)
        
        # Run multiple searches concurrently
        tasks = [
            store_specific_search(query, user_config),
            promotion_hunter(query, user_config),
            product_comparison_search(query, user_config)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results by search type
        organized_results = {
            "store_results": results[0] if not isinstance(results[0], Exception) else [],
            "promotions": results[1] if not isinstance(results[1], Exception) else [],
            "comparisons": results[2] if not isinstance(results[2], Exception) else []
        }
        
        return organized_results
        
    except Exception as e:
        print(f"Multi-angle research failed: {e}")
        return None


def get_tools(selected_tools: List[str]) -> List[Callable[..., Any]]:
    """Convert a list of tool names to actual tool functions."""
    tool_mapping = {
        "store_specific_search": store_specific_search,
        "promotion_hunter": promotion_hunter,
        "product_comparison_search": product_comparison_search,
        "grocery_news_search": grocery_news_search,
        "regional_deals_search": regional_deals_search,
        "advanced_research_tool": advanced_research_tool,
        "basic_research_tool": basic_research_tool,
        "get_todays_date": get_todays_date,
        "multi_angle_research": multi_angle_research
    }
    
    tools = []
    for tool_name in selected_tools:
        if tool_name in tool_mapping:
            tools.append(tool_mapping[tool_name])
        else:
            print(f"Warning: Tool '{tool_name}' not found in tool mapping")
    
    return tools 