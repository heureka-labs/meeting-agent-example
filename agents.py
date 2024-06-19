import re
from textwrap import dedent
from crewai import Agent
import streamlit as st

from tools.ExaSearchTool import ExaSearchTool


class MeetingPreparationAgents():
    def research_agent(self):
        return Agent(
            role='Research Specialist',
            goal='Conduct thorough research on people and companies involved in the meeting',
            tools=ExaSearchTool.tools(),
            backstory=dedent("""\
					As a Research Specialist, your mission is to uncover detailed information
					about the individuals and entities participating in the meeting. Your insights
					will lay the groundwork for strategic meeting preparation."""),
            verbose=True
        )

    def industry_analysis_agent(self):
        return Agent(
            role='Industry Analyst',
            goal='Analyze the current industry trends, challenges, and opportunities',
            tools=ExaSearchTool.tools(),
            backstory=dedent("""\
					As an Industry Analyst, your analysis will identify key trends,
					challenges facing the industry, and potential opportunities that
					could be leveraged during the meeting for strategic advantage."""),
            verbose=True
        )

    def meeting_strategy_agent(self):
        return Agent(
            role='Meeting Strategy Advisor',
            goal='Develop talking points, questions, and strategic angles for the meeting',
            tools=ExaSearchTool.tools(),
            backstory=dedent("""\
					As a Strategy Advisor, your expertise will guide the development of
					talking points, insightful questions, and strategic angles
					to ensure the meeting's objectives are achieved."""),
            verbose=True
        )

    def summary_and_briefing_agent(self):
        return Agent(
            role='Briefing Coordinator',
            goal='Compile all gathered information into a concise, informative briefing document',
            tools=ExaSearchTool.tools(),
            backstory=dedent("""\
					As the Briefing Coordinator, your role is to consolidate the research,
					analysis, and strategic insights."""),
            verbose=True
        )


class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange', 'violet']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Research Specialist" in cleaned_data:
            # Apply different color
            cleaned_data = cleaned_data.replace("Research Specialist", f":{self.colors[self.color_index]}[Research Specialist]")
        if "Industry Analyst" in cleaned_data:
            cleaned_data = cleaned_data.replace("Industry Analyst", f":{self.colors[self.color_index]}[Industry Analyst]")
        if "Meeting Strategy Advisor" in cleaned_data:
            cleaned_data = cleaned_data.replace("Meeting Strategy Advisor", f":{self.colors[self.color_index]}[Meeting Strategy Advisor]")
        if "Briefing Coordinator" in cleaned_data:
            cleaned_data = cleaned_data.replace("Briefing Coordinator", f":{self.colors[self.color_index]}[Briefing Coordinator]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []
