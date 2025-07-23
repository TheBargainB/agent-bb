"""
Test dataset for grocery shopping assistant evaluation.
Contains diverse test cases with different countries, languages, and user preferences.
"""

# Test email inputs for grocery shopping queries
grocery_inputs = [
    "Find me organic milk deals in Dutch stores",
    "I need to buy bread and vegetables for a family of 4 in Germany",
    "What are the best deals on meat this week in France?",
    "I'm looking for gluten-free products in the UK",
    "Find me budget-friendly groceries for a student in the Netherlands",
    "What are the current promotions on dairy products in the US?",
    "I need vegetarian options for dinner tonight in Germany",
    "Find me premium organic products in France",
    "What are the best deals on household items in the UK?",
    "I'm looking for halal meat options in the Netherlands"
]

# Expected triage outputs (which agent should handle the request)
triage_outputs_list = [
    "promotions_research_agent",  # Deals on organic milk
    "product_search_agent",       # Basic product search
    "promotions_research_agent",  # Deals on meat
    "product_search_agent",       # Gluten-free products
    "promotions_research_agent",  # Budget deals
    "promotions_research_agent",  # Dairy promotions
    "product_search_agent",       # Vegetarian options
    "product_search_agent",       # Premium organic products
    "promotions_research_agent",  # Household deals
    "product_search_agent"        # Halal meat options
]

# Expected tool calls for each test case
expected_tool_calls = [
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"],
    ["google_serpapi_product_search", "tavily_product_search", "get_todays_date"]
]

# Response criteria for evaluating quality
response_criteria_list = [
    "Should mention organic milk deals in Dutch stores (ah.nl, jumbo.com, lidl.nl)",
    "Should provide bread and vegetable options for family of 4 in German stores",
    "Should mention meat deals and promotions in French stores",
    "Should provide gluten-free product options in UK stores",
    "Should focus on budget-friendly options for student in Dutch stores",
    "Should mention dairy promotions and deals in US stores",
    "Should provide vegetarian dinner options in German stores",
    "Should focus on premium organic products in French stores",
    "Should mention household item deals in UK stores",
    "Should provide halal meat options in Dutch stores"
]

# Test configurations for different user preferences
test_configs = [
    {
        "country_code": "NL",
        "language_code": "en",
        "store_preference": "Albert Heijn",
        "store_websites": "ah.nl, jumbo.com, lidl.nl",
        "budget_level": "medium",
        "dietary_restrictions": "none",
        "household_size": 2
    },
    {
        "country_code": "DE",
        "language_code": "en",
        "store_preference": "Rewe",
        "store_websites": "rewe.de, edeka.de, aldi.de",
        "budget_level": "medium",
        "dietary_restrictions": "none",
        "household_size": 4
    },
    {
        "country_code": "FR",
        "language_code": "en",
        "store_preference": "Carrefour",
        "store_websites": "carrefour.fr, auchan.fr, leclerc.fr",
        "budget_level": "medium",
        "dietary_restrictions": "none",
        "household_size": 2
    },
    {
        "country_code": "UK",
        "language_code": "en",
        "store_preference": "Tesco",
        "store_websites": "tesco.com, sainsburys.co.uk, asda.com",
        "budget_level": "medium",
        "dietary_restrictions": "gluten_free",
        "household_size": 2
    },
    {
        "country_code": "NL",
        "language_code": "en",
        "store_preference": "Lidl",
        "store_websites": "lidl.nl, aldi.nl, dirk.nl",
        "budget_level": "low",
        "dietary_restrictions": "none",
        "household_size": 1
    },
    {
        "country_code": "US",
        "language_code": "en",
        "store_preference": "Walmart",
        "store_websites": "walmart.com, target.com, kroger.com",
        "budget_level": "medium",
        "dietary_restrictions": "none",
        "household_size": 3
    },
    {
        "country_code": "DE",
        "language_code": "en",
        "store_preference": "Edeka",
        "store_websites": "edeka.de, rewe.de, aldi.de",
        "budget_level": "medium",
        "dietary_restrictions": "vegetarian",
        "household_size": 2
    },
    {
        "country_code": "FR",
        "language_code": "en",
        "store_preference": "Monoprix",
        "store_websites": "monoprix.fr, carrefour.fr, auchan.fr",
        "budget_level": "high",
        "dietary_restrictions": "none",
        "household_size": 2
    },
    {
        "country_code": "UK",
        "language_code": "en",
        "store_preference": "Sainsbury's",
        "store_websites": "sainsburys.co.uk, tesco.com, asda.com",
        "budget_level": "medium",
        "dietary_restrictions": "none",
        "household_size": 3
    },
    {
        "country_code": "NL",
        "language_code": "en",
        "store_preference": "Jumbo",
        "store_websites": "jumbo.com, ah.nl, lidl.nl",
        "budget_level": "medium",
        "dietary_restrictions": "halal",
        "household_size": 4
    }
] 