import json
import re
import streamlit as st
import time
from pathlib import Path
from agno.utils.log import logger
from agno.agent import RunResponse
from workflow import (
    MRandUseCaseGenerationMultiAgent,
)  # Ensure this is correctly imported

import logging


# Set up logger to capture logs in sidebar
class StreamlitLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        update_logs(log_entry)


# Attach Streamlit log handler to the logger
log_handler = StreamlitLogHandler()
log_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)  # Ensure logger captures INFO level messages

# Initialize Streamlit app
# st.set_page_config(page_title="Multi-Agent AI Research", layout="wide")

# Sidebar for logs
st.sidebar.title("Logs")
log_placeholder = st.sidebar.empty()
log_messages = []


# Function to log messages in the sidebar
def update_logs(message):
    log_messages.append(message)
    log_placeholder.text("\n".join(log_messages[-10:]))  # Show last 10 logs


# UI Components
st.title("Multi-Agent Market Research and Use Case Generation")
st.write("Enter a company or industry name to generate reports.")

query = st.text_input("Enter query:", "Research about vivo mobile company")
run_button = st.button("Run Workflow")

# Define report paths
reports_dir = Path(__file__).parent.joinpath("reports")
mr_research_report = reports_dir.joinpath("mr_research_report.md")
market_standards_report = reports_dir.joinpath("market_standards_report.md")
resource_usecase_queries = reports_dir.joinpath("resource_usecase_queries.json")
final_usecase_report = reports_dir.joinpath("final_usecase_report.md")

# Display area for real-time responses
st.subheader("Live Report Generation")
report_placeholder = st.empty()  # Placeholder for displaying reports
# Run workflow on button click
if run_button and query:
    workflow = MRandUseCaseGenerationMultiAgent()

    with st.spinner("Running workflow..."):
        for idx, response in enumerate(workflow.run(query=query)):
            if isinstance(response, RunResponse):
                # Define report titles
                report_title = [
                    "Market Research Report",
                    "Industry Standards Report",
                    "Use Case Queries (JSON)",
                    "Final Use Case Report",
                ][idx]

                # Define corresponding file paths
                report_file = [
                    mr_research_report,
                    market_standards_report,
                    resource_usecase_queries,
                    final_usecase_report,
                ][idx]

                # Create a bordered container for each report
                with st.container(border=True):
                    st.subheader(report_title)

                    if report_file.suffix == ".md":
                        # Render Markdown correctly in a scrollable text area
                        st.markdown(
                            f"<div style='height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px;'>{response.content}</div><br>",
                            unsafe_allow_html=True,
                        )
                    else:
                        # Handle JSON response parsing
                        try:
                            json_data = response.content

                            if isinstance(json_data, dict):
                                use_cases = json_data
                            else:
                                if isinstance(json_data, str):
                                    # Clean JSON format from markdown code block markers
                                    json_pattern = r"```json\s*([\s\S]*?)\s*```"
                                    match = re.search(json_pattern, json_data)
                                    clean_json = match.group(1) if match else json_data
                                    use_cases = json.loads(clean_json.strip())
                                else:
                                    raise TypeError(
                                        "json_data must be a string or dictionary"
                                    )

                            # Pretty-print JSON and make it scrollable
                            formatted_json = json.dumps(use_cases, indent=4)
                            st.text_area(report_title, formatted_json, height=300)

                        except json.JSONDecodeError as e:
                            st.error(f"Error parsing JSON: {e}")
                            st.text_area(
                                report_title, response.content[:300], height=300
                            )  # Show first 300 chars
                            use_cases = {"use_cases": []}  # Minimal structure fallback

                    # # Display corresponding download button
                    # if report_file.exists():
                    #     with open(report_file, "r", encoding="utf-8") as file:
                    #         content = file.read()

                    #     st.download_button(
                    #         type="primary",
                    #         label=f"Download {report_title}",
                    #         data=content,
                    #         file_name=report_file.name,
                    #         mime=(
                    #             "text/markdown"
                    #             if report_file.suffix == ".md"
                    #             else "application/json"
                    #         ),
                    #     )

                    # time.sleep(0.5)

    st.success("Workflow completed! Check the reports above.")
