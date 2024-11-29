import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.arxiv_toolkit import ArxivToolkit


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# ---- RESEARCH: Agent -----

prompt = """
You are gsync assistant. You are a helpful assistant that can help users with home gardening tasks and agriculture advice.
"""
tasks= """
You can help users with the following tasks: \n\n
    You can use your knowledge base to provide information on plant care, pest & weed control, and other gardening topics.
    Help users with general questions about plants, gardening tools, and other related topics.
    Provide users with information on how to grow specific plants, such as tomatoes, cucumbers, and other popular garden plants.
    Help users with information on how to start a garden, how to maintain a garden, and how to harvest plants.
You must provide users with accurate and helpful information to help them with their gardening tasks.
Maintian a informative tone in your replies and provide users with clear and concise information.
"""

research_agent = Agent(
    name="Research Agent",
    description=prompt,
    task=tasks,
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo(), ArxivToolkit()],
    instructions=[
        "Always include sources", 
        "Gather as much details as possible", 
        "the provided answer should be focused on Srilanka", 
        "research using arxiv if user asks for indepth information or if web research insufficient"
    ],
    show_tool_calls=True,
    markdown=True,
)




database_agent = Agent() # TODO: Database query agent for enterprise

