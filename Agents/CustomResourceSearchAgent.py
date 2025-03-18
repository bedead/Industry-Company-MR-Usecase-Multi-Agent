from agno.agent import Agent
from Agents.AIResourceToolKit import AIResourceTools
from llm_utils import get_google_api_key
from agno.models.google.gemini import Gemini


def CustomSearchAgent(query: str, save_response_at_file: str):
    agent = Agent(
        name="ResourceHunter",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        tools=[AIResourceTools()],
        description="""You are a specialized data resource curator who identifies and collects 
        real, accessible datasets, models, and implementation resources for AI/ML use cases.""",
        instructions=[
            "For each AI use case provided, search for real resources using the AIResourceTools.",
            "Use search_kaggle_datasets(), search_huggingface(), and search_github_repos() functions for each use case.",
            "Create a comprehensive markdown report with all findings, organized by use case.",
            "Include direct hyperlinks to actual resources in proper markdown format: [Resource Name](actual_url_here).",
            "For each dataset, include statistics like size, records, and features.",
            "For GitHub repositories, include star count, last update date, and contributor count.",
            "Verify each URL using the verify_url() function before including it in the report.",
            "Include license information for each resource when available.",
            "Save the final markdown report to a file using the provided save_markdown() function.",
            "Use multiple search keywords to ensure comprehensive resource discovery.",
            "For resources not found, include suggestions for alternative search strategies.",
        ],
        expected_output="Comprehensive reporting containing search data related to query in markdown format with real urls and data.",
        save_response_to_file=save_response_at_file,
        # show_tool_calls=True,
        debug_mode=True,
        # markdown=True,
    )
    response = agent.run(query)
    return response.content
