import asyncio
import sys

from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.windows_utils import (
    get_hwnd_for_window_by_title,
    maximize_window_by_handle,
)


class MaximizeAI(BaseTool):
    """
    A tool to maximize a window by its title.
    Only works on Windows systems.
    """

    window_title: str = Field(
        ...,
        description="The title of the window to maximize. Can be partial or exact match.",
    )
    exact_match: bool = Field(
        False,
        description="If True, requires exact title match. If False, matches substrings.",
    )

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
            hwnd = get_hwnd_for_window_by_title(
                self.window_title,
                partial_match=not self.exact_match,
                activate_if_found=True
            )
            
            if not hwnd:
                return f"Error: No window found with title '{self.window_title}'"

            # Maximize the window
            if maximize_window_by_handle(hwnd):
                return f"Successfully maximized window with title '{self.window_title}'"
            else:
                return f"Error: Failed to maximize window with title '{self.window_title}'"

        except Exception as e:
            Console().print(f"[bold red]Error maximizing window: {str(e)}[/bold red]")
            return f"Error: {str(e)}"


if __name__ == "__main__":
    async def test_tool():
        # Test with a Notepad window
        tool = MaximizeAI(window_title="Notepad")
        result = await tool.run()
        print(result)

        # Test with exact match
        tool = MaximizeAI(window_title="Untitled - Notepad", exact_match=True)
        result = await tool.run()
        print(result)

    asyncio.run(test_tool())
