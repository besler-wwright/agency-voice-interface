import asyncio

from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.aider_utils import tell_aider_one_thing


class TellAider(BaseTool):
    """
    A tool to send commands to an Aider instance.
    If no Aider instance is running, one will be started automatically.
    """

    message: str = Field(
        ..., 
        description="The message or command to send to Aider"
    )

    async def run(self) -> str:
        try:
            # Get or create Aider instance
            return await tell_aider_one_thing(self.message)
            
        except Exception as e:
            Console().print(f"[bold red]Error sending message to Aider: {str(e)}[/bold red]")
            return f"Failed to send message to Aider: {str(e)}"



if __name__ == "__main__":
    tool = TellAider(message="/help")
    Console().print(asyncio.run(tool.run()))
    

