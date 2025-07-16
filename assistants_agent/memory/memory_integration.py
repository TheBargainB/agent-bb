"""
Memory integration system for Phase 2: Semantic Memory Collection.
Hooks into supervisor workflow to collect insights without affecting routing.
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.store.memory import InMemoryStore

from assistants_agent.memory.collection_tools import extract_insights_from_conversation
from assistants_agent.memory.schemas import GroceryProfile


class MemoryCollector:
    """
    Phase 2: Collect semantic memory from conversations without affecting routing.
    """
    
    def __init__(self, memory_store: InMemoryStore):
        self.memory_store = memory_store
        self.enabled_features = {
            'semantic': False,
            'episodic': False, 
            'procedural': False
        }
    
    def configure(self, config: Dict[str, Any]):
        """Configure which memory features are enabled"""
        self.enabled_features['semantic'] = config.get('memory_semantic_enabled', False)
        self.enabled_features['episodic'] = config.get('memory_episodic_enabled', False)
        self.enabled_features['procedural'] = config.get('memory_procedural_enabled', False)
        
        print(f"🧠 Memory collector configured:")
        print(f"   Semantic: {self.enabled_features['semantic']}")
        print(f"   Episodic: {self.enabled_features['episodic']}")
        print(f"   Procedural: {self.enabled_features['procedural']}")
    
    def collect_from_conversation(
        self,
        user_id: str,
        user_query: str,
        user_config: Dict[str, Any],
        agent_responses: List[str]
    ) -> Dict[str, Any]:
        """
        Phase 2: Collect semantic memory from conversation.
        Returns collection results without affecting routing decisions.
        """
        results = {
            'semantic_collected': False,
            'insights_count': 0,
            'collection_summary': "Memory collection disabled"
        }
        
        # Only collect if semantic memory is enabled
        if not self.enabled_features['semantic']:
            return results
        
        try:
            # Extract insights from conversation
            insights = extract_insights_from_conversation(user_query, user_config, agent_responses)
            
            if not insights:
                results['collection_summary'] = "No new semantic insights detected"
                return results
            
            # Get or create user profile
            try:
                existing_item = self.memory_store.get(("grocery_profiles", user_id), "profile")
                if existing_item:
                    profile = GroceryProfile(**existing_item.value)
                else:
                    profile = GroceryProfile(user_id=user_id)
            except Exception:
                profile = GroceryProfile(user_id=user_id)
            
            # Update profile with insights
            insights_added = 0
            for insight in insights:
                category = getattr(profile, insight.category, {})
                if not category:
                    category = {}
                
                # Add or update insight
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
            
            # Update profile timestamp
            profile.last_updated = datetime.now()
            
            # Store updated profile
            self.memory_store.put(("grocery_profiles", user_id), "profile", profile.model_dump())
            
            results.update({
                'semantic_collected': True,
                'insights_count': insights_added,
                'collection_summary': f"✅ {insights_added} new insights collected (Phase 2: collection only)"
            })
            
        except Exception as e:
            results['collection_summary'] = f"❌ Memory collection error: {str(e)}"
        
        return results
    
    def get_user_profile_summary(self, user_id: str) -> str:
        """
        Get a summary of collected user insights for transparency.
        Phase 2: Show what system has learned.
        """
        try:
            profile_item = self.memory_store.get(("grocery_profiles", user_id), "profile")
            if not profile_item:
                return "No semantic insights collected yet"
            
            profile = GroceryProfile(**profile_item.value)
            
            summary = "🧠 Learned User Insights (Phase 2 - Collection Only):\n\n"
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
            return f"❌ Error retrieving insights: {str(e)}"


def create_memory_collector(memory_store: InMemoryStore, config: Dict[str, Any]) -> Optional[MemoryCollector]:
    """
    Factory function to create memory collector if memory is enabled.
    Phase 2: Only create if semantic memory is enabled.
    """
    if not config.get('memory_enabled', False):
        return None
        
    collector = MemoryCollector(memory_store)
    collector.configure(config)
    return collector


def add_memory_insight_to_prompt(
    original_prompt: str, 
    user_id: str, 
    memory_collector: Optional[MemoryCollector]
) -> str:
    """
    Phase 2: Add memory insights to supervisor prompt for transparency.
    Shows what system has learned but doesn't change routing logic.
    """
    if not memory_collector or not memory_collector.enabled_features['semantic']:
        return original_prompt
    
    try:
        insights_summary = memory_collector.get_user_profile_summary(user_id)
        
        # Add insights section to prompt (for transparency, not routing changes)
        enhanced_prompt = f"""{original_prompt}

🧠 MEMORY INSIGHTS (Phase 2 - Transparency Only):
{insights_summary}

IMPORTANT: These insights are for awareness only. Continue using the same routing logic as before.
Do not change agent selection based on these insights yet (Phase 2 limitation)."""
        
        return enhanced_prompt
        
    except Exception as e:
        print(f"⚠️ Memory insight integration error: {e}")
        return original_prompt 