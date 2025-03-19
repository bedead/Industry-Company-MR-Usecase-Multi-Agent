from textwrap import dedent
from typing import Optional
from pydantic import BaseModel, Field
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from agno.models.google.gemini import Gemini
from agno.models.groq.groq import Groq
from utils import get_google_api_key, get_groq_api_key
from agno.agent import Agent


class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    articles: list[Article]


def WebSearcherAgent(description, instructions, expected_output):
    web_searcher: Agent = Agent(
        name="Web Researcher",
        model=Gemini(
            id="gemini-2.0-flash",
            api_key=get_google_api_key(),
        ),
        tools=[
            DuckDuckGoTools(),
        ],
        description=description,
        instructions=instructions,
        expected_output=expected_output,
        # response_model=SearchResults,
        # debug_mode=True,
        structured_outputs=True,
    )

    return web_searcher
