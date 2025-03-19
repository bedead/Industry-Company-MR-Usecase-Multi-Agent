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
from Agents.WebSearcherAgent import WebSearcherAgent
from Agents.WebArticleScraperAgent import WebArticleScraperAgent
from agno.models.groq import Groq
from utils import get_groq_api_key

reports_dir = Path(__file__).parent.joinpath("reports")
if reports_dir.is_dir():
    rmtree(path=reports_dir, ignore_errors=True)
reports_dir.mkdir(parents=True, exist_ok=True)
mr_research_report = str(reports_dir.joinpath("mr_research_report.md"))
market_standards_report = str(reports_dir.joinpath("market_standards_report.md"))
resource_usecase_queries = str(reports_dir.joinpath("resource_usecase_queries.json"))
final_usecase_report = str(reports_dir.joinpath("final_usecase_report.md"))


class MRTeam:
    def __init__(self, mr_save_response_as_file):
        self.web_searcher = WebSearcherAgent(
            description=dedent(
                """\
        You are Web Search Bot, an expert at discovering academic and business development sources.\
        """
            ),
            instructions=[
                "Given a company name or industry, conduct a comprehensive search to gather relevant and credible information on its business model, market position, and strategic priorities.",
                "Search web for 10-15 times, prioritizing the most authoritative and relevant 7-10 sources for analysis.",
                "Prioritize the following types of sources: \n  - Peer-reviewed articles and academic publications\n  - Recent reports from reputable institutions (e.g., McKinsey, Deloitte, World Economic Forum, Nexocode, etc.)\n  - Authoritative news sources (e.g., Bloomberg, Forbes, Financial Times, Harvard Business Review, MIT Technology Review)\n  - Industry whitepapers, government reports, and expert commentary from professionals recognized in the field.",
                "Avoid non-authoritative sources, opinion pieces, blogs with unverified claims, or promotional content with no factual basis.",
                "Perform a detailed search for recent company information, including key products/services, target markets, primary business objectives, and major technology initiatives.",
                "Where applicable, search for references related to industry-specific and insights from firms such as McKinsey, Deloitte, and Nexocode to ensure high-quality search findings.",
                dedent(
                    """\
                Use this JSON schema:

                Article = {"title": str,"url": str,"summary": str}
                SearchResults: list[Article]
                    \
            """
                ),
            ],
            expected_output="Strictly follow provided JSON schema for output.",
        )

        self.article_searcher = WebArticleScraperAgent(
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

            Output Format:  
            Return a dictionary containing the extracted article data:  

            [
                {
                    "title": "<Title of the article>",
                    "url": "<Link to the article>",
                    "summary": "<Summary of the article, or None if unavailable>",
                    "content": "<Extracted article content in Markdown format, or None>"
                },{
                next article...
                }
                
            ]

            Ensure content is well-structured and formatted for optimal readability in Markdown.  
            """
            ),
            expected_output="Strictly follow provided output format.",
        )
        self.MRWriter = MRWriterAgent(save_response_as_file=mr_save_response_as_file)

    def run(self, query):
        response: RunResponse = self.web_searcher.run(message=query)
        response1: RunResponse = self.article_searcher.run(message=response.content)
        final_report: RunResponse = self.MRWriter.run(message=response1.content)

        return final_report


class UseCaseTeam:
    def __init__(self, usecase_save_response_at_file):
        self.web_searcher = WebSearcherAgent(
            description="Conduct targeted web searches to find the latest industry research, reports, and case studies on AI/ML adoption for the given company/industry report.",
            instructions=dedent(
                """
            - Conduct at least 6 distinct searches related to AI adoption in this specific industry before finalizing results.
            - Use queries such as:
            - "How is the [industry] leveraging AI and ML?"
            - "AI applications in [industry]"
            - "Latest AI adoption trends in [industry]"
            - "Benchmark AI/ML practices in [industry]"
            - Prioritize results from authoritative sources such as:
            - Consulting firms (McKinsey, Deloitte, Gartner, Nexocode).
            - Peer-reviewed journals and research papers.
            - Industry reports and whitepapers.
            - Tech blogs from major AI companies.
            - Discard opinion-based or low-credibility sources.
            - Return a structured list of URLs with article titles, summaries (if available), and source credibility ratings."""
            ),
            expected_output="Strictly follow provided JSON schema for output.",
        )

        self.article_searcher = WebArticleScraperAgent(
            description="Scrape the provided URLs and extract complete article content in markdown format.",
            instructions=dedent(
                """For each provided URL:
                - Extract the full article content while maintaining technical accuracy.
                - **Retain citations, references, and original attribution**.
                - Structure the extracted content logically with sections such as:
                    - Introduction
                    - Key Findings
                    - Methodology
                    - Insights
                    - Conclusion
                - Extract AI/ML applications, trends, methodologies, and benchmarks from the content.
                - If an article is **paywalled**, summarize publicly available information or use alternative sources.
                - Return data in the following format:
                
                    ```json
                    {
                        "title": "Title of the article",
                        "url": "URL of the article",
                        "summary": "Brief summary (or None if unavailable)",
                        "content": "Markdown-formatted extracted content (or None if unavailable)"
                    }
                    ```
                - Return a list of extracted articles."""
            ),
            expected_output="list of extracted articles",
        )

        self.usecase_writer = UsecaseWriter(
            save_response_at_file=usecase_save_response_at_file
        )

    def run(self, MR_REPORT):
        response: RunResponse = self.web_searcher.run(message=MR_REPORT)
        response1: RunResponse = self.article_searcher.run(message=response.content)
        final_report: RunResponse = self.usecase_writer.run(message=response1.content)

        return final_report


class MRandUseCaseGenerationMultiAgent(Workflow):
    """Advanced workflow for generating Market research report and comapany/industry specific usecase with advanced model, datasets, and example reterival."""

    name = "Market Research and Usecase Generation Multi-Agent"
    description = "Advanced workflow for generating Market research report and comapany/industry specific usecase with advanced model, datasets, and example reterival."

    firstAGENT = MRTeam(mr_save_response_as_file=mr_research_report)
    secondAGENT = UseCaseTeam(usecase_save_response_at_file=market_standards_report)
    thridAGENT = UsecaseQueryGeneratorAgent(
        save_response_at_file=resource_usecase_queries
    )
    fourthAGENT = UseCaseFinderAgent(save_response_at_file=final_usecase_report)

    def run(self, query: str) -> Iterator[RunResponse]:
        logger.info(f"Researching about: {query}")
        mr_report: RunResponse = self.firstAGENT.run(query)
        if mr_report is None or not mr_report.content:
            yield RunResponse(
                run_id=self.run_id,
                content="Sorry, could not research about this company/industry.",
            )
            return
        else:
            logger.info(f"Printing Industry/Company Market Report....")
            yield RunResponse(run_id=self.run_id, content=mr_report.content)

        logger.info("Looking for industry-specific AI applications usecases.")
        usecases_report: RunResponse = self.secondAGENT.run(mr_report.content)
        if usecases_report is None or not usecases_report.content:
            yield RunResponse(
                run_id=self.run_id,
                content="Sorry, could not get the industry specific usecase report.",
            )
            return
        else:
            logger.info(f"Printing Industry/Company AI/ML Usecases Report....")
            yield RunResponse(run_id=self.run_id, content=usecases_report.content)

        logger.info(
            "Generating usecase specific keywords to look for relavant models, dataset, and solutions and saving it as JSON."
        )
        usercase_json_data: RunResponse = self.thridAGENT.run(
            message=usecases_report.content
        )

        if usercase_json_data is None or not usercase_json_data.content:
            yield RunResponse(
                run_id=self.run_id,
                content="Sorry, could not generate usecase specific query of searching.",
            )
            return
        else:
            yield RunResponse(run_id=self.run_id, content=usercase_json_data.content)
        logger.info(
            "Generating usecase specific keywords to look for relavant models, dataset, and solutions and saving it as JSON."
        )
        logger.info(f"Complete Final usecase report generation for query : {query}")
        yield RunResponse(
            run_id=self.run_id,
            content=self.fourthAGENT.run(usercase_json_data.content),
        )


## workflow testing
if __name__ == "__main__":
    from agno.utils.pprint import pprint_run_response

    query = "info on wipro company"
    # Workflow = MRandUseCaseGenerationMultiAgent()
    f = MRTeam(mr_save_response_as_file=mr_research_report)
    s = UseCaseTeam(market_standards_report)
    report = f.run(query)
    pprint_run_response(report, markdown=True, show_time=True)

    report_1 = s.run(report)
    pprint_run_response(report_1, markdown=True, show_time=True)

    # report: RunResponse = Workflow.run(query=query)
    # Print the report
