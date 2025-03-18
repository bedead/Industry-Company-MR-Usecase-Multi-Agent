from typing import List, Dict, Any, Optional
from agno.tools import Toolkit
from agno.utils.log import logger


class AIResourceTools(Toolkit):
    def __init__(
        self, kaggle_username: Optional[str] = None, kaggle_key: Optional[str] = None
    ):
        super().__init__(name="ai_resource_tools")
        self.kaggle_username = kaggle_username
        self.kaggle_key = kaggle_key

        # Register all the search methods
        self.register(self.search_kaggle_datasets)
        self.register(self.search_huggingface)
        self.register(self.search_github_repos)
        self.register(self.verify_url)

    def _setup_kaggle_api(self):
        """Sets up the Kaggle API with authentication."""
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            api = KaggleApi()

            # Use provided credentials or from environment
            if self.kaggle_username and self.kaggle_key:
                import os

                os.environ["KAGGLE_USERNAME"] = self.kaggle_username
                os.environ["KAGGLE_KEY"] = self.kaggle_key

            api.authenticate()
            return api
        except Exception as e:
            logger.warning(f"Failed to authenticate with Kaggle: {e}")
            return None

    def search_kaggle_datasets(
        self, query: str, max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for datasets on Kaggle based on a query.

        Args:
            query (str): The search query for datasets
            max_results (int): Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of dataset information dictionaries
        """
        try:
            api = self._setup_kaggle_api()
            if not api:
                return [{"error": "Failed to authenticate with Kaggle API"}]

            logger.info(f"Searching Kaggle for datasets: {query}")
            datasets = api.dataset_list(search=query)

            results = []
            for i, dataset in enumerate(datasets):
                if i >= max_results:
                    break

                # print(dataset)
                # print("===================")

                # Extract dataset information
                dataset_info = {
                    "title": dataset.title,
                    "url": dataset.url,
                    "owner": dataset.owner_name,
                    "size": self._format_size(dataset.total_bytes),
                    "last_updated": str(dataset.last_updated),
                    "download_count": dataset.download_count,
                    "description": (
                        dataset.description[:200] + "..."
                        if dataset.description and len(dataset.description) > 200
                        else dataset.description or "No description available"
                    ),
                    "tags": dataset.tags if hasattr(dataset, "tags") else [],
                    "license": (
                        dataset.license_name
                        if hasattr(dataset, "licenseName")
                        else "Not specified"
                    ),
                }
                results.append(dataset_info)

            logger.info(f"Found {len(results)} Kaggle datasets for query: {query}")
            return results

        except Exception as e:
            logger.warning(f"Error searching Kaggle datasets: {e}")
            return [{"error": f"Failed to search Kaggle: {str(e)}"}]

    def search_huggingface(
        self, query: str, model_type: str = "all", max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for models or datasets on HuggingFace.

        Args:
            query (str): The search query
            model_type (str): Type of resource ('model', 'dataset', or 'all')
            max_results (int): Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of resource information dictionaries
        """
        try:
            import requests

            logger.info(f"Searching HuggingFace for {model_type}: {query}")

            # Set up the search endpoints
            endpoints = []
            if model_type == "model" or model_type == "all":
                endpoints.append("models")
            if model_type == "dataset" or model_type == "all":
                endpoints.append("datasets")

            results = []
            for endpoint in endpoints:
                url = f"https://huggingface.co/api/{endpoint}?search={query}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    for item in data[:max_results]:
                        # Extract resource information
                        item_info = {
                            "type": endpoint[:-1],  # Remove 's' to get singular form
                            "name": item.get("modelId") or item.get("id"),
                            "url": f"https://huggingface.co/{item.get('modelId') or item.get('id')}",
                            "author": item.get("author") or "Unknown",
                            "last_modified": item.get("lastModified", "Unknown"),
                            "downloads": item.get("downloads", "Unknown"),
                            "likes": item.get("likes", 0),
                            "tags": item.get("tags", []),
                            "description": (
                                item.get("description", "No description available")[
                                    :200
                                ]
                                + "..."
                                if item.get("description")
                                and len(item.get("description")) > 200
                                else item.get("description")
                                or "No description available"
                            ),
                        }
                        results.append(item_info)

            logger.info(
                f"Found {len(results)} HuggingFace resources for query: {query}"
            )
            return results[:max_results]

        except Exception as e:
            logger.warning(f"Error searching HuggingFace: {e}")
            return [{"error": f"Failed to search HuggingFace: {str(e)}"}]

    def search_github_repos(
        self, query: str, max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for repositories on GitHub.

        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of repository information dictionaries
        """
        try:
            import requests

            logger.info(f"Searching GitHub for repositories: {query}")

            # GitHub search API
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                results = []

                for repo in data.get("items", [])[:max_results]:
                    # Extract repository information
                    repo_info = {
                        "name": repo.get("full_name"),
                        "url": repo.get("html_url"),
                        "description": (
                            repo.get("description")[:200] + "..."
                            if repo.get("description")
                            and len(repo.get("description")) > 200
                            else repo.get("description") or "No description available"
                        ),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "language": repo.get("language"),
                        "last_updated": repo.get("updated_at"),
                        "license": (
                            repo.get("license", {}).get("name")
                            if repo.get("license")
                            else "Not specified"
                        ),
                    }
                    results.append(repo_info)

                logger.info(
                    f"Found {len(results)} GitHub repositories for query: {query}"
                )
                return results
            else:
                return [
                    {"error": f"GitHub API returned status code {response.status_code}"}
                ]

        except Exception as e:
            logger.warning(f"Error searching GitHub repositories: {e}")
            return [{"error": f"Failed to search GitHub: {str(e)}"}]

    def verify_url(self, url: str) -> Dict[str, Any]:
        """
        Verify if a URL is accessible.

        Args:
            url (str): The URL to verify

        Returns:
            Dict[str, Any]: Status information for the URL
        """
        try:
            import requests

            logger.info(f"Verifying URL: {url}")

            response = requests.head(url, timeout=10)

            result = {
                "url": url,
                "status_code": response.status_code,
                "accessible": response.status_code < 400,
                "reason": response.reason,
            }

            logger.info(f"URL verification result: {result}")
            return result

        except Exception as e:
            logger.warning(f"Error verifying URL {url}: {e}")
            return {
                "url": url,
                "status_code": None,
                "accessible": False,
                "reason": str(e),
            }

    def format_resources_markdown(
        self,
        use_case: str,
        datasets: List[Dict[str, Any]],
        implementations: List[Dict[str, Any]],
    ) -> str:
        """
        Format resources into a well-structured markdown document.

        Args:
            use_case (str): The name of the use case
            datasets (List[Dict[str, Any]]): List of dataset information
            implementations (List[Dict[str, Any]]): List of implementation resources

        Returns:
            str: Formatted markdown text
        """
        markdown = f"## Use Case: {use_case}\n\n"

        # Add datasets section
        markdown += "**Datasets:**\n\n"
        for i, dataset in enumerate(datasets, 1):
            markdown += f"{i}. **{dataset.get('title') or dataset.get('name')}**\n"
            markdown += f"   * **Source Platform:** {dataset.get('type', 'Kaggle') if 'type' in dataset else 'Kaggle'}\n"
            markdown += f"   * **URL:** [{dataset.get('url')}]({dataset.get('url')})\n"
            markdown += f"   * **Description:** {dataset.get('description')}\n"

            # Add features/statistics
            stats = []
            if "size" in dataset:
                stats.append(f"Size: {dataset['size']}")
            if "download_count" in dataset:
                stats.append(f"Downloads: {dataset['download_count']}")
            if "last_updated" in dataset:
                stats.append(f"Last updated: {dataset['last_updated']}")

            markdown += f"   * **Key Features/Statistics:** {', '.join(stats)}\n"
            markdown += (
                f"   * **License:** {dataset.get('license', 'Not specified')}\n\n"
            )

        # Add implementations section
        markdown += "**Implementation Resources:**\n\n"
        for i, impl in enumerate(implementations, 1):
            markdown += f"{i}. **{impl.get('name')}**\n"
            source = (
                "GitHub"
                if "github.com" in impl.get("url", "")
                else (
                    "HuggingFace"
                    if "huggingface.co" in impl.get("url", "")
                    else "Other"
                )
            )
            markdown += f"   * **Source Platform:** {source}\n"
            markdown += f"   * **URL:** [{impl.get('url')}]({impl.get('url')})\n"
            markdown += f"   * **Description:** {impl.get('description')}\n"

            # Add features/statistics
            stats = []
            if "stars" in impl:
                stats.append(f"Stars: {impl['stars']}")
            if "forks" in impl:
                stats.append(f"Forks: {impl['forks']}")
            if "language" in impl and impl["language"]:
                stats.append(f"Language: {impl['language']}")
            if "last_updated" in impl or "last_modified" in impl:
                stats.append(
                    f"Last updated: {impl.get('last_updated') or impl.get('last_modified')}"
                )

            markdown += f"   * **Key Features/Statistics:** {', '.join(stats)}\n"
            markdown += f"   * **License:** {impl.get('license', 'Not specified')}\n\n"

        return markdown

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes into a readable size."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024 or unit == "TB":
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
