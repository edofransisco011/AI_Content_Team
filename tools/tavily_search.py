import os
import json
from tavily import TavilyClient
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('tavily_search')
class TavilySearchTool(BaseTool):
    """
    A custom web search tool using the Tavily API.
    This tool is designed to provide clean, AI-ready search results.
    """
    name = 'tavily_search'
    # THE FIX: Removed the erroneous double-quote from the middle of this string.
    description = (
        'Performs a web search using the Tavily API to find up-to-date information on a given topic. '
        'Returns a concise summary of search results.'
    )
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': 'The search query to find information about.',
        'required': True
    }]

    def __init__(self, cfg: dict = {}):
        super().__init__(cfg)
        # Initialize the Tavily client with the API key from environment variables
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def call(self, params: str, **kwargs) -> str:
        """
        Executes the search query using the Tavily client.
        """
        try:
            # Parse the parameters string into a dictionary
            params_dict = json.loads(params)
            query = params_dict.get('query')
            if not query:
                return 'Error: The search query cannot be empty.'

            # Perform the search
            response = self.client.search(query=query, search_depth="basic", max_results=3)

            # Format the results into a clean string for the LLM
            formatted_results = []
            for result in response.get('results', []):
                formatted_results.append(
                    f"Title: {result.get('title')}\n"
                    f"URL: {result.get('url')}\n"
                    f"Snippet: {result.get('content')}\n"
                    "---"
                )
            
            if not formatted_results:
                return "No search results found."

            return "\n".join(formatted_results)

        except Exception as e:
            return f"An error occurred during the search: {str(e)}"
