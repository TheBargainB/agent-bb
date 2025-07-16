"""
Memory collection tools for learning user preferences from conversations.
Phase 2: Collect insights without changing routing behavior.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from langchain_core.tools import tool
from langgraph.store.memory import InMemoryStore

from assistants_agent.memory.schemas import GroceryProfile, MemoryUpdate


class ProfileInsight(BaseModel):
    """Container for a discovered user insight"""
    category: str = Field(description="Category: store_insights, product_preferences, shopping_patterns, contextual_insights")
    key: str = Field(description="Specific key within category")
    value: Any = Field(description="The learned insight")
    confidence: float = Field(default=0.7, description="Confidence in this insight (0.0-1.0)")
    source: str = Field(description="How this insight was discovered")


def extract_insights_from_conversation(user_query: str, user_config: Dict[str, Any], agent_responses: List[str]) -> List[ProfileInsight]:
    """
    Extract semantic insights from user conversation that go beyond static config.
    Phase 2: Collection only, no routing changes.
    """
    insights = []
    
    # Analyze user query for behavioral patterns
    query_lower = user_query.lower()
    
    # Store preference insights (beyond basic store_preference in config)
    if any(store in query_lower for store in ['target', 'walmart', 'costco', 'whole foods']):
        for store in ['target', 'walmart', 'costco', 'whole foods']:
            if store in query_lower:
                insights.append(ProfileInsight(
                    category="store_insights",
                    key=f"{store}_familiarity",
                    value="mentioned_specifically",
                    confidence=0.8,
                    source="explicit_mention_in_query"
                ))
    
    # Product preference insights (beyond dietary restrictions)
    if any(brand in query_lower for brand in ['organic', 'brand name', 'premium', 'store brand']):
        if 'organic' in query_lower:
            insights.append(ProfileInsight(
                category="product_preferences",
                key="organic_preference",
                value="frequently_requests",
                confidence=0.9,
                source="repeated_organic_requests"
            ))
    
    # Shopping pattern insights
    if any(term in query_lower for term in ['bulk', 'family size', 'weekly', 'monthly']):
        if 'bulk' in query_lower or 'family size' in query_lower:
            insights.append(ProfileInsight(
                category="shopping_patterns",
                key="quantity_preference",
                value="bulk_buyer",
                confidence=0.8,
                source="bulk_quantity_requests"
            ))
    
    # Contextual insights (situation-specific preferences)
    if any(term in query_lower for term in ['quick', 'fast', 'urgent', 'tonight']):
        insights.append(ProfileInsight(
            category="contextual_insights",
            key="time_sensitivity",
            value="values_convenience",
            confidence=0.7,
            source="urgency_indicators"
        ))
    
    # Price sensitivity insights
    if any(term in query_lower for term in ['cheap', 'budget', 'deal', 'sale', 'discount']):
        insights.append(ProfileInsight(
            category="contextual_insights", 
            key="price_sensitivity",
            value="deal_focused",
            confidence=0.8,
            source="price_focused_language"
        ))
    
    return insights


@tool
def collect_semantic_memory(
    user_id: str,
    user_query: str, 
    user_config: Dict[str, Any],
    agent_responses: List[str],
    memory_store: InMemoryStore
) -> str:
    """
    Tool to collect semantic memory from conversation without affecting routing.
    Phase 2: Collection only - insights stored but not used for decisions.
    """
    try:
        # Extract insights from this conversation
        insights = extract_insights_from_conversation(user_query, user_config, agent_responses)
        
        if not insights:
            return "No new semantic insights detected in this conversation"
        
        # Retrieve existing profile or create new one
        try:
            existing_item = memory_store.get(("grocery_profiles", user_id), "profile")
            if existing_item:
                profile = GroceryProfile(**existing_item.value)
            else:
                profile = GroceryProfile(user_id=user_id)
        except:
            profile = GroceryProfile(user_id=user_id)
        
        # Update profile with new insights
        insights_added = 0
        for insight in insights:
            category = getattr(profile, insight.category, {})
            if not category:
                category = {}
            
            # Only add if we don't already have this insight or if confidence is higher
            existing_insight = category.get(insight.key)
            if not existing_insight or insight.confidence > existing_insight.get('confidence', 0):
                category[insight.key] = {
                    'value': insight.value,
                    'confidence': insight.confidence,
                    'source': insight.source,
                    'last_updated': datetime.now().isoformat()
                }
                setattr(profile, insight.category, category)
                insights_added += 1
        
        # Update timestamp
        profile.last_updated = datetime.now()
        
        # Store updated profile
        memory_store.put(("grocery_profiles", user_id), "profile", profile.model_dump())
        
        return f"✅ Semantic memory updated: {insights_added} new insights collected (Phase 2: collection only)"
        
    except Exception as e:
        return f"❌ Error collecting semantic memory: {str(e)}"


@tool 
def get_memory_summary(user_id: str, memory_store: InMemoryStore) -> str:
    """
    Tool to display collected memory for transparency.
    Phase 2: Show what system has learned about user.
    """
    try:
        profile_item = memory_store.get(("grocery_profiles", user_id), "profile")
        if not profile_item:
            return "No semantic memory collected yet for this user"
        
        profile = GroceryProfile(**profile_item.value)
        
        summary = f"🧠 Learned User Insights (Phase 2 - Collection Only):\n\n"
        
        total_insights = 0
        for category in ['store_insights', 'product_preferences', 'shopping_patterns', 'contextual_insights']:
            category_data = getattr(profile, category, {})
            if category_data:
                summary += f"📊 {category.replace('_', ' ').title()}:\n"
                for key, data in category_data.items():
                    summary += f"  • {key}: {data['value']} (confidence: {data['confidence']:.1f})\n"
                    total_insights += 1
                summary += "\n"
        
        if total_insights == 0:
            return "No specific insights collected yet - system is learning from conversations"
        
        summary += f"Total insights: {total_insights} | Last updated: {profile.last_updated}\n"
        summary += "Note: These insights supplement your configuration but don't change routing yet (Phase 2)"
        
        return summary
        
    except Exception as e:
        return f"❌ Error retrieving memory summary: {str(e)}"


# Tool list for supervisor integration
MEMORY_COLLECTION_TOOLS = [collect_semantic_memory, get_memory_summary] 