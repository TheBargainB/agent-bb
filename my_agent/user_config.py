"""
International user configuration model for storing user preferences.
This configuration supports grocery shopping worldwide with personalized preferences.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class DietaryRestriction(str, Enum):
    """Common dietary restrictions and preferences."""
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    LACTOSE_FREE = "lactose_free"
    KETO = "keto"
    HALAL = "halal"
    KOSHER = "kosher"

class BudgetLevel(str, Enum):
    """Budget level preferences."""
    LOW = "low"          # Budget-conscious, discount stores
    MEDIUM = "medium"    # Balanced price/quality
    HIGH = "high"        # Premium products, no budget constraints
    NO_LIMIT = "no_limit"

class UserConfig(BaseModel):
    """International user configuration for personalizing agent responses."""
    
    # User identification
    user_id: Optional[str] = Field(default=None, description="Unique identifier for the user")
    
    # Personal preferences
    name: Optional[str] = Field(default=None, description="User's name for personalization")
    
    # Location
    country_code: str = Field(default="US", description="Country code (e.g., 'US', 'UK', 'DE', 'NL')")
    language_code: str = Field(default="en", description="Language code (e.g., 'en', 'nl', 'de', 'fr')")
    
    # User preferences
    dietary_restrictions: List[DietaryRestriction] = Field(
        default=[DietaryRestriction.NONE],
        description="Dietary restrictions and preferences"
    )
    budget_level: BudgetLevel = Field(default=BudgetLevel.MEDIUM, description="Budget level preference")
    household_size: int = Field(default=1, description="Number of people in household")
    store_preference: str = Field(default="any", description="Preferred store for shopping")
    store_websites: str = Field(default="walmart.com, target.com, amazon.com", description="Store websites to search") 