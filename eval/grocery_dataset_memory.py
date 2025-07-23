"""
Dataset for evaluating the Phase 3 sophisticated memory functionality
"""

# Memory evaluation examples
examples_memory = [
    {
        "inputs": {
            "user_query": "I'm allergic to gluten and dairy, can you recommend breakfast options?",
            "user_id": "test_user_1"
        },
        "outputs": {
            "has_dietary_restrictions": True,
            "dietary_restrictions": ["gluten-free", "dairy-free"],
            "food_category": "breakfast",
            "should_remember_preferences": True
        }
    },
    {
        "inputs": {
            "user_query": "I need organic vegetables under $20 for my family of 4",
            "user_id": "test_user_2"
        },
        "outputs": {
            "budget_constraint": True,
            "budget_amount": 20,
            "family_size": 4,
            "organic_preference": True,
            "food_category": "vegetables"
        }
    },
    {
        "inputs": {
            "user_query": "I bought those blueberries you recommended last week, they were great!",
            "user_id": "test_user_1"
        },
        "outputs": {
            "references_past_interaction": True,
            "positive_feedback": True,
            "mentioned_product": "blueberries",
            "should_update_preferences": True
        }
    },
    {
        "inputs": {
            "user_query": "Can you find me low-sodium snacks for my heart condition?",
            "user_id": "test_user_3"
        },
        "outputs": {
            "health_condition": "heart condition",
            "dietary_restrictions": ["low-sodium"],
            "food_category": "snacks",
            "health_conscious": True
        }
    },
    {
        "inputs": {
            "user_query": "I usually shop at Whole Foods, find me their weekly deals",
            "user_id": "test_user_2"
        },
        "outputs": {
            "store_preference": "whole_foods",
            "seeking_deals": True,
            "should_remember_store_preference": True,
            "temporal_request": "weekly"
        }
    }
]

# Regional agent evaluation examples
examples_regional_usa = [
    {
        "inputs": {
            "user_query": "I need organic pasta under $5 at Target",
            "config": {
                "country_code": "US",
                "language_code": "en",
                "store_preference": "target"
            }
        },
        "outputs": {
            "response_language": "en",
            "mentions_target": True,
            "mentions_dollar_pricing": True,
            "organic_focus": True,
            "budget_constraint": 5
        }
    },
    {
        "inputs": {
            "user_query": "Find me the cheapest whole grain bread at Walmart",
            "config": {
                "country_code": "US",
                "language_code": "en",
                "store_preference": "walmart"
            }
        },
        "outputs": {
            "response_language": "en",
            "mentions_walmart": True,
            "price_focused": True,
            "product_type": "bread",
            "health_conscious": True
        }
    }
]

examples_regional_netherlands = [
    {
        "inputs": {
            "user_query": "Ik zoek biologische melk onder €3 bij Albert Heijn",
            "config": {
                "country_code": "NL",
                "language_code": "nl",
                "store_preference": "albert_heijn"
            }
        },
        "outputs": {
            "response_language": "nl",
            "mentions_albert_heijn": True,
            "mentions_euro_pricing": True,
            "organic_focus": True,
            "product_type": "melk"
        }
    },
    {
        "inputs": {
            "user_query": "Wat zijn de goedkoopste groenten bij Jumbo deze week?",
            "config": {
                "country_code": "NL",
                "language_code": "nl",
                "store_preference": "jumbo"
            }
        },
        "outputs": {
            "response_language": "nl",
            "mentions_jumbo": True,
            "price_focused": True,
            "product_type": "groenten",
            "temporal_request": "deze week"
        }
    }
]

# Tool functionality evaluation examples
examples_tools = [
    {
        "inputs": {
            "user_query": "Search for vegan protein powder under $30",
            "tool_type": "search"
        },
        "outputs": {
            "uses_search_tool": True,
            "dietary_filter": "vegan",
            "product_category": "protein powder",
            "price_filter": 30,
            "returns_results": True
        }
    },
    {
        "inputs": {
            "user_query": "Research the nutritional benefits of quinoa",
            "tool_type": "research"
        },
        "outputs": {
            "uses_research_tool": True,
            "research_topic": "quinoa",
            "focus_area": "nutrition",
            "provides_detailed_info": True
        }
    },
    {
        "inputs": {
            "user_query": "Compare prices of organic apples across stores",
            "tool_type": "comparison"
        },
        "outputs": {
            "price_comparison": True,
            "product_type": "apples",
            "organic_focus": True,
            "multi_store_analysis": True
        }
    }
] 