from agno.agent import Agent
from agno.models.google.gemini import Gemini
from utils import get_google_api_key
from textwrap import dedent

"""
instructions=[
            "Using the provided industry research, analyze the latest AI/ML adoption trends specific to this sector, ensuring references to credible sources where applicable.",
            "Conduct targeted searches for industry-specific AI applications, using queries like 'how is the retail industry leveraging AI and ML' or 'AI applications in automotive manufacturing'.",
            "Identify benchmark standards and best practices for AI implementation in this industry, citing authoritative reports from McKinsey, Deloitte, Gartner, or Nexocode wherever possible.",
            "Compare the company's current technology adoption against industry benchmarks to highlight gaps and potential opportunities.",
            "Generate at least 8 well-defined AI/ML use cases addressing the company's pain points and strategic goals, backed by real-world industry applications.",
            "For each use case, clearly define: (1) The business problem being solved, (2) The AI/ML approach recommended, (3) Expected business impact, (4) Implementation complexity.",
            "Prioritize use cases based on a weighted scoring system: Business Impact (60%) and Implementation Feasibility (40%).",
            "Categorize each use case by functional area (e.g., Operations, Supply Chain, Customer Experience, Marketing, Finance, etc.).",
            "For each use case, identify the most relevant GenAI and ML technologies (e.g., LLMs, Computer Vision, Predictive Analytics, NLP) and reference any successful implementations from industry leaders.",
            "Tag use cases with relevant keywords to facilitate efficient resource matching in subsequent stages.",
            "Provide a comparative analysis of how competitors or industry leaders are leveraging similar AI solutions, linking to case studies or research articles where applicable.",
            "Organize all findings into a structured format with clear sections, priority scores, and categorization.",
            "Focus on practical, implementable AI solutions rather than theoretical concepts.",
            "Include estimated timeframes for implementation (Short-term: 0-6 months, Medium-term: 6-12 months, Long-term: 12+ months) with supporting industry case studies where available.",
            "Ensure all sources are properly cited, adding URLs at the end of relevant paragraphs in proper markdown format (e.g., [Source](URL)).",
            "Perform at least 6 distinct searches related to AI adoption in this specific industry before finalizing the report.",
        ],
"""


def UsecaseWriter(save_response_at_file) -> Agent:
    market_standards_agent: Agent = Agent(
        name="UsecaseWriter",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        # tools=[TavilyTools()],
        instructions=dedent(
            """
            - Analyze AI/ML applications, industry benchmarks, and case studies from scraped content.
            - Identify benchmark standards and best practices** for AI adoption in the given industry.
            - Compare the company's current technology adoption** against industry benchmarks to highlight gaps and opportunities.
            - Generate at least 8 well-defined AI/ML use cases**, each including:
            1. Business problem being solved
            2. AI/ML approach recommended
            3. Expected business impact
            4. Implementation complexity
            - Prioritize use cases based on:
            - Business Impact (60%)
            - Implementation Feasibility (40%)
            - Categorize use cases by functional area (e.g., Operations, Supply Chain, Marketing, etc.).
            - Identify the most relevant AI/ML technologies for each use case (e.g., LLMs, Computer Vision, NLP).
            - **Tag use cases with relevant keywords** to enable efficient resource matching.
            - Compare how competitors or industry leaders use AI for similar solutions.
            - Provide estimated implementation timeframes:
            - Short-term (0-6 months)
            - Medium-term (6-12 months)
            - Long-term (12+ months)
            - Structure the final report logically with clear sections and priority scoring.            
        """
        ),
        description="You are an AI adoption trend analyst and Writer specializing in identifying industry-specific AI applications and generating high-impact use cases.",
        # debug_mode=True,
        save_response_to_file=save_response_at_file,
        markdown=True,
    )
    return market_standards_agent
