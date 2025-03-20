from pathlib import Path
from shutil import rmtree
from textwrap import dedent
from typing import Iterator
from agno.workflow import Workflow
from agno.utils.log import logger
from agno.agent import Agent, RunResponse
from Agents.MRTeam import MRTeam
from Agents.UsecaseTeam import UseCaseTeam
from Agents.UsecaseQueryGeneratorAgent import UsecaseQueryGeneratorAgent
from Agents.UseCaseFinderAgent import UseCaseFinderAgent
from agno.utils.pprint import pprint_run_response


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
            message=usecases_report.content, retries=5
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

    query = "info on wipro company"
    # Workflow = MRandUseCaseGenerationMultiAgent()
    f = UseCaseTeam(usecase_save_response_at_file=market_standards_report)
    # s = UseCaseTeam(market_standards_report)
    report = f.run(query)
    pprint_run_response(report, markdown=True, show_time=True)

    # report_1 = s.run(report)
    # pprint_run_response(report_1, markdown=True, show_time=True)

    # report: RunResponse = Workflow.run(query=query)
    # Print the report
