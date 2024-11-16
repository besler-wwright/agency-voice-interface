"""
This tool allows you to send a message to a specific agent within a specified agency and receive a response.

To use this tool, provide the message you want to send, the name of the agency to which the agent belongs, and optionally the name of the agent to whom the message should be sent. If the agent name is not specified, the message will be sent to the default agent for that agency.
"""

import asyncio
import logging
from typing import Optional

from agency_swarm.tools import BaseTool
from pydantic import Field, PrivateAttr, field_validator

from voice_assistant.tools.registry import AgenciesRegistry
from voice_assistant.utils.decorators import timeit_decorator


class SendMessage(BaseTool):
    """
    Sends a message to a specific agent within a specified agency and waits for an immediate response.

    Use this tool for direct, synchronous communication with agents for tasks that can be completed quickly.
    The agent processes the message and returns a response immediately.
    If 'agent_name' is not provided, the message is sent to the main agent in the agency.

    To continue the dialogue, invoke this tool again with your follow-up message.
    Note: You are responsible for relaying the agent's responses back to the user.
    Do not send more than one message at a time.

    Available Agencies and Agents:
    {agency_agents}
    """

    message: str = Field(..., description="The message to be sent.")
    agency_name: str = Field(..., description="The name of the agency to send the message to.")
    agent_name: Optional[str] = Field(
        None,
        description="The name of the agent to send the message to, or None to use the default agent.",
    )
    _registry: AgenciesRegistry = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._registry = AgenciesRegistry()

    @field_validator("agency_name", mode="before")
    def validate_agency_name(cls, value: str) -> str:
        registry = AgenciesRegistry()
        if not registry.get_agency(value):
            available = registry.get_available_agencies()
            raise ValueError(f"Agency '{value}' not found. Available agencies: {available}")
        return value

    @field_validator("agent_name", mode="before")
    def validate_agent_name(cls, value: Optional[str]) -> Optional[str]:
        if value:
            registry = AgenciesRegistry()
            agent_names = [
                agent.name 
                for agency in registry.agencies.values() 
                for agent in agency.agents
            ]
            if value not in agent_names:
                available = ", ".join(agent_names)
                raise ValueError(f"Agent '{value}' not found. Available agents: {available}")
        return value

    @classmethod
    def set_registry_for_testing(cls, registry: AgenciesRegistry) -> None:
        """Allow injection of registry for testing purposes"""
        cls._registry = registry

    @timeit_decorator
    async def run(self) -> str:
        try:
            async with asyncio.timeout(30):  # Add timeout
                result = await self._send_message()
                return str(result)
        except asyncio.TimeoutError:
            return "Error: Request timed out"
        except Exception as e:
            logging.error(f"Error in SendMessage: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

    async def _send_message(self) -> str:
        agency = self._registry.get_agency(self.agency_name)
        if not agency:
            return f"Agency '{self.agency_name}' not found"

        recipient_agent = None
        if self.agent_name:
            recipient_agent = next(
                (agent for agent in agency.agents if agent.name == self.agent_name),
                None
            )
            if not recipient_agent:
                return self._format_agent_error()

        response = await asyncio.to_thread(
            agency.get_completion,
            message=self.message,
            recipient_agent=recipient_agent or agency.agents[0]  # Use first agent as default
        )
        
        if isinstance(response, str):
             return response
        elif response is None:
             return "No response received"
        else:
            # Handle generator or other types by converting to string
            return str(response)

    def _format_agent_error(self) -> str:
        agency = self._registry.get_agency(self.agency_name)
        available = ", ".join(agent.name for agent in agency.agents)
        return f"Agent '{self.agent_name}' not found in agency '{self.agency_name}'. Available agents: {available}"


# Dynamically update the class docstring with the list of agencies and their agents
if SendMessage.__doc__:
    SendMessage.__doc__ = SendMessage.__doc__.format(
        agency_agents=AgenciesRegistry().agencies_string
    )


if __name__ == "__main__":
    tool = SendMessage(
        message="Hello, how are you?",
        agency_name="ResearchAgency",
        agent_name="BrowsingAgent",
    )
    print(asyncio.run(tool.run()))

    tool = SendMessage(
        message="Hello, how are you?",
        agency_name="ResearchAgency",
        agent_name=None,
    )
    print(asyncio.run(tool.run()))
