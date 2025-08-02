"""City Assistant agent system: orchestration agent and subagents."""

import logging
from agents import Agent, handoff, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters

from app.cores.tools import city_facts_tool, weather_tool, time_tool
from app.schemas.schemas import HandoffInfo


# Setup logger
logger = logging.getLogger("cityassistant.agent")


class CityAssistantAgent:
    """
    CityAssistantAgent manages the orchestration agent, including
    the city summary and trip discussion subagents.

    :param model: Language model to use (default "gpt-4o-mini").
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        logger.info("Initializing CityAssistantAgent with model %s", self.model)
        self.city_summary_agent = self._build_city_summary_agent()
        self.trip_discussion_agent = self._build_trip_discussion_agent()
        self.agent = self._build_orchestration_agent()

    @staticmethod
    async def on_handoff(ctx: RunContextWrapper[None], input_data: HandoffInfo):
        """
        Called when the orchestrator delegates to a subagent.

        :param ctx: RunContextWrapper instance.
        :param input_data: HandoffInfo instance with handoff metadata.
        """
        logger.info(
            f"Handoff to '{input_data.subagent_name}' because '{input_data.reason}'"
        )

    def _build_city_summary_agent(self) -> Agent:
        """Create the city summary agent."""
        logger.debug("Building CitySummaryAgent.")
        agent = Agent(
            name="City summary agent",
            instructions="""
            You are a city information assistant. 
            Fetch information using following tools: cit_facts_tool, weather_tool, time_tool
            Reply in one line, and always end with a question.
            Output format:
            {
                "thinking": "Explain reasoning",
                "function_calls": [
                    { "tool": "tool name (without functions.)", "parameters": { ... tool input ... } },
                    ...
                ],
                "response": "response in one line, and end with a question"
            }
            Only answer question related to your task.
            """,
            tools=[city_facts_tool, weather_tool, time_tool],
            model=self.model,
        )
        return agent

    def _build_trip_discussion_agent(self) -> Agent:
        """Create the trip discussion agent."""
        logger.debug("Building TripDiscussionAgent.")
        agent = Agent(
            name="Trip discussion agent",
            instructions="""
            You are a travel planning assistant. 
            Discuss ideas to plan a trip.
            Be very brief. less than 100 words.
            Output format:
            {
                "thinking": "Explain reasoning",
                "function_calls": [
                    { "tool": "tool name", "parameters": { ... tool input ... } },
                    ...
                ],
                "response": "response here"
            }
            If no tools are used function_calls is [].
            Only answer question related to your task.
            """,
            model=self.model,
        )
        return agent

    def _build_orchestration_agent(self) -> Agent:
        """Create the orchestration agent."""
        logger.debug("Building OrchestrationAgent.")
        agent = Agent(
            name="Orchestration agent",
            tools=[city_facts_tool, weather_tool, time_tool],
            handoffs=[
                handoff(
                    self.city_summary_agent,
                    on_handoff=self.on_handoff,
                    input_type=HandoffInfo,
                    input_filter=handoff_filters.remove_all_tools,
                ),
                handoff(
                    self.trip_discussion_agent,
                    on_handoff=self.on_handoff,
                    input_type=HandoffInfo,
                    input_filter=handoff_filters.remove_all_tools,
                ),
            ],
            instructions=RECOMMENDED_PROMPT_PREFIX
            + """
            Your only job is to decide which subagent should handle the request.

            - If the user asks about a city, always delegate to the City summary agent.
            - If the user wants advice, discussion, or planning for a trip, always delegate to the Trip discussion agent.
            - Never answer questions yourself, only handoff to subagents.
            """,
            model=self.model,
        )
        return agent

    def get(self) -> Agent:
        """
        Returns the main orchestration agent for API usage.

        :return: The orchestration agent.
        """
        logger.debug("Returning CityAssistantAgent.")
        return self.agent
