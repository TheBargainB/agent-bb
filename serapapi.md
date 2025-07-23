SerpAPIWrapper
class langchain_community.utilities.serpapi.SerpAPIWrapper[source]
Bases: BaseModel

Wrapper around SerpAPI.

To use, you should have the google-search-results python package installed, and the environment variable SERPAPI_API_KEY set with your API key, or pass serpapi_api_key as a named parameter to the constructor.

Example

from langchain_community.utilities import SerpAPIWrapper
serpapi = SerpAPIWrapper()
Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

param aiosession: ClientSession | None = None
param params: dict = {'engine': 'google', 'gl': 'us', 'google_domain': 'google.com', 'hl': 'en'}
param serpapi_api_key: str | None = None
async aresults(query: str) → dict[source]
Use aiohttp to run query through SerpAPI and return the results async.

Parameters
:
query (str)

Return type
:
dict

async arun(
query: str,
**kwargs: Any,
) → str[source]
Run query through SerpAPI and parse result async.

Parameters
:
query (str)

kwargs (Any)

Return type
:
str

get_params(
query: str,
) → Dict[str, str][source]
Get parameters for SerpAPI.

Parameters
:
query (str)

Return type
:
Dict[str, str]

results(query: str) → dict[source]
Run query through SerpAPI and return the raw result.

Parameters
:
query (str)

Return type
:
dict

run(query: str, **kwargs: Any) → str[source]
Run query through SerpAPI and parse result.

Parameters
:
query (str)

kwargs (Any)

Return type
:
str