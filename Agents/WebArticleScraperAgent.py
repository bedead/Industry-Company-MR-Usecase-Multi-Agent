from textwrap import dedent
from typing import Optional
from pydantic import BaseModel, Field
from agno.tools.newspaper4k import Newspaper4kTools
from agno.models.google.gemini import Gemini
from utils import get_google_api_key
from agno.agent import Agent


class ScrapedArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )
    content: Optional[str] = Field(
        ...,
        description="Content of the in markdown format if available. Return None if the content is not available or does not make sense.",
    )


def WebArticleScraperAgent(description, instructions, expected_output):
    web_article_scraper: Agent = Agent(
        name="Web Article Scraper",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        tools=[Newspaper4kTools()],
        description=description,
        instructions=instructions,
        expected_output=expected_output,
        # debug_mode=True,
        # response_model=ScrapedArticle,
        structured_outputs=True,
    )

    return web_article_scraper
