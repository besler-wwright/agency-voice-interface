import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import tell_aider_one_thing


class AiderSwitchToCodeMode(BaseTool):
    """
    A tool to switch Aider from chat mode to code mode.
    This tool sends the '/chat-mode' command to toggle Aider's mode.
    """

    async def run(self) -> str:
        try:
            return await tell_aider_one_thing("/chat-mode code")            
        except Exception as e:
            Console().print(f"[bold red]Error switching Aider mode: {str(e)}[/bold red]")
            return f"Failed to switch Aider mode: {str(e)}"

if __name__ == "__main__":
    tool = AiderSwitchToCodeMode()
    Console().print(asyncio.run(tool.run()))
