import subprocess
import sys
import time

from voice_assistant.utils.git_utils import get_repository_name
from voice_assistant.utils.terminal import (
    open_powershell_prompt,
    send_multiple_lines_to_powershell,
    send_single_line_to_powershell,
)


async def generate_aider_window_title() -> str:
    """
    Generates the window title for Aider terminal window.
    
    Returns:
        str: Window title in format "Aider - {repo_name}"
    """
    git_repo_name = await get_repository_name()
    return f"Aider - {git_repo_name}"

async def initialize_windows_aider_session()->str:
    """
    Initializes an Aider session in a new PowerShell window on Windows.
    """
    title = await generate_aider_window_title()
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
    
    return "Aider launched successfully in a new terminal window"

def initialize_linux_aider_session()->str:
    """
    Initializes an Aider session in a new terminal window on Linux/Mac.
    """
    terminal_cmd = "gnome-terminal" if sys.platform.startswith("linux") else "open -a Terminal"
    cmd = 'aider'
    subprocess.Popen([terminal_cmd, '--', 'bash', '-c', cmd])
    """
    Initializes an Aider session in a new terminal window on Linux/Mac.
    """
    terminal_cmd = "gnome-terminal" if sys.platform.startswith("linux") else "open -a Terminal"
    cmd = 'aider'
    subprocess.Popen([terminal_cmd, '--', 'bash', '-c', cmd])
    return "Aider launched successfully in a new terminal window"
