from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import VisionTool, FileReadTool

from .tools.video_tools import extract_video_data

@CrewBase
class CrewaiVideoStudyGuideCrew():
	"""CrewaiVideoStudyGuide crew"""

	@agent
	def video_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['video_engineer'],
			tools=[extract_video_data],
			verbose=True,
			allow_delegation=False
		)

	@agent
	def content_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_analyzer'],
			tools=[VisionTool()],
			verbose=False,
			allow_delegation=False,
			max_iter=3,
			max_execution_time=300
		)

	@agent
	def note_synthesizer(self) -> Agent:
		return Agent(
			config=self.agents_config['note_synthesizer'],
			tools=[FileReadTool()],
			verbose=False,
			allow_delegation=False,
			max_iter=2,
			max_execution_time=300
		)

	@task
	def extract_task(self) -> Task:
		return Task(
			config=self.tasks_config['extract_task'],
			agent=self.video_engineer()
		)

	@task
	def analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['analysis_task'],
			agent=self.content_analyzer(),
			context=[self.extract_task()]
		)

	@task
	def synthesis_task(self) -> Task:
		return Task(
			config=self.tasks_config['synthesis_task'],
			agent=self.note_synthesizer(),
			context=[self.extract_task(), self.analysis_task()],
			output_file='final_study_guide.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiVideoStudyGuide crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=False,
			full_output=True,
			max_rpm=15,
			memory=False
		)