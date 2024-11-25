import asyncio
import time

import pyautogui
from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import get_aider_instance


class AiderMoveLeft(BaseTool):
    """
    A tool to move the cursor left in Aider while selecting text using Windows+Shift+Left.
    This is useful for selecting and modifying code in Aider.
    """

    async def run(self) -> str:
        """
        Executes the key combination Windows+Shift+Left using pyautogui on the Aider instance.
        
    Returns:
            str: Status message indicating success or failure
        """
        try:
            #get aider instance
            await get_aider_instance()
            
            # Ensure there's a small delay before sending keystrokes
            await asyncio.sleep(1)

            pyautogui.hotkey('win', 'ctrl', 'left')                        
            # pyautogui.keyDown('win')
            # pyautogui.keyDown('ctrl')
            # pyautogui.keyDown('left')
            # time.sleep(0.1)  # Small delay to ensure keys register
            # pyautogui.keyUp('left')
            # pyautogui.keyUp('ctrl')
            # pyautogui.keyUp('win')
                        
            return "Successfully moved left" 

        except Exception as e:
            Console().print(f"[bold red]Error sending keystrokes: {str(e)}[/bold red]")
            return f"Failed to send keystrokes: {str(e)}"


if __name__ == "__main__":
    tool = AiderMoveLeft()
    Console().print(asyncio.run(tool.run()))
