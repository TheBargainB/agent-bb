"""
Simple runner script for grocery shopping assistant evaluations
Run this script to execute all LangSmith evaluations
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, try to load manually
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Check for LangSmith API key
if not os.getenv("LANGSMITH_API_KEY"):
    print("❌ Error: LANGSMITH_API_KEY environment variable not set")
    print("Please set your LangSmith API key:")
    print("export LANGSMITH_API_KEY='your-api-key-here'")
    sys.exit(1)

# Import and run evaluations
try:
    from eval.grocery_evaluation_langsmith import run_evaluations
    
    print("🍎 Grocery Shopping Assistant - LangSmith Evaluation")
    print("=" * 60)
    print("This will evaluate:")
    print("✅ Phase 3 Memory System")
    print("✅ USA Regional Agent")  
    print("✅ Netherlands Regional Agent")
    print("✅ Tools Functionality")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("Run evaluations? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        results = run_evaluations(run_expt=True)
        
        if results:
            print("\n🎉 All evaluations completed successfully!")
            print("📊 Check LangSmith UI for detailed results")
        else:
            print("\n⚠️ Evaluations completed but no results returned")
    else:
        print("❌ Evaluations cancelled")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install langsmith requests")
    
except Exception as e:
    print(f"❌ Error running evaluations: {e}")
    print("Make sure the LangGraph server is running on http://127.0.0.1:2024") 