from agno.agent import Agent
from agno.models.google.gemini import Gemini
from llm_utils import get_google_api_key


"""
instructions=[
            "Given a company name or industry, conduct thorough research to understand its business model, market position, and strategic focus areas.",
            "Perform a detailed search for recent company information, including key products/services, target markets, primary business objectives, and any notable technology initiatives.",
            "Identify the industry segment(s) the company operates in (e.g., Automotive, Manufacturing, Finance, Retail, Healthcare, etc.) and highlight emerging trends in that sector.",
            "Analyze the company's strategic initiatives, particularly those related to digital transformation, AI adoption, and technology integration.",
            "Research the company's current pain points, operational challenges, and areas where they are seeking efficiency improvements.",
            "Assess the company's customer experience strategies, including how they leverage technology in customer interactions and automation.",
            "Identify the company's key competitors and conduct a comparative analysis of their technology adoption, competitive edge, and innovation strategies.",
            "Where applicable, refer to industry-specific reports and insights from sources like McKinsey, Deloitte, Nexocode, and other reputable market research firms for AI and digital transformation trends.",
            "Structure the findings into a well-organized report with clear sections: Company Overview, Industry Classification, Key Offerings, Strategic Focus Areas, Current Technology Usage, and Operational Challenges.",
            "Ensure that all paragraphs has at least one sources of information, and URLs for the sources should be included at the end of each relevant paragraph in proper formatting (e.g., [Source](URL)).",
            "If information about the company is scarce, focus on broader industry trends, market shifts, and general challenges faced by similar businesses in the sector.",
            "Gather information from diverse and credible sources, including annual reports, company press releases, industry analyses, and reputable business publications.",
            "Search for 10-15 sources and identify the 5-7 most authoritative and relevant ones and balanced analysis before compiling the final report.",
        ],
"""


def MRWriterAgent(save_response_at_file: str) -> Agent:
    industry_research_agent: Agent = Agent(
        name="Market Research Writer Agent",
        model=Gemini(id="gemini-1.5-flash", api_key=get_google_api_key()),
        description="You are an expert industry research writer specializing in synthesizing market insights, competitive analysis, and AI adoption trends into structured reports.",
        instructions=[
            "Given the research findings on a company or industry, synthesize the information into a well-structured and insightful report.",
            "Organize content into clear sections, including: Company Overview, Industry Classification, Key Offerings, Strategic Focus Areas, Current Technology Usage, Operational Challenges, and AI Adoption Trends.",
            "Ensure logical flow and coherence, maintaining a professional tone and precise industry terminology.",
            "Where applicable, integrate references to industry-specific reports and insights from authoritative sources such as McKinsey, Deloitte, Nexocode, and leading business publications.",
            "Cite all referenced data, statistics, and insights using proper in-text citations, with URLs included at the end of relevant paragraphs (e.g., [Source](URL)).",
            "Highlight competitive benchmarks by summarizing how key competitors leverage AI and digital transformation strategies.",
            "Incorporate key findings on emerging trends and industry-wide shifts, emphasizing real-world applications of AI/ML technologies.",
            "If direct company-specific insights are limited, expand the analysis by referencing broader industry trends and comparable case studies.",
            "Ensure a balanced perspective by summarizing multiple credible sources while avoiding speculation or opinion-based conclusions.",
            "Present all information in a clean, well-structured format with clear section headers and bullet points where applicable to enhance readability.",
        ],
        # show_tool_calls=True,
        expected_output="Comprehensive analysis of companies and their market segments report in markdown format",
        debug_mode=True,
        save_response_to_file=save_response_at_file,
        markdown=True,
    )

    return industry_research_agent
