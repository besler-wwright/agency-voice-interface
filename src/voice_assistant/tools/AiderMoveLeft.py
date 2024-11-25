import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console
import pyautogui

class AiderMoveLeft(BaseTool):
    """
    A tool to move the cursor left in Aider while selecting text using Ctrl+Shift+Left.
    This is useful for selecting and modifying code in Aider.
    """

    async def run(self) -> str:
        """
        Executes the key combination Ctrl+Shift+Left using pyautogui.
        
        Returns:
            str: Status message indicating success or failure
        """
        try:
            # Ensure there's a small delay before sending keystrokes
            await asyncio.sleep(0.1)
            
            # Press the key combination
            pyautogui.hotkey('ctrl', 'shift', 'left')
            
            return "Successfully moved cursor left with selection"

        except Exception as e:
            Console().print(f"[bold red]Error sending keystrokes: {str(e)}[/bold red]")
            return f"Failed to send keystrokes: {str(e)}"


if __name__ == "__main__":
    async def test_tool():
        tool = AiderMoveLeft()
        result = await tool.run()
        Console().print(result)

    asyncio.run(test_tool())
