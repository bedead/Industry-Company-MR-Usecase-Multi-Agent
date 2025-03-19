import json
from pathlib import Path
import re
from shutil import rmtree
from Agents.WebSearcherAgent import WebSearcherAgent
from Agents.WebArticleScraperAgent import WebArticleScraperAgent
from Agents.MRWriterAgent import MRWriterAgent
from agno.utils.pprint import pprint_run_response

reports_dir = Path(__file__).parent.joinpath("reports")
if reports_dir.is_dir():
    rmtree(path=reports_dir, ignore_errors=True)
reports_dir.mkdir(parents=True, exist_ok=True)
mr_research_report = reports_dir.joinpath("mr_research_report.md")
a1 = WebSearcherAgent()
a2 = WebArticleScraperAgent()
a3 = MRWriterAgent(save_response_at_file=mr_research_report)
topic = "research about vivo mobile company"
response = a1.run(topic)
# print(response)
response1 = a2.run(response.content)

json_string = response1.content.strip()
json_string = re.sub(r"^```json|```$", "", json_string).strip()
parsed_json = json.loads(json_string)

if isinstance(parsed_json, list):
    articles = [
        {
            "title": article["title"],
            "url": article["url"],
            "summary": article.get("summary", None),
            "content": article["content"] if article["content"] != None else None,
        }
        for article in parsed_json
    ]
else:
    raise ValueError("Expected a list of articles, but received a different structure.")

writer_input = {"topic": topic, "articles": articles}  # List of cleaned articles

response2 = a3.run(json.dumps(writer_input, indent=4))
pprint_run_response(response2, markdown=True, show_time=True)
