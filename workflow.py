from pathlib import Path
from shutil import rmtree
from typing import Iterator
from agno.workflow import Workflow
from agno.utils.log import logger
from agno.agent import Agent, RunResponse
from Agents.MRWriterAgent import MRWriterAgent
from Agents.AITrendAnalystAgent import AITrendAnalystAgent
from Agents.UsecaseQueryGeneratorAgent import UsecaseQueryGeneratorAgent
from Agents.UseCaseFinderAgent import UseCaseFinderAgent

reports_dir = Path(__file__).parent.joinpath("reports")
if reports_dir.is_dir():
    rmtree(path=reports_dir, ignore_errors=True)
reports_dir.mkdir(parents=True, exist_ok=True)
mr_research_report = str(reports_dir.joinpath("mr_research_report.md"))
market_standards_report = str(reports_dir.joinpath("market_standards_report.md"))
resource_usecase_queries = str(reports_dir.joinpath("resource_usecase_queries.json"))
final_usecase_report = str(reports_dir.joinpath("final_usecase_report.md"))


class MRandUseCaseGenerationMultiAgent(Workflow):
    """Advanced workflow for generating Market research report and comapany/industry specific usecase with advanced model, datasets, and example reterival."""

    name = "Market Research and Usecase Generation Multi-Agent"
    description = "Advanced workflow for generating Market research report and comapany/industry specific usecase with advanced model, datasets, and example reterival."

    mr_research_agent = MRWriterAgent(save_response_at_file=mr_research_report)
    ai_trends_analyst_agent = AITrendAnalystAgent(
        save_response_at_file=market_standards_report
    )
    usecase_query_generator_agent = UsecaseQueryGeneratorAgent(
        save_response_at_file=resource_usecase_queries
    )
    usecase_finder_agent = UseCaseFinderAgent(
        save_response_at_file=final_usecase_report
    )

    def run(self, query: str) -> Iterator[RunResponse]:
        logger.info(f"Researching about: {query}")
        mr_report: RunResponse = self.mr_research_agent.run(query)
        if mr_report is None or not mr_report.content:
            yield RunResponse(
                run_id=self.run_id,
                content="Sorry, could not research about this company/industry.",
            )
            return
        else:
            yield RunResponse(run_id=self.run_id, content=mr_report.content)

        logger.info("Looking for industry-specific AI applications usecases.")
        usecases_report: RunResponse = self.ai_trends_analyst_agent.run(
            mr_report.content
        )
        if usecases_report is None or not usecases_report.content:
            yield RunResponse(
                run_id=self.run_id,
                content="Sorry, could not get the industry specific usecase report.",
            )
            return
        else:
            yield RunResponse(run_id=self.run_id, content=usecases_report.content)

        logger.info(
            "Generating usecase specific keywords to look for relavant models, dataset, and solutions and saving it as JSON."
        )
        usercase_json_data: RunResponse = self.usecase_query_generator_agent.run(
            usecases_report.content
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
            content=self.usecase_finder_agent.run(usercase_json_data.content),
        )


## workflow testing
if __name__ == "__main__":
    from agno.utils.pprint import pprint_run_response

    query = input("You :")
    workflow = MRandUseCaseGenerationMultiAgent()

    report: RunResponse = workflow.run(query=query)
    # Print the report
    pprint_run_response(report, markdown=True, show_time=True)
