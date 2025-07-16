"""
Memory schemas for grocery shopping assistant.

These schemas capture LEARNED insights that complement the runtime configuration.
Static preferences (dietary restrictions, budget, etc.) remain in UserConfig.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class GroceryProfile(BaseModel):
    """
    Semantic Memory: Learned user insights that go beyond static config.
    Complements UserConfig with discovered preferences and patterns.
    """
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Learned store insights (beyond basic store_preference in config)
    store_insights: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Store-specific learned preferences: layout familiarity, preferred departments, timing patterns"
    )
    
    # Discovered product preferences (beyond basic dietary restrictions)
    product_preferences: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Learned brand preferences, quality expectations, discovered alternatives"
    )
    
    # Shopping behavior patterns
    shopping_patterns: Dict[str, Any] = Field(
        default_factory=dict,
        description="Learned timing preferences, quantity patterns, seasonal behaviors"
    )
    
    # Contextual preferences discovered through conversation
    contextual_insights: Dict[str, Any] = Field(
        default_factory=dict,
        description="Situation-specific preferences: crowd tolerance, price sensitivity variations"
    )
    
    last_updated: datetime = Field(default_factory=datetime.now)


class ShoppingEpisode(BaseModel):
    """
    Episodic Memory: Track specific shopping sessions and agent performance.
    Helps improve routing and response quality over time.
    """
    episode_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Original user query and context
    user_query: str
    user_config: Dict[str, Any]  # Runtime config at time of request
    
    # Agent routing decisions
    routing_decisions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Which agents were called, in what order, and why"
    )
    
    # Tool usage and effectiveness
    tool_usage: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Which tools were used, search queries, result quality"
    )
    
    # Final response and user reaction
    final_response: Optional[str] = None
    user_satisfaction_indicators: Dict[str, Any] = Field(
        default_factory=dict,
        description="Follow-up questions, clarifications, corrections needed"
    )
    
    # Performance metrics
    response_time: Optional[float] = None
    tokens_used: Optional[int] = None
    
    # Success indicators
    task_completed: Optional[bool] = None
    required_clarification: bool = False


class SupervisorInstructions(BaseModel):
    """
    Procedural Memory: Learn optimal routing and response strategies.
    Evolves the supervisor's decision-making based on successful patterns.
    """
    instruction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Routing strategy patterns
    routing_strategies: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Query type -> optimal agent routing patterns learned from episodes"
    )
    
    # Response synthesis patterns
    synthesis_strategies: Dict[str, str] = Field(
        default_factory=dict,
        description="How to best combine multiple agent outputs for different query types"
    )
    
    # Personalization tactics
    personalization_patterns: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="User-specific communication and assistance patterns that work well"
    )
    
    # Performance thresholds and preferences
    quality_thresholds: Dict[str, float] = Field(
        default_factory=dict,
        description="Learned quality standards for different types of responses"
    )
    
    last_updated: datetime = Field(default_factory=datetime.now)
    confidence_score: float = Field(
        default=0.5,
        description="Confidence in these learned strategies (0.0-1.0)"
    )


# Memory collection helpers
class MemoryUpdate(BaseModel):
    """Helper class for memory updates"""
    memory_type: str  # "semantic", "episodic", "procedural"
    user_id: str
    update_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class MemoryQuery(BaseModel):
    """Helper class for memory queries"""
    memory_type: str
    user_id: str
    query_filters: Optional[Dict[str, Any]] = None 