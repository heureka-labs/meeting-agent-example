import sys
from agents import MeetingPreparationAgents, StreamToExpander
from tasks import MeetingPreparationTasks
from crewai import Crew
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_icon="📅", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 24px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class MeetingCrew:

    def __init__(self, participants, context, objective):
        self.participants = participants
        self.context = context
        self.objective = objective
        self.output_placeholder = st.empty()

    def run(self):
        crew = self.setup(self.participants, self.context, self.objective)
        result = crew.kickoff()
        self.output_placeholder.markdown(result)

        return result

    def setup(self, participants, context, objective):
        tasks = MeetingPreparationTasks()
        agents = MeetingPreparationAgents()

        # Create Agents
        researcher_agent = agents.research_agent()
        industry_analyst_agent = agents.industry_analysis_agent()
        meeting_strategy_agent = agents.meeting_strategy_agent()
        summary_and_briefing_agent = agents.summary_and_briefing_agent()

        # Create Tasks
        research = tasks.research_task(researcher_agent, participants, context)
        industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, participants, context)
        meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context, objective)
        summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context, objective)

        meeting_strategy.context = [research, industry_analysis]
        summary_and_briefing.context = [research, industry_analysis, meeting_strategy]

        # Create Crew responsible for Copy
        crew = Crew(
            agents=[
                researcher_agent,
                industry_analyst_agent,
                meeting_strategy_agent,
                summary_and_briefing_agent
            ],
            tasks=[
                research,
                industry_analysis,
                meeting_strategy,
                summary_and_briefing
            ],
            verbose=True
        )

        return crew


if __name__ == "__main__":
    icon("📅 Prep a Meeting")

    st.subheader("Let AI agents plan your next meeting!",
                 divider="rainbow", anchor=False)

    with st.sidebar:
        st.header("👇 Enter your meeting details")
        with st.form("my_form"):
            participants = st.text_input("What are the emails for the participants (other than you) in the meeting?", placeholder="klaus@company.org")
            context = st.text_input("What is the context of the meeting?", placeholder="Important Strategy")
            objective = st.text_input("What is your objective for this meeting?", placeholder="Be aligned")

            submitted = st.form_submit_button("Submit")

        st.divider()

        st.sidebar.info("Start with airouter.io", icon="👇")
        st.sidebar.markdown(
            """
        <a href="https://airouter.io" target="_blank">
            <img src="https://airouter.io/assets/images/logo-mini.svg" alt="airouter" style="width:50px;"/>
        </a>
        """,
            unsafe_allow_html=True
        )


if submitted:
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=500, border=False):
            sys.stdout = StreamToExpander(st)
            meeting_crew = MeetingCrew(participants, context, objective)
            result = meeting_crew.run()
        status.update(label="✅ Meeting Plan Ready!",
                      state="complete", expanded=False)

    st.subheader("Here is your Meeting Plan", anchor=False, divider="rainbow")
    st.markdown(result)
