# International Grocery Shopping Assistant

A LangGraph-based AI assistant system that helps users find grocery deals and promotions **worldwide** using configurable local stores and search terms.

## 🌍 International Support

This assistant works globally by allowing users to configure:

- **Local grocery stores** and their websites
- **Search terms** in local languages
- **Dietary restrictions** in local terminology
- **Currency** and budget preferences
- **Regional shopping patterns**

## 🛒 Supported Regions (Pre-configured)

### Netherlands (NL)
- **Stores**: Albert Heijn, Jumbo, Lidl
- **Language**: Dutch
- **Currency**: EUR
- **Search terms**: "aanbiedingen", "bonus", "korting"

### United States (US)
- **Stores**: Walmart, Target
- **Language**: English
- **Currency**: USD  
- **Search terms**: "deals", "offers", "promotions"

### United Kingdom (UK)
- **Stores**: Tesco, Sainsbury's
- **Language**: English
- **Currency**: GBP
- **Search terms**: "offers", "deals", "promotions"

## 🔧 Custom Configuration

You can easily add support for any country by configuring:

```python
from my_agent.user_config import UserConfig, GroceryStore, LocalizationConfig

# Example: German configuration
german_config = UserConfig(
    localization=LocalizationConfig(
        language_code="de",
        country_code="DE",
        promotion_keywords=["angebote", "rabatt", "aktionen"],
        this_week_terms=["diese woche", "wöchentlich"],
        grocery_terms=["lebensmittel", "supermarkt"],
        dietary_terms={
            "vegetarian": ["vegetarisch"],
            "vegan": ["vegan"],
            "gluten_free": ["glutenfrei"],
            "organic": ["bio", "ökologisch"]
        }
    ),
    grocery_stores=[
        GroceryStore(
            name="REWE",
            website_domain="rewe.de",
            promotions_search_terms=[
                "rewe.de angebote diese woche",
                "rewe.de rabatte"
            ],
            country="DE",
            currency="EUR"
        ),
        GroceryStore(
            name="EDEKA", 
            website_domain="edeka.de",
            promotions_search_terms=[
                "edeka.de angebote",
                "edeka.de aktionen"
            ],
            country="DE",
            currency="EUR"
        )
    ]
)
```

## 🎯 Agents

### Promotions Research Agent
- Finds current deals and promotions from configured stores
- Uses store-specific search terms and local language
- Filters by dietary restrictions and budget

### Grocery Search Agent  
- Searches for specific products across configured stores
- Compares prices in local currency
- Considers household size and preferences

## 🚀 Usage

The assistant automatically adapts to your configuration:

1. **Store Selection**: Uses only your configured stores
2. **Language**: Searches using your local terms
3. **Currency**: Shows prices in your local currency
4. **Dietary Needs**: Filters using local dietary terms
5. **Cultural Preferences**: Adapts to regional shopping patterns

## 🛠️ Technical Architecture

- **Modular Design**: Shared agent framework in `utils/`
- **Dynamic Prompts**: Generated based on user configuration
- **International Support**: Configurable stores and search terms
- **LangGraph**: Supervisor pattern with specialized agents
- **Personalization**: User preferences integrated at runtime

## 📁 Project Structure

```
my_agent/
├── agents/
│   ├── promotions_agent/    # Finds deals and promotions
│   └── grocery_agent/       # Searches for specific products
├── supervisor/              # Orchestrates agent collaboration
├── utils/                   # Shared agent framework
├── user_config.py          # International configuration system
└── agent.py               # Main entry point
```

## 🔑 Configuration Fields

- **Stores**: Website domains and search terms
- **Language**: Search keywords and dietary terms
- **Budget**: Currency and spending preferences  
- **Diet**: Local terminology for restrictions
- **Location**: Country/city for local availability
- **Household**: Size and storage considerations

Start shopping smarter with personalized, international grocery assistance! 🛍️