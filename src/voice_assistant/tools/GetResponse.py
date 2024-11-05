import asyncio
import logging
from typing import Any, Optional

from agency_swarm import Agency, get_openai_client
from agency_swarm.agents import Agent
from agency_swarm.threads import Thread
from agency_swarm.tools import BaseTool
from openai import OpenAI
from openai.types.beta.threads import TextContentBlock
from pydantic import Field, PrivateAttr, field_validator

from voice_assistant.agencies import AGENCIES, AGENCIES_AND_AGENTS_STRING
from voice_assistant.utils.decorators import timeit_decorator

logger = logging.getLogger(__name__)


class GetResponse(BaseTool):
    """
    Checks the status of a task or retrieves the response from a specific agent within a specified agency.

    Use this tool after initiating a long-running task with 'SendMessageAsync'.
    Use the same parameters you used with 'SendMessageAsync' to check if the task is completed.
    If the task is completed, this tool will return the agent's response.
    If the task is still in progress, it will inform you accordingly.

    Available Agencies and Agents:
    {agency_agents}
    """

    agency_name: str = Field(..., description="The name of the agency.")
    agent_name: Optional[str] = Field(None, description="The name of the agent, or None to use the default agent.")
    _client: OpenAI = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = get_openai_client()

    @field_validator("agency_name", mode="before")
    def validate_agency_name(cls, value: str) -> str:
        if value not in AGENCIES:
            available = ", ".join(AGENCIES.keys())
            raise ValueError(f"Agency '{value}' not found. Available agencies: {available}")
        return value

    @field_validator("agent_name", mode="before")
    def validate_agent_name(cls, value: Optional[str]) -> Optional[str]:
        if value:
            agent_names = [agent.name for agency in AGENCIES.values() for agent in agency.agents]
            if value not in agent_names:
                available = ", ".join(agent_names)
                raise ValueError(f"Agent '{value}' not found. Available agents: {available}")
        return value

    @timeit_decorator
    async def run(self) -> str:
        """
        Executes the GetResponse tool to check task status or retrieve agent response.

        Returns:
            str: The result message based on the task status.
        """
        agency = AGENCIES.get(self.agency_name)
        if not agency:
            return f"Error: Agency '{self.agency_name}' not found"
        assert isinstance(agency, Agency)  # Type narrowing for static analysis

        # Determine the thread based on agent_name
        if not self.agent_name or (isinstance(agency.ceo, Agent) and self.agent_name == agency.ceo.name):
            thread = agency.main_thread
        else:
            thread = agency.agents_and_threads.get(agency.ceo.name, {}).get(self.agent_name)  # type: ignore

        if not thread:
            return f"Error: No thread found between '{agency.ceo.name}' and '{self.agent_name}'"  # type: ignore
        if not thread.thread or not thread.id:
            return f"Error: Thread between '{agency.ceo.name}' and '{self.agent_name}' is not initialized"  # type: ignore

        run = await asyncio.to_thread(self._get_last_run, thread)

        if not run:
            return "System Notification: 'Agent is ready to receive a message. " "Please send a message with the 'SendMessageAsync' tool.'"

        if run.status in ["queued", "in_progress", "requires_action"]:
            return "System Notification: 'Task is not completed yet. Please tell the user to wait " "and try again later.'"

        if run.status == "failed":
            error_message = (
                run.last_error.message 
                if run.last_error and hasattr(run.last_error, 'message')
                else "Unknown error"
            )
            return f"System Notification: 'Agent run failed with error: {error_message}. " "You may send another message with the 'SendMessageAsync' tool.'"

        if not thread.id:
            return "System Notification: 'Thread ID is missing'"

        messages = await asyncio.to_thread(self._client.beta.threads.messages.list, thread_id=thread.id, order="desc")

        if messages.data and messages.data[0].content:
            content_block = messages.data[0].content[0]
            if isinstance(content_block, TextContentBlock):
                text = content_block.text
                if text and text.value:  # Add null check for text and text.value
                    response_text = text.value
                    return f"{self.agent_name}'s Response: '{response_text}'"
            return "System Notification: 'Message content is not in text format or is empty'"
        else:
            return "System Notification: 'No response found from the agent.'"

    def _get_last_run(self, thread: Thread) -> Optional[Any]:
        if not thread.id:
            return None
        runs = self._client.beta.threads.runs.list(
            thread_id=thread.id,
            order="desc",
        )
        return runs.data[0] if runs.data else None


# Dynamically update the class docstring with the list of agencies and their agents
GetResponse.__doc__ = GetResponse.__doc__.format(agency_agents=AGENCIES_AND_AGENTS_STRING)


if __name__ == "__main__":

    async def main():
        # Example usage for a specific thread
        tool = GetResponse(
            agency_name="ResearchAgency",
            agent_name="BrowsingAgent",
        )
        response = await tool.run()
        print(response)

    asyncio.run(main())
