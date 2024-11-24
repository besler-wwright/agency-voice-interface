import asyncio
from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.aider_utils import get_aider_instance, generate_aider_window_title
from voice_assistant.utils.terminal import send_single_line_to_powershell

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
            status = await get_aider_instance()
            Console().print(f"[bold blue]Aider status: {status}[/bold blue]")
            
            # Get the window title for the Aider instance
            title = await generate_aider_window_title()
            
            # Send the message to Aider
            send_single_line_to_powershell(self.message, title=title)
            
            return f"Message sent to Aider: {self.message}"
            
        except Exception as e:
            Console().print(f"[bold red]Error sending message to Aider: {str(e)}[/bold red]")
            return f"Failed to send message to Aider: {str(e)}"


if __name__ == "__main__":
    async def test_tool():
        tool = TellAider(message="Hello Aider!")
        result = await tool.run()
        print(result)

    asyncio.run(test_tool())
