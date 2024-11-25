import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import get_aider_instance
from voice_assistant.utils.terminal_utils import send_single_line_to_powershell


class AiderSwitchToCodeMode(BaseTool):
    """
    A tool to switch Aider from chat mode to code mode.
    This tool sends the '/chat-mode' command to toggle Aider's mode.
    """

    async def run(self) -> str:
        try:
            # Get or create Aider instance
            title = await get_aider_instance()
            Console().print(f"[bold blue]Driving Aider Instance: {title}[/bold blue]")
            
            # Send the chat-mode command to toggle to code mode
            send_single_line_to_powershell("/chat-mode code", title=title)
            
            return "Switched Aider to code mode"
            
        except Exception as e:
            Console().print(f"[bold red]Error switching Aider mode: {str(e)}[/bold red]")
            return f"Failed to switch Aider mode: {str(e)}"

if __name__ == "__main__":
    async def test_tool():
        tool = AiderSwitchToCodeMode()
        result = await tool.run()
        Console().print(result)

    asyncio.run(test_tool())
