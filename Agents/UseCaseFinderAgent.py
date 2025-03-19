import json
from pathlib import Path
import re
from shutil import rmtree
from agno.agent import RunResponse

from utils import get_kaggle_username, get_kaggle_api_key
from Agents.AIResourceToolKit import AIResourceTools


class UseCaseFinderAgent:
    def __init__(self, save_response_at_file: str):
        self.save_response_at_file = save_response_at_file

    def run(self, json_data):
        ## call CustomSearchAgent(with each search query followed by where to search)
        ## e.g search client onboarding data in kaggle, iteratively till all the kaggle search fields are searched,
        ## same for huggingface and github
        try:
            # If json_data is already a dictionary, use it directly
            if isinstance(json_data, dict):
                use_cases = json_data
            else:
                # Clean the string to remove any markdown code block markers or extra characters
                if isinstance(json_data, str):
                    # Remove markdown code block markers if present
                    json_pattern = r"```json\s*([\s\S]*?)\s*```"
                    match = re.search(json_pattern, json_data)
                    if match:
                        clean_json = match.group(1)
                    else:
                        clean_json = json_data

                    # Strip any extra whitespace
                    clean_json = clean_json.strip()

                    # Parse the JSON
                    use_cases = json.loads(clean_json)
                else:
                    raise TypeError("json_data must be a string or dictionary")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(
                f"JSON data received: {json_data[:100]}..."
            )  # Print the first 100 chars for debugging
            # Create a minimal structure to continue processing
            use_cases = {"use_cases": []}

        # Initialize AIResourceTools
        search_tool = AIResourceTools(
            kaggle_username=get_kaggle_username(), kaggle_key=get_kaggle_api_key()
        )

        # Initialize the markdown report
        report = "# AI/ML Resources for Use Cases\n\n"

        # Process each use case
        for use_case in use_cases["use_cases"]:
            uc_id = use_case["id"]
            uc_title = use_case["title"]

            report += f"## {uc_id}: {uc_title}\n\n"

            # Search Kaggle datasets
            report += "### Kaggle Datasets\n\n"
            kaggle_results = []
            for query in use_case["search_queries"]["kaggle"]:
                results = search_tool.search_kaggle_datasets(query, max_results=2)
                kaggle_results.extend(results)

            # Remove duplicates based on URL
            unique_kaggle = {}
            for result in kaggle_results:
                if "error" not in result and result.get("url") not in unique_kaggle:
                    unique_kaggle[result.get("url")] = result

            if unique_kaggle:
                for url, dataset in unique_kaggle.items():
                    status = "✅ Verified"

                    report += f"#### [{dataset['title']}]({url}) {status}\n\n"
                    report += f"- **Owner:** {dataset['owner']}\n"
                    report += f"- **Size:** {dataset['size']}\n"
                    report += f"- **Last Updated:** {dataset['last_updated']}\n"
                    report += f"- **Downloads:** {dataset['download_count']}\n"
                    report += f"- **License:** {dataset['license']}\n"
                    report += f"- **Description:** {dataset['description']}\n\n"
            else:
                report += "No relevant datasets found on Kaggle.\n\n"

            # Search HuggingFace models and datasets
            report += "### HuggingFace Resources\n\n"
            hf_results = []
            for query in use_case["search_queries"]["huggingface"]:
                model_results = search_tool.search_huggingface(
                    query, model_type="model", max_results=2
                )
                dataset_results = search_tool.search_huggingface(
                    query, model_type="dataset", max_results=2
                )
                hf_results.extend(model_results + dataset_results)

            # Remove duplicates based on URL
            unique_hf = {}
            for result in hf_results:
                if "error" not in result and result.get("url") not in unique_hf:
                    unique_hf[result.get("url")] = result

            if unique_hf:
                for url, resource in unique_hf.items():
                    # Verify URL
                    verification = search_tool.verify_url(url)
                    status = (
                        "✅ Verified"
                        if verification["accessible"]
                        else "❌ Not accessible"
                    )

                    resource_type = resource.get("type", "Resource")
                    report += f"#### [{resource['name']}]({url}) ({resource_type.capitalize()}) {status}\n\n"
                    report += f"- **Author:** {resource['author']}\n"
                    report += f"- **Last Modified:** {resource['last_modified']}\n"
                    report += f"- **Downloads:** {resource['downloads']}\n"
                    report += f"- **Likes:** {resource['likes']}\n"
                    report += f"- **Tags:** {', '.join(resource['tags']) if resource.get('tags') else 'None'}\n"
                    report += f"- **Description:** {resource['description']}\n\n"
            else:
                report += "No relevant resources found on HuggingFace.\n\n"

            # Search GitHub repositories
            report += "### GitHub Repositories\n\n"
            github_results = []
            for query in use_case["search_queries"]["github"]:
                results = search_tool.search_github_repos(query, max_results=2)
                github_results.extend(results)

            # Remove duplicates based on URL
            unique_github = {}
            for result in github_results:
                if "error" not in result and result.get("url") not in unique_github:
                    unique_github[result.get("url")] = result

            if unique_github:
                for url, repo in unique_github.items():
                    # Verify URL
                    verification = search_tool.verify_url(url)
                    status = (
                        "✅ Verified"
                        if verification["accessible"]
                        else "❌ Not accessible"
                    )

                    report += f"#### [{repo['name']}]({url}) {status}\n\n"
                    report += f"- **Description:** {repo['description']}\n"
                    report += f"- **Stars:** {repo['stars']}\n"
                    report += f"- **Forks:** {repo['forks']}\n"
                    report += f"- **Language:** {repo['language'] or 'Not specified'}\n"
                    report += f"- **Last Updated:** {repo['last_updated']}\n"
                    report += f"- **License:** {repo['license']}\n\n"
            else:
                report += "No relevant repositories found on GitHub.\n\n"

            report += "---\n\n"

        # Add generation timestamp
        from datetime import datetime

        report += f"\n\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

        # Save the report to a file
        # report_path = "reports/ai_ml_resources_report.md"
        with open(self.save_response_at_file, "w", encoding="utf-8") as f:
            f.write(report)

        return report
