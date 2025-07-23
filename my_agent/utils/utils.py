"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from langgraph.store.base import BaseStore


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(model, model_provider=provider)


# Memory utility functions (following tutorial pattern)
async def get_user_memory(store: BaseStore, user_id: str) -> dict:
    """Get user memory preferences (tutorial pattern with memory enhancement)."""
    try:
        prefs_item = await store.aget(("user_preferences",), user_id)
        return prefs_item.value if prefs_item else {}
    except Exception as e:
        print(f"⚠️ Memory read error: {e}")
        return {}


async def save_user_memory(store: BaseStore, preferences: dict, user_id: str) -> None:
    """Save user memory preferences (tutorial pattern)."""
    try:
        await store.aput(("user_preferences",), user_id, preferences)
        print(f"💾 Saved user preferences for {user_id}")
    except Exception as e:
        print(f"⚠️ Memory save error: {e}")


def build_memory_context(user_prefs: dict, configurable: dict) -> str:
    """Build memory context string (tutorial pattern - simple and clean)."""
    if not user_prefs:
        return ""
    
    context_parts = []
    
    # Extract preferences
    dietary = user_prefs.get("dietary_restrictions", [])
    if dietary:
        context_parts.append(f"DIETARY: {', '.join(dietary)}")
    
    stores = user_prefs.get("preferred_stores", [])
    if stores:
        context_parts.append(f"STORES: {', '.join(stores[:2])}")  # Top 2
    
    quality = user_prefs.get("quality_preferences", [])
    if quality:
        context_parts.append(f"QUALITY: {', '.join(quality[:2])}")  # Top 2
    
    # Add runtime config
    country = configurable.get("country_code", "US")
    language = configurable.get("language_code", "en")
    store_pref = configurable.get("store_preference", "any")
    
    context_parts.append(f"CONFIG: {country}/{language}/{store_pref}")
    
    return " | ".join(context_parts)


async def learn_from_interaction(store: BaseStore, user_query: str, response: str, config: dict) -> None:
    """Learn from user interaction (tutorial pattern - simple learning)."""
    user_id = config.get("user_id", "default_user")
    
    try:
        # Get current preferences
        user_prefs = await get_user_memory(store, user_id)
        
        # Simple learning patterns
        query_lower = user_query.lower()
        
        # Learn dietary restrictions
        if "dietary_restrictions" not in user_prefs:
            user_prefs["dietary_restrictions"] = []
        
        dietary_keywords = {
            "vegan": ["vegan", "plant-based"],
            "vegetarian": ["vegetarian", "veggie"],
            "gluten-free": ["gluten-free", "gluten free", "celiac"],
            "organic": ["organic", "pesticide-free"]
        }
        
        for restriction, keywords in dietary_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if restriction not in user_prefs["dietary_restrictions"]:
                    user_prefs["dietary_restrictions"].append(restriction)
        
        # Learn store preferences
        if "preferred_stores" not in user_prefs:
            user_prefs["preferred_stores"] = []
        
        store_keywords = {
            "albert_heijn": ["albert heijn", "ah"],
            "jumbo": ["jumbo"],
            "walmart": ["walmart"],
            "target": ["target"],
            "whole_foods": ["whole foods", "wholefoods"]
        }
        
        for store, keywords in store_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if store not in user_prefs["preferred_stores"]:
                    user_prefs["preferred_stores"].append(store)
        
        # Learn quality preferences  
        if "quality_preferences" not in user_prefs:
            user_prefs["quality_preferences"] = []
        
        quality_keywords = ["organic", "grass-fed", "free-range", "local", "sustainable"]
        for quality in quality_keywords:
            if quality in query_lower and quality not in user_prefs["quality_preferences"]:
                user_prefs["quality_preferences"].append(quality)
        
        # Update interaction count
        user_prefs["interaction_count"] = user_prefs.get("interaction_count", 0) + 1
        user_prefs["last_updated"] = datetime.now().isoformat()
        
        # Save updated preferences
        await save_user_memory(store, user_prefs, user_id)
        
        print(f"✅ Learning completed: {len(user_prefs.get('dietary_restrictions', []))} dietary, {len(user_prefs.get('preferred_stores', []))} stores")
        
    except Exception as e:
        print(f"⚠️ Learning error: {e}")