import asyncio
import os
import random
import subprocess
import sys
import time

from agency_swarm.tools import BaseTool
from pydantic import Field
from rich.console import Console

from voice_assistant.utils.terminal import (
    open_powershell_prompt,
    send_multiple_lines_to_powershell,
    send_single_line_to_powershell,
)


class LaunchAider(BaseTool):
    """
    A tool to launch Aider in a new terminal prompt window.
    """

    directory: str = Field(
        default=".",
        description="The directory to open Aider in. Defaults to current directory."
    )

    async def run(self) -> str:
        try:
            if sys.platform == "win32":
                # Windows
                # cmd = f'start cmd /K "cd /d {os.path.abspath(self.directory)} && aider"'
                # subprocess.Popen(cmd, shell=True)
                title = f"Aider - {random.randint(0, 1000)}"
                open_powershell_prompt(title=title)
                time.sleep(1)  # Wait for window to open
                lines = [
                    "Get-Process | Select-Object -First 5", 
                    "cd /git/agency-voice-interface",
                    "Remove-Item Env:VSCODE_GIT_IPC_HANDLE",
                    "aider"
                    ]
                send_multiple_lines_to_powershell(lines, title=title)
                time.sleep(1)  # Wait for aider to start up
                send_single_line_to_powershell("/read-only .instructions/", title=title)
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
