from langchain_core.runnables import RunnableConfig
from assistants_agent.supervisor.supervisor_configuration import Configuration
from assistants_agent.supervisor.subagents import create_subagents
from assistants_agent.utils.utils import load_chat_model

from langgraph_supervisor import create_supervisor

# Memory imports (Phase 1: passive initialization, Phase 2: collection integration)
from langgraph.store.memory import InMemoryStore
from assistants_agent.memory.schemas import GroceryProfile, ShoppingEpisode, SupervisorInstructions
from assistants_agent.memory.memory_integration import create_memory_collector, MemoryCollector

# Main graph construction
async def make_supervisor_graph(config: RunnableConfig):
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful supervisor agent.")
    
    # Phase 1: Initialize memory store passively, Phase 2: Add memory collection
    memory_enabled = configurable.get("memory_enabled", False)
    memory_store = None
    memory_collector = None
    
    if memory_enabled:
        # Initialize InMemoryStore and memory collector (Phase 2: active collection)
        memory_store = InMemoryStore()
        memory_collector = create_memory_collector(memory_store, configurable)
        
        print(f"🧠 Memory store initialized (enabled: {memory_enabled})")
        if memory_collector:
            print(f"   Semantic collection: {memory_collector.enabled_features['semantic']}")
        print(f"   Episodic: {configurable.get('memory_episodic_enabled', False)}")
        print(f"   Procedural: {configurable.get('memory_procedural_enabled', False)}")
    
    # Create subagents using the new async function, passing configurable values
    subagents = await create_subagents(configurable)

    # Create supervisor graph
    supervisor_graph = create_supervisor(
        agents=subagents,
        model=load_chat_model(supervisor_model),
        prompt=supervisor_system_prompt,
        config_schema=Configuration
    )

    compiled_graph = supervisor_graph.compile()
    
    # Store memory instances for current and future phases
    if memory_store:
        compiled_graph._memory_store = memory_store
    if memory_collector:
        compiled_graph._memory_collector = memory_collector
    
    return compiled_graph


# Phase 2: Memory collection function to be called after supervisor processes requests
def collect_memory_from_conversation(
    compiled_graph,
    user_id: str, 
    user_query: str,
    user_config: dict,
    agent_responses: list
) -> dict:
    """
    Phase 2: Collect semantic memory from conversation after supervisor completes.
    This function can be called post-processing to learn without affecting routing.
    """
    if not hasattr(compiled_graph, '_memory_collector') or not compiled_graph._memory_collector:
        return {'status': 'memory_disabled', 'message': 'Memory collection not enabled'}
    
    memory_collector = compiled_graph._memory_collector
    
    try:
        # Collect semantic memory from the conversation
        results = memory_collector.collect_from_conversation(
            user_id=user_id,
            user_query=user_query, 
            user_config=user_config,
            agent_responses=agent_responses
        )
        
        # Add memory collection status to results
        results['status'] = 'success'
        results['phase'] = 'phase_2_collection_only'
        
        return results
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Memory collection failed: {str(e)}',
            'phase': 'phase_2_collection_only'
        }


# Phase 2: Function to get memory insights for transparency  
def get_memory_insights(compiled_graph, user_id: str) -> str:
    """
    Phase 2: Get memory insights for transparency.
    Shows what the system has learned about the user.
    """
    if not hasattr(compiled_graph, '_memory_collector') or not compiled_graph._memory_collector:
        return "Memory collection not enabled"
    
    memory_collector = compiled_graph._memory_collector
    return memory_collector.get_user_profile_summary(user_id) 