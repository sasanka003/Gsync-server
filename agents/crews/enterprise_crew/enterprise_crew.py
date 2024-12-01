from crewai import Agent, Crew, Process, Task
from crewai import LLM
from crewai.project import CrewBase, agent, crew, task, after_kickoff, before_kickoff
from crewai_tools import SerperDevTool
from crewai_tools import EXASearchTool
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
llm = LLM(model="gpt-4o", temperature=0.2)

@CrewBase
class EnterpriseAnalystCrew():
  """Enterprise data crew"""

  @before_kickoff
  def before_kickoff_function(self, inputs):
    print(f"Before kickoff function with inputs: {inputs}")
    return inputs 
  
  @agent
  def data_engineer(self) -> Agent:
    return Agent(
      config=self.agents_config['data_engineer'],
      verbose=True,
      llm=llm,
      tools=[SerperDevTool()]
    )

  @agent
  def financial_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['financial_analyst'],
      verbose=True,
      llm=llm,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'],
      llm=llm,
      verbose=True
    )
  
  @task
  def data_task(self) -> Task:
    return Task(
      config=self.tasks_config['data_task'],
    )

  @task
  def financial_task(self) -> Task:
    return Task(
      config=self.tasks_config['financial_task'],
    )

  @task
  def reporting_task(self) -> Task:
    return Task(
      config=self.tasks_config['reporting_task'],
    )

  @crew
  def crew(self) -> Crew:
    """Creates the LatestAiDevelopment crew"""
    return Crew(
      agents=self.agents, 
      tasks=self.tasks, 
      process=Process.sequential,
      verbose=True,
    )
  
  @after_kickoff
  def after_kickoff_function(self, result):
    print(f"After kickoff function with result: {result}")
    return result 
