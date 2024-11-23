import asyncio
import os
import subprocess
import sys

from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.aider_utils import (
    get_aider_window_title,
    initialize_windows_aider_session,
    initialize_linux_aider_session
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
            if sys.platform == "win32":
                # Windows
                await initialize_windows_aider_session()
            else:
                # Linux/Mac
                initialize_linux_aider_session()
                
            return "Aider launched successfully in a new terminal window"
        except Exception as e:
            Console().print(f"[bold red]Error launching Aider: {str(e)}[/bold red]")
            return f"Failed to launch Aider: {str(e)}"

if __name__ == "__main__":
    tool = LaunchAider()
    print(asyncio.run(tool.run()))
if __name__ == "__main__":
    tool = LaunchAider()
    print(asyncio.run(tool.run()))
