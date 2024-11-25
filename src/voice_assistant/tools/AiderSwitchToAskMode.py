import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import tell_aider_one_thing


class AiderSwitchToAskMode(BaseTool):
    """
    A tool to switch Aider from chat mode to ask mode.
    This tool sends the '/chat-mode' command to toggle Aider's mode.
    """

    async def run(self) -> str:
        try:
            return await tell_aider_one_thing("/chat-mode ask")
        except Exception as e:
            Console().print(f"[bold red]Error switching Aider mode: {str(e)}[/bold red]")
            return f"Failed to switch Aider mode: {str(e)}"
        
if __name__ == "__main__":
    async def test_tool():
        tool = AiderSwitchToAskMode()
        result = await tool.run()
        Console().print(result)

    asyncio.run(test_tool())