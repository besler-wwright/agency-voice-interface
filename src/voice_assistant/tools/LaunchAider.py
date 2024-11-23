import asyncio
import os
import subprocess
import sys
from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

class LaunchAider(BaseTool):
    """
    A tool to launch Aider in a new command prompt window.
    """

    directory: str = Field(
        default=".",
        description="The directory to open Aider in. Defaults to current directory."
    )

    async def run(self) -> str:
        try:
            if sys.platform == "win32":
                # Windows
                cmd = f'start cmd /K "cd /d {os.path.abspath(self.directory)} && aider"'
                subprocess.Popen(cmd, shell=True)
            else:
                # Linux/Mac
                terminal_cmd = "gnome-terminal" if sys.platform.startswith("linux") else "open -a Terminal"
                cmd = f'cd {os.path.abspath(self.directory)} && aider'
                subprocess.Popen([terminal_cmd, '--', 'bash', '-c', cmd])
                
            return "Aider launched successfully in a new terminal window"
        except Exception as e:
            Console().print(f"[bold red]Error launching Aider: {str(e)}[/bold red]")
            return f"Failed to launch Aider: {str(e)}"


if __name__ == "__main__":
    tool = LaunchAider()
    print(asyncio.run(tool.run()))
