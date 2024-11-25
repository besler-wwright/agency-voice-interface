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
            await tell_aider_one_thing("/exit") #exit aider
            return await tell_aider_one_thing("exit") #exit powershell
        except Exception as e:
            Console().print(f"[bold red]Error shutting down Aider: {str(e)}[/bold red]")
            return f"Failed to shut down Aider: {str(e)}"


if __name__ == "__main__":
    tool = AiderShutDown()
    Console().print(asyncio.run(tool.run()))
