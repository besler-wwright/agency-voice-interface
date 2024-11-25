import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import tell_aider_one_thing


class AiderShutDown(BaseTool):
    """
    A tool to shut down the Aider instance by sending the exit command.
    This tool sends the '/exit' command to cleanly terminate Aider.
    """

    async def run(self) -> str:
        """
        Sends the exit command to the active Aider instance.
        
        Returns:
            str: Status message indicating success or failure
        """
        try:
            return await tell_aider_one_thing("/exit")
        except Exception as e:
            Console().print(f"[bold red]Error shutting down Aider: {str(e)}[/bold red]")
            return f"Failed to shut down Aider: {str(e)}"


if __name__ == "__main__":
    async def test_tool():
        tool = AiderShutDown()
        result = await tool.run()
        Console().print(result)

    asyncio.run(test_tool())