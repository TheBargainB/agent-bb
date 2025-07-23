"""
Phase 3: Sophisticated Memory Intelligence - Advanced learning, insights, and proactive recommendations.
Only used in supervisor, not in tools.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from langgraph.store.base import BaseStore
from pydantic import BaseModel, Field
import asyncio
import json
from collections import defaultdict, Counter


# Enhanced Memory Schemas for Phase 3
class UserPreferences(BaseModel):
    """Structured user preferences with rich data types and confidence scoring."""
    # Dietary & Health
    dietary_restrictions: List[str] = Field(default_factory=list, description="Dietary restrictions like vegan, gluten-free")
    health_goals: List[str] = Field(default_factory=list, description="Health goals like low-sodium, high-protein")
    allergies: List[str] = Field(default_factory=list, description="Food allergies")
    
    # Shopping Preferences
    budget_ranges: Dict[str, str] = Field(default_factory=dict, description="Price sensitivity by category")
    preferred_stores: List[str] = Field(default_factory=list, description="Preferred store chains")
    preferred_brands: List[str] = Field(default_factory=list, description="Favorite brands")
    
    # Quality & Sourcing
    quality_preferences: List[str] = Field(default_factory=list, description="organic, grass-fed, non-GMO, etc.")
    sourcing_preferences: List[str] = Field(default_factory=list, description="local, farm-fresh, sustainable")
    
    # Behavioral Patterns
    shopping_frequency: Dict[str, int] = Field(default_factory=dict, description="How often they buy categories")
    seasonal_patterns: Dict[str, List[str]] = Field(default_factory=dict, description="Seasonal preferences")
    time_patterns: Dict[str, List[str]] = Field(default_factory=dict, description="Time-based patterns")
    
    # Phase 3: Intelligence Metrics
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence in each preference")
    interaction_count: int = Field(default=0, description="Total interactions")
    last_updated: datetime = Field(default_factory=datetime.now)
    successful_recommendations: int = Field(default=0, description="Count of successful proactive recommendations")


class MemoryInsight(BaseModel):
    """Generated insights from memory analysis."""
    insight_type: str = Field(description="Type of insight: pattern, recommendation, prediction")
    confidence: float = Field(description="Confidence score 0-1")
    description: str = Field(description="Human readable insight")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    actionable_recommendation: Optional[str] = Field(default=None, description="Specific action to take")
    temporal_context: Optional[str] = Field(default=None, description="Time-based context")


class ShoppingPattern(BaseModel):
    """Enhanced shopping pattern with intelligence."""
    query_type: str = Field(description="Type of search pattern")
    frequency: int = Field(default=1, description="How often this pattern occurs")
    success_rate: float = Field(default=1.0, description="Success rate of this pattern")
    last_used: datetime = Field(default_factory=datetime.now)
    seasonal_relevance: List[str] = Field(default_factory=list, description="Seasons when relevant")
    time_relevance: List[str] = Field(default_factory=list, description="Times when relevant")
    related_patterns: List[str] = Field(default_factory=list, description="Related search patterns")


# Phase 3: Advanced Memory Operations

async def get_sophisticated_user_memory(store: BaseStore, user_id: str) -> Tuple[UserPreferences, List[MemoryInsight]]:
    """Get enhanced user memory with generated insights."""
    try:
        # Get existing preferences - fix store API call
        prefs_item = await store.aget(("user_preferences",), user_id)
        prefs = UserPreferences(**prefs_item.value) if prefs_item else UserPreferences()
        
        # Generate insights from memory
        insights = await generate_memory_insights(store, prefs, user_id)
        
        print(f"🧠 Phase 3: Loaded sophisticated memory with {len(insights)} insights")
        return prefs, insights
        
    except Exception as e:
        print(f"⚠️ Memory read error: {e}")
        return UserPreferences(), []


async def generate_memory_insights(store: BaseStore, prefs: UserPreferences, user_id: str) -> List[MemoryInsight]:
    """Phase 3: Generate sophisticated insights from user memory."""
    insights = []
    
    try:
        # Pattern Analysis Insight
        if prefs.interaction_count >= 3:
            pattern_insight = await analyze_shopping_patterns(store, user_id)
            if pattern_insight:
                insights.append(pattern_insight)
        
        # Proactive Recommendation Insight
        if prefs.dietary_restrictions or prefs.preferred_stores:
            recommendation_insight = await generate_proactive_recommendations(prefs)
            if recommendation_insight:
                insights.append(recommendation_insight)
        
        # Temporal Insight
        temporal_insight = await analyze_temporal_patterns(store, user_id)
        if temporal_insight:
            insights.append(temporal_insight)
        
        # Budget Optimization Insight
        if prefs.budget_ranges:
            budget_insight = await analyze_budget_patterns(prefs)
            if budget_insight:
                insights.append(budget_insight)
        
        print(f"🔍 Generated {len(insights)} sophisticated insights")
        
    except Exception as e:
        print(f"⚠️ Insight generation error: {e}")
    
    return insights


async def analyze_shopping_patterns(store: BaseStore, user_id: str) -> Optional[MemoryInsight]:
    """Analyze cross-interaction patterns for insights."""
    try:
        # Get recent shopping patterns
        recent_patterns = []
        for i in range(5):  # Check last 5 patterns
            pattern_item = await store.aget(("shopping_pattern",), f"{user_id}_{i}")
            if pattern_item:
                recent_patterns.append(ShoppingPattern(**pattern_item.value))
        
        if len(recent_patterns) >= 2:
            # Analyze for cross-domain patterns
            categories = [p.query_type for p in recent_patterns]
            if len(set(categories)) >= 2:
                return MemoryInsight(
                    insight_type="pattern",
                    confidence=0.8,
                    description=f"Cross-category shopping pattern detected: {', '.join(set(categories))}",
                    evidence=[f"Recent searches: {', '.join(categories)}"],
                    actionable_recommendation="Consider bundling related items in future recommendations"
                )
                
    except Exception as e:
        print(f"⚠️ Pattern analysis error: {e}")
    
    return None


async def generate_proactive_recommendations(prefs: UserPreferences) -> Optional[MemoryInsight]:
    """Generate proactive recommendations based on learned preferences."""
    try:
        recommendations = []
        
        # Dietary-based recommendations
        if "gluten-free" in prefs.dietary_restrictions:
            recommendations.append("Consider suggesting gluten-free alternatives automatically")
        
        if "organic" in prefs.quality_preferences:
            recommendations.append("Prioritize organic options in search results")
        
        # Store-based recommendations
        if prefs.preferred_stores:
            top_store = max(prefs.preferred_stores, key=prefs.preferred_stores.count) if prefs.preferred_stores else None
            if top_store:
                recommendations.append(f"Focus searches on {top_store} for better personalization")
        
        if recommendations:
            return MemoryInsight(
                insight_type="recommendation",
                confidence=0.9,
                description="Proactive recommendation opportunities identified",
                evidence=recommendations,
                actionable_recommendation="Implement proactive filtering and suggestions"
            )
            
    except Exception as e:
        print(f"⚠️ Recommendation generation error: {e}")
    
    return None


async def analyze_temporal_patterns(store: BaseStore, user_id: str) -> Optional[MemoryInsight]:
    """Analyze time-based shopping patterns."""
    try:
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime("%A")
        
        # Simple temporal analysis
        time_context = ""
        if 6 <= current_hour <= 10:
            time_context = "morning breakfast planning"
        elif 11 <= current_hour <= 14:
            time_context = "lunch preparation"  
        elif 15 <= current_hour <= 19:
            time_context = "dinner planning"
        elif 20 <= current_hour <= 23:
            time_context = "next-day meal prep"
        
        if time_context:
            return MemoryInsight(
                insight_type="prediction",
                confidence=0.7,
                description=f"Temporal pattern: User shopping during {time_context} time",
                evidence=[f"Current time: {current_hour}:00 on {current_day}"],
                temporal_context=time_context,
                actionable_recommendation=f"Tailor recommendations for {time_context}"
            )
            
    except Exception as e:
        print(f"⚠️ Temporal analysis error: {e}")
    
    return None


async def analyze_budget_patterns(prefs: UserPreferences) -> Optional[MemoryInsight]:
    """Analyze budget consciousness patterns."""
    try:
        budget_keywords = []
        for category, sensitivity in prefs.budget_ranges.items():
            if "affordable" in sensitivity.lower() or "cheap" in sensitivity.lower():
                budget_keywords.append(category)
        
        if budget_keywords:
            return MemoryInsight(
                insight_type="pattern",
                confidence=0.85,
                description=f"Budget-conscious pattern in categories: {', '.join(budget_keywords)}",
                evidence=[f"Budget sensitivity in {len(budget_keywords)} categories"],
                actionable_recommendation="Prioritize value options and highlight cost savings"
            )
            
    except Exception as e:
        print(f"⚠️ Budget analysis error: {e}")
    
    return None


async def build_sophisticated_memory_context(prefs: UserPreferences, insights: List[MemoryInsight], user_query: str) -> str:
    """Build Phase 3 enhanced context with insights and predictions."""
    
    context_parts = []
    
    # Core preferences
    if prefs.dietary_restrictions:
        context_parts.append(f"DIETARY: {', '.join(prefs.dietary_restrictions)}")
    
    if prefs.quality_preferences:
        context_parts.append(f"QUALITY: {', '.join(prefs.quality_preferences)}")
    
    if prefs.preferred_stores:
        stores = list(set(prefs.preferred_stores))[:3]  # Top 3 unique stores
        context_parts.append(f"STORES: {', '.join(stores)}")
    
    if prefs.budget_ranges:
        budget_items = [f"{k}:{v}" for k, v in list(prefs.budget_ranges.items())[:2]]
        context_parts.append(f"BUDGET: {', '.join(budget_items)}")
    
    # Phase 3: Add insights
    if insights:
        high_confidence_insights = [i for i in insights if i.confidence >= 0.8]
        if high_confidence_insights:
            insight_summaries = []
            for insight in high_confidence_insights[:2]:  # Top 2 insights
                insight_summaries.append(f"{insight.insight_type}: {insight.description}")
            context_parts.append(f"INSIGHTS: {' | '.join(insight_summaries)}")
    
    # Interaction history
    if prefs.interaction_count > 0:
        context_parts.append(f"HISTORY: {prefs.interaction_count} interactions")
    
    base_context = " | ".join(context_parts)
    
    # Phase 3: Add predictive recommendations
    predictive_context = ""
    for insight in insights:
        if insight.actionable_recommendation and insight.confidence >= 0.8:
            predictive_context += f"\n🎯 PROACTIVE: {insight.actionable_recommendation}"
        if insight.temporal_context:
            predictive_context += f"\n⏰ TIMING: {insight.temporal_context}"
    
    full_context = base_context + predictive_context
    
    print(f"📝 Sophisticated context built: {len(full_context)} chars with {len(insights)} insights")
    return full_context


async def sophisticated_learning_from_interaction(store: BaseStore, user_query: str, supervisor_response: str, config: dict, insights: List[MemoryInsight]) -> None:
    """Phase 3: Advanced learning with insight validation and cross-domain patterns."""
    
    user_id = config.get("user_id", "default_user")
    
    try:
        print("🎓 Starting Phase 3 sophisticated learning...")
        
        # Get current preferences - fix store API call
        prefs_item = await store.aget(("user_preferences",), user_id)
        prefs = UserPreferences(**prefs_item.value) if prefs_item else UserPreferences()
        
        # Advanced learning patterns
        await advanced_dietary_learning(prefs, user_query)
        await advanced_quality_learning(prefs, user_query)
        await advanced_temporal_learning(prefs, user_query)
        await cross_domain_learning(store, prefs, user_query, user_id)
        await validate_and_correct_memory(prefs, insights)
        
        # Update confidence scores
        await update_confidence_scores(prefs, user_query, supervisor_response)
        
        # Update interaction metrics
        prefs.interaction_count += 1
        prefs.last_updated = datetime.now()
        
        # Save enhanced preferences - fix store API call
        await store.aput(("user_preferences",), user_id, prefs.dict())
        print(f"💾 Saved sophisticated preferences: {prefs.interaction_count} interactions")
        
        # Save advanced shopping pattern
        await save_advanced_shopping_pattern(store, user_query, user_id, prefs)
        
        print(f"✅ Sophisticated learning completed: {len(prefs.dietary_restrictions)} dietary, {len(prefs.preferred_stores)} stores")
        
    except Exception as e:
        print(f"⚠️ Sophisticated learning error: {e}")


async def advanced_dietary_learning(prefs: UserPreferences, user_query: str) -> None:
    """Learn advanced dietary patterns with confidence scoring."""
    query_lower = user_query.lower()
    
    # Advanced dietary detection
    dietary_patterns = {
        "gluten-free": ["gluten-free", "gluten free", "celiac"],
        "vegan": ["vegan", "plant-based", "no animal products"],
        "vegetarian": ["vegetarian", "veggie", "no meat"],
        "keto": ["keto", "ketogenic", "low-carb", "low carb"],
        "paleo": ["paleo", "paleolithic", "caveman diet"],
        "dairy-free": ["dairy-free", "dairy free", "lactose-free", "no dairy"]
    }
    
    for restriction, keywords in dietary_patterns.items():
        if any(keyword in query_lower for keyword in keywords):
            if restriction not in prefs.dietary_restrictions:
                prefs.dietary_restrictions.append(restriction)
                prefs.confidence_scores[f"dietary_{restriction}"] = 0.8
            else:
                # Increase confidence with repeated mentions
                current_confidence = prefs.confidence_scores.get(f"dietary_{restriction}", 0.8)
                prefs.confidence_scores[f"dietary_{restriction}"] = min(0.95, current_confidence + 0.1)


async def advanced_quality_learning(prefs: UserPreferences, user_query: str) -> None:
    """Learn quality preferences with nuanced understanding."""
    query_lower = user_query.lower()
    
    quality_patterns = {
        "organic": ["organic", "pesticide-free", "chemical-free"],
        "grass-fed": ["grass-fed", "grass fed", "pasture-raised"],
        "non-gmo": ["non-gmo", "non gmo", "gmo-free"],
        "free-range": ["free-range", "free range", "cage-free"],
        "sustainable": ["sustainable", "eco-friendly", "environmentally friendly"],
        "local": ["local", "locally sourced", "farm-fresh", "farmers market"]
    }
    
    for quality, keywords in quality_patterns.items():
        if any(keyword in query_lower for keyword in keywords):
            if quality not in prefs.quality_preferences:
                prefs.quality_preferences.append(quality)
                prefs.confidence_scores[f"quality_{quality}"] = 0.75
            else:
                current_confidence = prefs.confidence_scores.get(f"quality_{quality}", 0.75)
                prefs.confidence_scores[f"quality_{quality}"] = min(0.9, current_confidence + 0.1)


async def advanced_temporal_learning(prefs: UserPreferences, user_query: str) -> None:
    """Learn time-based patterns."""
    current_hour = datetime.now().hour
    current_day = datetime.now().strftime("%A").lower()
    
    # Categorize by time
    time_category = ""
    if 6 <= current_hour <= 10:
        time_category = "morning"
    elif 11 <= current_hour <= 14:
        time_category = "midday"
    elif 15 <= current_hour <= 19:
        time_category = "evening"
    elif 20 <= current_hour <= 23:
        time_category = "night"
    
    if time_category:
        if time_category not in prefs.time_patterns:
            prefs.time_patterns[time_category] = []
        
        # Extract product category from query
        query_lower = user_query.lower()
        if "bread" in query_lower or "pasta" in query_lower:
            prefs.time_patterns[time_category].append("carbohydrates")
        elif "milk" in query_lower or "cheese" in query_lower:
            prefs.time_patterns[time_category].append("dairy")


async def cross_domain_learning(store: BaseStore, prefs: UserPreferences, user_query: str, user_id: str) -> None:
    """Learn patterns that apply across different product categories."""
    query_lower = user_query.lower()
    
    # If user mentions budget in one category, apply to related categories
    if any(word in query_lower for word in ["affordable", "cheap", "budget", "inexpensive"]):
        category = "general"
        if "bread" in query_lower or "pasta" in query_lower:
            category = "carbohydrates"
        elif "milk" in query_lower or "dairy" in query_lower:
            category = "dairy"
        
        if category not in prefs.budget_ranges:
            prefs.budget_ranges[category] = "budget-conscious"
        
        # Cross-domain application: if budget-conscious in one category, likely in others
        if len(prefs.budget_ranges) >= 2:
            prefs.budget_ranges["general"] = "budget-conscious"


async def validate_and_correct_memory(prefs: UserPreferences, insights: List[MemoryInsight]) -> None:
    """Validate memory against insights and correct inconsistencies."""
    
    # Check for conflicting dietary restrictions
    conflicts = []
    if "vegan" in prefs.dietary_restrictions and "vegetarian" in prefs.dietary_restrictions:
        prefs.dietary_restrictions.remove("vegetarian")  # Vegan is more specific
        conflicts.append("Resolved vegan/vegetarian conflict")
    
    # Validate confidence scores
    for key, confidence in prefs.confidence_scores.items():
        if confidence > 1.0:
            prefs.confidence_scores[key] = 1.0
        elif confidence < 0.0:
            prefs.confidence_scores[key] = 0.0
    
    if conflicts:
        print(f"🔧 Memory validation: {', '.join(conflicts)}")


async def update_confidence_scores(prefs: UserPreferences, user_query: str, supervisor_response: str) -> None:
    """Update confidence scores based on interaction success."""
    
    # If the supervisor response seems successful (contains product info), boost confidence
    if any(word in supervisor_response.lower() for word in ["found", "here are", "available", "options"]):
        # Boost confidence for dietary restrictions mentioned in this query
        query_lower = user_query.lower()
        for restriction in prefs.dietary_restrictions:
            if restriction.replace("-", " ") in query_lower:
                current_confidence = prefs.confidence_scores.get(f"dietary_{restriction}", 0.8)
                prefs.confidence_scores[f"dietary_{restriction}"] = min(0.95, current_confidence + 0.05)


async def save_advanced_shopping_pattern(store: BaseStore, user_query: str, user_id: str, prefs: UserPreferences) -> None:
    """Save enhanced shopping patterns with intelligence metrics."""
    
    query_lower = user_query.lower()
    
    # Determine pattern type with more sophistication
    pattern_type = "general_search"
    if any(word in query_lower for word in ["bread", "pasta", "rice"]):
        pattern_type = "carbohydrate_search"
    elif any(word in query_lower for word in ["milk", "cheese", "yogurt"]):
        pattern_type = "dairy_search"
    elif "organic" in query_lower:
        pattern_type = "organic_search"
    elif any(word in query_lower for word in ["affordable", "cheap", "budget"]):
        pattern_type = "budget_search"
    
    # Create sophisticated pattern
    current_time = datetime.now()
    pattern = ShoppingPattern(
        query_type=pattern_type,
        frequency=1,
        success_rate=1.0,  # Assume success for now
        last_used=current_time,
        seasonal_relevance=[current_time.strftime("%B").lower()],  # Current month
        time_relevance=[f"{current_time.hour}:00"],
        related_patterns=[]
    )
    
    # Save pattern - fix store API call
    pattern_key = f"{user_id}_{prefs.interaction_count}"
    await store.aput(("shopping_pattern",), pattern_key, pattern.dict())
    print(f"🔍 Saved sophisticated pattern: {pattern_type}")


# Legacy function aliases for backward compatibility
async def get_user_memory(store: BaseStore, user_id: str) -> dict:
    """Legacy wrapper for backward compatibility."""
    prefs, _ = await get_sophisticated_user_memory(store, user_id)
    return prefs.dict()


async def save_user_memory(store: BaseStore, preferences: dict, user_id: str) -> None:
    """Legacy wrapper for backward compatibility."""
    await store.aput(("user_preferences",), user_id, preferences)


async def build_memory_context(user_prefs: dict) -> str:
    """Legacy wrapper for backward compatibility."""
    prefs = UserPreferences(**user_prefs)
    return await build_sophisticated_memory_context(prefs, [], "")


async def learn_from_interaction(store: BaseStore, user_query: str, supervisor_response: str, config: dict) -> None:
    """Legacy wrapper for backward compatibility."""
    await sophisticated_learning_from_interaction(store, user_query, supervisor_response, config, [])


async def add_search_pattern(store: BaseStore, query: str, results_summary: str) -> None:
    """Legacy wrapper - now handled by sophisticated learning."""
    pass 