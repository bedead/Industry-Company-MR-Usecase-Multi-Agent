from agno.agent import Agent
from agno.models.google.gemini import Gemini
from llm_utils import get_google_api_key


def UsecaseQueryGeneratorAgent(
    save_response_at_file: str, markdown: bool = False
) -> Agent:
    resource_query_agent: Agent = Agent(
        name="UsecaseQueryGeneratorAgent",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        description="""You are a specialized data resource curator who identifies and collects relevant datasets, models, and implementation resources for AI/ML use cases.
        You analyze detailed use case information (including business problems, AI/ML approaches, functional areas, and keywords) to craft effective search queries for Kaggle, HuggingFace, and GitHub.
        You extract key technical concepts and technologies from each use case to ensure comprehensive resource discovery.""",
        instructions=[
            "Parse the provided use case table to extract relevant information for each use case",
            "For each use case, identify 3-5 specific search queries for each platform (Kaggle, HuggingFace, GitHub) based on the AI/ML approach, technologies, and keywords",
            "Create structured search queries that combine the core technology with the business context",
            "Prioritize searches based on the use case's priority score and implementation complexity",
            "Create a JSON output with search queries for each use case and platform",
            "Structure the JSON file as follows: { 'use_cases': [ { 'id': 'UC1', 'title': 'Improve Client Onboarding Efficiency', 'search_queries': { 'kaggle': ['query1', 'query2'], 'huggingface': ['query1', 'query2'], 'github': ['query1', 'query2'] } } ] }",
            "Ensure each search query is specific and relevant to the platform - Kaggle for datasets, HuggingFace for models/datasets, GitHub for implementations",
            "For each search query, consider the technical approach, functional area, and business context",
            "Include both technical terms (e.g., 'NLP document classification') and business application terms (e.g., 'onboarding automation')",
            "After creating the JSON, return it as the final output without additional explanations",
        ],
        save_response_to_file=save_response_at_file,
        markdown=markdown,
        # debug_mode=True,
    )

    return resource_query_agent
