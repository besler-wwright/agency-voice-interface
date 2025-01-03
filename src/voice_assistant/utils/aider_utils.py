import subprocess
import sys
import time

from rich.console import Console

from voice_assistant.config import CURRENT_GIT_PROJECT_DIR
from voice_assistant.utils.git_utils import get_repository_name
from voice_assistant.utils.terminal_utils import (
    open_powershell_prompt,
    send_multiple_lines_to_powershell,
    send_single_line_to_powershell,
)
from voice_assistant.utils.windows_utils import get_hwnd_for_window_by_title


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
        f"cd {CURRENT_GIT_PROJECT_DIR}",
        "Remove-Item Env:VSCODE_GIT_IPC_HANDLE",
        "aider"
    ]
    send_multiple_lines_to_powershell(lines, title=title)
    time.sleep(1)  # Wait for aider to start up
    send_single_line_to_powershell("/read-only .instructions/", title=title)
    
    return title

async def get_aider_instance() -> str:
    """
    Gets or creates an Aider instance.
    First checks if an Aider window exists and activates it if found.
    If no Aider window exists, creates a new instance.
    
    Returns:
        str: Status message indicating what action was taken
    """
    title = await generate_aider_window_title()
    hwnd = get_hwnd_for_window_by_title(title, partial_match=True)
    
    if hwnd:
        return title
    else:
        return await initialize_windows_aider_session()

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


async def tell_aider_one_thing(message):
    try:
        title = await get_aider_instance()
        send_single_line_to_powershell(message, title=title)
        
        return f"Message sent to Aider: {message}"
    except Exception as e:
        Console().print(f"[bold red]Error sending message to Aider: {str(e)}[/bold red]")
        return f"Failed to send message to Aider: {str(e)}"

async def tell_aider_several_things(messages :list[str]):
    try:
        title = await get_aider_instance()
        send_multiple_lines_to_powershell(messages, title=title)
        return "Messages sent to Aider"
    except Exception as e:
        Console().print(f"[bold red]Error sending message to Aider: {str(e)}[/bold red]")
        return f"Failed to send message to Aider: {str(e)}"
        return f"Failed to send message to Aider: {str(e)}"
