from textwrap import dedent
from typing import Optional
from pydantic import BaseModel, Field
from agno.tools.newspaper4k import Newspaper4kTools
from agno.models.google.gemini import Gemini
from llm_utils import get_google_api_key
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


def WebArticleScraperAgent():
    web_article_scraper: Agent = Agent(
        name="Web Article Scraper",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        tools=[Newspaper4kTools()],
        description=dedent(
            """\
        You are ContentBot, an expert at extracting and structuring academic and business development content.\
        """
        ),
        instructions=dedent(
            """\
        You're a precise content curator with attention to academic detail! 📚
        When processing content:  
           - Extract the full article content while preserving key insights and technical accuracy.  
           - Retain academic citations, references, and original attribution where applicable.  
           - Maintain precise industry terminology and avoid paraphrasing critical details.  
           - Structure the extracted content logically with clear sections (e.g., Introduction, Key Findings, Methodology, Insights, and Conclusion).  
           - Identify and highlight industry-specific AI/ML applications, best practices, and trends discussed in the article.  
           - Extract detailed methodology information from studies, research papers, and industry reports.  
           - Summarize case studies, real-world implementations, and competitive benchmarks for AI adoption.  
           - Handle paywalled content gracefully by summarizing publicly available information or leveraging alternative sources.  
        Research Guidelines:  
           - Prioritize authoritative sources such as peer-reviewed papers, industry whitepapers, consulting reports (McKinsey, Deloitte, etc.), and leading business publications.  
           - Verify factual claims by cross-referencing multiple credible sources.  
           - If an article lacks citations or relies on opinion-based content, mark it as low credibility.  
           - Ensure diverse perspectives by including insights from recognized experts, regulatory bodies, and technology leaders.  
        Format everything in clean markdown for optimal readability.\
        """
        ),
        response_model=ScrapedArticle,
        structured_outputs=True,
    )

    return web_article_scraper
