from textwrap import dedent
from typing import Optional
from pydantic import BaseModel, Field
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.google.gemini import Gemini
from llm_utils import get_google_api_key
from agno.agent import Agent


class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    articles: list[Article]


def WebSearcherAgent():
    web_searcher: Agent = Agent(
        name="Web Researcher",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        tools=[GoogleSearchTools()],
        description=dedent(
            """\
        You are Web Search Bot, an expert at discovering academic and business development sources.\
        """
        ),
        instructions=[
            "Given a company name or industry, conduct a comprehensive search to gather relevant and credible information on its business model, market position, and strategic priorities.",
            "Search for 10-15 potential sources, prioritizing the most authoritative and relevant 5-7 sources for analysis.",
            "Prioritize the following types of sources: \n  - Peer-reviewed articles and academic publications\n  - Recent reports from reputable institutions (e.g., McKinsey, Deloitte, World Economic Forum, Nexocode, etc.)\n  - Authoritative news sources (e.g., Bloomberg, Forbes, Financial Times, Harvard Business Review, MIT Technology Review)\n  - Industry whitepapers, government reports, and expert commentary from professionals recognized in the field.",
            "Avoid non-authoritative sources, opinion pieces, blogs with unverified claims, or promotional content with no factual basis.",
            "Perform a detailed search for recent company information, including key products/services, target markets, primary business objectives, and major technology initiatives.",
            "Identify the industry segment(s) in which the company operates (e.g., Automotive, Manufacturing, Finance, Retail, Healthcare, etc.) and highlight emerging AI/ML trends shaping this sector.",
            "Assess the company's strategic initiatives related to digital transformation, AI adoption, and technology integration, ensuring sourced data is from trusted industry reports.",
            "Research the company's operational pain points and areas where efficiency improvements are being sought, focusing on data-backed analysis from reputable sources.",
            "Gather comparative insights on the company's competitors, analyzing their technology adoption, innovation strategies, and competitive advantages.",
            "Where applicable, include references to industry-specific reports and insights from firms such as McKinsey, Deloitte, and Nexocode to ensure high-quality research findings.",
            "If direct company-specific information is limited, shift focus to broader industry trends, market dynamics, and general challenges faced by similar businesses in the sector.",
            "Ensure a balanced and well-rounded analysis by gathering insights from diverse, credible sources, such as annual reports, company press releases, industry analyses, and reputable business publications.",
        ],
        response_model=SearchResults,
        structured_outputs=True,
    )

    return web_searcher
