import json
from pathlib import Path
from typing import Dict, Optional
from Agents.WebSearcherAgent import WebSearcherAgent, SearchResults
from Agents.WebArticleScraperAgent import WebArticleScraperAgent, ScrapedArticle
from Agents.MRWriterAgent import MRWriterAgent
from agno.utils.pprint import pprint_run_response

reports_dir = Path(__file__).parent.joinpath("reports")
mr_research_report = reports_dir.joinpath("mr_research_report.md")
a1 = WebSearcherAgent()
a2 = WebArticleScraperAgent()
a3 = MRWriterAgent(save_response_at_file=mr_research_report)
topic = "research about vivo mobile company"
response: Optional[SearchResults] = a1.run(topic)
print(response)
# response1: Dict[str, ScrapedArticle] = a2.run(response)

# # Prepare the input for the writer
# writer_input = {
#     "topic": topic,
#     "articles": [v.model_dump() for v in response1.values()],
# }
# # Run the writer and yield the response
# response2 = a3.run(json.dumps(writer_input, indent=4))

# pprint_run_response(response2, markdown=True, show_time=True)
