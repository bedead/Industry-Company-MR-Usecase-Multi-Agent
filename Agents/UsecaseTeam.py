from pathlib import Path
from shutil import rmtree
from textwrap import dedent
from typing import Iterator
from agno.workflow import Workflow
from agno.utils.log import logger
from agno.agent import Agent, RunResponse
from Agents.MRTeam import MRTeam
from Agents.MRWriterAgent import MRWriterAgent
from Agents.UsecaseWriter import UsecaseWriter
from Agents.UsecaseQueryGeneratorAgent import UsecaseQueryGeneratorAgent
from Agents.UseCaseFinderAgent import UseCaseFinderAgent
from agno.utils.pprint import pprint_run_response

from agno.models.google.gemini import Gemini
from utils import get_google_api_key
from agno.tools.duckduckgo import DuckDuckGoTools


class UseCaseTeam:
    def __init__(self, usecase_save_response_at_file):
        self.web_searcher = Agent(
            name="Web Searcher Agent",
            model=Gemini(
                id="gemini-1.5-flash",
                api_key=get_google_api_key(),
                temperature=0.2,
            ),
            tools=[DuckDuckGoTools()],
            description="You are Web Search Bot, an expert at discovering high-quality web sources and formatting results precisely in a structured format.",
            instructions=[
                "First create search query using below example queries:",
                "How is the <industry> leveraging AI and ML?",
                "AI applications in <industry>",
                "Latest AI adoption trends in <industry>",
                "Benchmark AI/ML practices in <industry>",
                "Second, your task is to use DuckDuckGoTools to search at least 10-15 sources and identify the 5-7 most authoritative and relevant ones."
                "Search should be similar to above example queries.",
                "Prioritize results from authoritative sources such as:"
                "Consulting firms (McKinsey, Deloitte, Gartner, Nexocode)",
                "Return a structured list of URLs with article titles, summaries, contents,, and source credibility ratings.",
            ],
            # response_model=SearchResults,
            debug_mode=True,
            structured_outputs=True,
            # show_tool_calls=True,
        )

        self.usecase_writer = UsecaseWriter(
            save_response_at_file=usecase_save_response_at_file
        )

    def run(self, query):
        response: RunResponse = self.web_searcher.run(message=query)
        final_report: RunResponse = self.usecase_writer.run(message=response.content)

        return final_report
