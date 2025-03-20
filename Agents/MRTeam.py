from pathlib import Path
from shutil import rmtree
from textwrap import dedent
from typing import Iterator
from agno.workflow import Workflow
from agno.utils.log import logger
from agno.agent import Agent, RunResponse
from Agents.MRWriterAgent import MRWriterAgent
from Agents.UsecaseWriter import UsecaseWriter
from Agents.UsecaseQueryGeneratorAgent import UsecaseQueryGeneratorAgent
from Agents.UseCaseFinderAgent import UseCaseFinderAgent
from agno.utils.pprint import pprint_run_response

from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.tavily import TavilyTools
from agno.models.google.gemini import Gemini
from utils import get_google_api_key, get_tavily_api_key
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools


class MRTeam:
    def __init__(self, mr_save_response_as_file):
        self.web_searcher: Agent = Agent(
            name="Web Searcher Agent",
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=get_google_api_key(),
                temperature=0.2,
            ),
            tools=[
                DuckDuckGoTools(),
            ],
            description="You are Web Search Bot, an expert at discovering high-quality web sources and formatting results precisely in a structured format.",
            instructions=dedent(
                """
                Your task is to use DuckDuckGoTools to search for each least 10-15 sources and identify the 5-7 most authoritative and relevant ones.
                Prioritize:
                Peer-reviewed articles and academic publications
                Recent developments from reputable institutions
                Authoritative news sources and expert commentary
                Diverse perspectives from recognized experts

                Always provide your output in the following strict JSON format:
                [
                    {
                        "title": "Full title of the source",
                        "url": "Complete URL of the source",
                        "summary": "A concise 2-3 sentence summary of the key information"
                    }
                ]

                Do not include any explanations or additional text before or after the JSON list. The output must be a valid JSON array that can be directly parsed.
                """
            ),
            tool_choice="auto",
            # response_model=SearchResults,
            debug_mode=True,
            structured_outputs=True,
            # show_tool_calls=True,
        )

        self.article_searcher: Agent = Agent(
            name="Web Article Scraper",
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=get_google_api_key(),
                # temperature=0.2,
            ),
            tools=[Newspaper4kTools()],
            description="Scrape the provided URLs and extract complete article content.",
            instructions=dedent(
                """\
                You are given a list of dictinary containing several article titles, url and summary.
                Your task is to use tools to extract content for each provided url, and return structured output.
                Structured output format:

                [
                    {
                        "title": "<Title of the article>",
                        "url": "<Link to the article>",
                        "summary": "<Summary of the article>",
                        "content": "<Extracted article content in Markdown format, or None>"
                    },{
                    next article...
                    },
                ]
                """
            ),
            debug_mode=True,
            # response_model=ScrapedArticle,
            structured_outputs=True,
        )

        self.MRWriter = MRWriterAgent(save_response_as_file=mr_save_response_as_file)

    def run(self, query):
        response: RunResponse = self.web_searcher.run(query)
        response1: RunResponse = self.article_searcher.run(message=response.content)
        final_report: RunResponse = self.MRWriter.run(message=response1.content)

        return final_report
