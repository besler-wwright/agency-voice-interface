import asyncio
import sys

from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.aider_utils import get_aider_instance
from voice_assistant.utils.windows_utils import (
    get_hwnd_for_window_by_title,
    maximize_window_by_handle,
)


class MaximizeAider(BaseTool):
    """
    A tool to maximize an Aider window by its title.
    Only works on Windows systems.
    """
    async def run(self) -> str:
        """
        Find and maximize a window by its title.
        
        Returns:
            str: Status message indicating success or failure
        """
        if sys.platform != "win32":
            return "Error: This tool only works on Windows systems"

        try:
            # Find the window
            title = await get_aider_instance()
            hwnd = get_hwnd_for_window_by_title(title)
            
            if not hwnd:
                return f"Error: No window found with title '{title}'"

            # Maximize the window
            if maximize_window_by_handle(hwnd):
                return f"Successfully maximized window with title '{title}'"
            else:
                return f"Error: Failed to maximize window with title '{title}'"

        except Exception as e:
            Console().print(f"[bold red]Error maximizing window: {str(e)}[/bold red]")
            return f"Error: {str(e)}"


if __name__ == "__main__":
    tool = MaximizeAider()
    print(asyncio.run(tool.run()))
