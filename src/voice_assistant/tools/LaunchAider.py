import asyncio
import sys

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import (
    initialize_linux_aider_session,
    initialize_windows_aider_session,
)


class LaunchAider(BaseTool):
    """
    A tool to launch Aider in a new terminal prompt window.
    """

    # directory: str = Field(
    #     default=".",
    #     description="The directory to open Aider in. Defaults to current directory."
    # )

    async def run(self) -> str:
        try:
            response = ""
            if sys.platform == "win32":
                # Windows
                response = await initialize_windows_aider_session()
            else:
                # Linux/Mac
                response = initialize_linux_aider_session()
                
            return response
        except Exception as e:
            Console().print(f"[bold red]Error launching Aider: {str(e)}[/bold red]")
            return f"Failed to launch Aider: {str(e)}"

if __name__ == "__main__":
    tool = LaunchAider()
    print(asyncio.run(tool.run()))
