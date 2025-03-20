import json
from pathlib import Path
import re
from shutil import rmtree
from textwrap import dedent
from agno.utils.pprint import pprint_run_response
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from utils import get_google_api_key, get_tavily_api_key
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from Agents.MRTeam import MRTeam
from Agents.UsecaseTeam import UseCaseTeam
from Agents.UsecaseWriter import UsecaseWriter

reports_dir = Path(__file__).parent.joinpath("reports")
if reports_dir.is_dir():
    rmtree(path=reports_dir, ignore_errors=True)
reports_dir.mkdir(parents=True, exist_ok=True)
mr_research_report = str(reports_dir.joinpath("mr_research_report.md"))
market_standards_report = str(reports_dir.joinpath("market_standards_report.md"))
# a1 = Agent(
#     name="Web Searcher Agent",
#     model=Gemini(
#         id="gemini-1.5-flash",
#         api_key=get_google_api_key(),
#         temperature=0.2,
#     ),
#     tools=[DuckDuckGoTools()],
#     description="You are Web Search Bot, an expert at discovering high-quality web sources and formatting results precisely in a structured format.",
#     instructions=[
#         "First create search query using below example queries:",
#         "How is the <industry> leveraging AI and ML?",
#         "AI applications in <industry>",
#         "Latest AI adoption trends in <industry>",
#         "Benchmark AI/ML practices in <industry>",
#         "Second, your task is to use DuckDuckGoTools to search at least 10-15 sources and identify the 5-7 most authoritative and relevant ones."
#         "Search should be similar to above example queries.",
#         "Prioritize results from authoritative sources such as:"
#         "Consulting firms (McKinsey, Deloitte, Gartner, Nexocode)",
#         "Return a structured list of URLs with article titles, summaries, contents,, and source credibility ratings.",
#     ],
#     # response_model=SearchResults,
#     debug_mode=True,
#     structured_outputs=True,
#     # show_tool_calls=True,
# )

# a1.print_response("info on wipro")


a1 = UseCaseTeam(market_standards_report)
pprint_run_response(a1.run("ai adoption in wipro"))
