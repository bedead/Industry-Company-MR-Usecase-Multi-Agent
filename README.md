# Market Research & Use Case Generation Agent

This project is a multi-agent system designed to perform market research and generate AI/ML use cases for specific companies or industries. It leverages advanced AI models and tools to extract, analyze, and present insights in a structured format.

## Features

- **Market Research**: Conducts detailed research on companies or industries, analyzing their market position, strategic focus, and technology adoption.
- **Use Case Generation**: Identifies and prioritizes AI/ML use cases tailored to the business needs of the target company or industry.
- **Resource Discovery**: Searches for relevant datasets, models, and implementation resources on platforms like Kaggle, HuggingFace, and GitHub.
- **Interactive Web App**: Provides a user-friendly interface to run the workflow and view reports in real-time.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bedead/Industry-Company-MR-Usecase-Multi-Agent
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following keys with appropriate values:

     ```
     GEMINI_API_KEY=<your_gemini_api_key>
     TAVILY_API_KEY=<your_tavily_api_key> ## not really required
     KAGGLE_USERNAME=<your_kaggle_username>
     KAGGLE_API_KEY=<your_kaggle_api_key>
     GROQ_API_KEY=<your_groq_api_key> ## not really required
     ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser (usually at `http://localhost:8501`).

3. Enter a company or industry name in the input field and click "Run Workflow" to generate reports.

## Project Structure

- **Agents**: Contains the core logic for various tasks like web scraping, market research, and use case generation.
- **Reports**: Stores the generated reports in markdown and JSON formats.
- **App**: The main entry point for the Streamlit web application.
- **Requirements**: Lists all the dependencies required for the project.

## Reports

The workflow generates the following reports:

1. **Market Research Report**: A detailed analysis of the target company or industry.
2. **Industry Standards Report**: AI/ML use cases and benchmarks for the industry.
3. **Use Case Queries**: JSON file containing search queries for datasets, models, and implementations.
4. **Final Use Case Report**: A comprehensive report with resources for each use case.

## License

This project is not licensed yet.
