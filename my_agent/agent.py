"""
Main agent definition for the grocery shopping assistant.
Following the tutorial pattern with memory enhancement.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import memory-enhanced supervisor (tutorial pattern)
from my_agent.utils.graph import make_memory_enhanced_supervisor

# Export the memory-enhanced graph for LangGraph configuration (tutorial pattern)
graph = make_memory_enhanced_supervisor 