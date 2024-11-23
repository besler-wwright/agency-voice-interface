import random
import subprocess
import time
from typing import Any, Dict, Optional, TypedDict, Union

import pyautogui
from loguru import logger

from voice_assistant.utils.windows import get_hwnd_for_window_by_title


class ProcessWindowContext(TypedDict, total=False):
    handle: Optional[int]
    pid: int

class PowerShellWindowContext(TypedDict, total=False):
    handle: Optional[int]
    title: Optional[str]

def debug_print(message: str, context: Optional[Union[Dict[str, Any], ProcessWindowContext, PowerShellWindowContext]] = None) -> None:
    """Print debug information with optional context"""
    if context:
        logger.debug(f"{message} | Context: {context}")
    else:
        logger.debug(message)


def open_powershell_prompt(command: str | None = None, title: str | None = None) -> subprocess.Popen:
    """
    Open a new PowerShell window with an optional command and title.
    
    Args:
        command: Optional command to execute in PowerShell. If None, opens an empty shell.
        title: Optional title for the PowerShell window
    
    Returns:
        subprocess.Popen: Handle to the created Windows Terminal process
    """
    if title:
        base_command = [
            'wt.exe',          # Windows Terminal executable
            'new-tab',         # Create a new tab instead of new window
            '--title',         # Specify that next argument is the tab title
            title,            # The actual title to display
            'pwsh.exe',       # PowerShell Core executable
            '-NoProfile',     # Start without loading the PowerShell profile (faster startup)
            '-NoExit'         # Keep the window open after running commands
        ]
    else:
        base_command = [
            'wt.exe',         # Windows Terminal executable
            'pwsh.exe',       # PowerShell Core executable
            '-NoProfile',     # Start without loading the PowerShell profile (faster startup)
            '-NoExit'         # Keep the window open after running commands
        ]
    
    if command:
        base_command.extend([
            '-Command',       # Specify that what follows is a PowerShell command to execute
            command          # The actual command to run
        ])

    return subprocess.Popen(base_command)

def send_single_line_to_powershell(text: str, title:str):
    
    hwnd = get_hwnd_for_window_by_title(title, activate_if_found=True)
    
    if not hwnd or hwnd == 0:
        print(f"Failed to find PowerShell window with title {title}")
        return False

    time.sleep(1)  # Give window time to come to foreground

    pyautogui.write(text)
    pyautogui.press('enter')

def send_multiple_lines_to_powershell(lines: list[str], title:str):
    
    hwnd = get_hwnd_for_window_by_title(title, activate_if_found=True)
    
    if not hwnd or hwnd == 0:
        print(f"Failed to find PowerShell window with title {title}")
        return False

    time.sleep(1)  # Give window time to come to foreground
    
    for line in lines:
        pyautogui.write(line)
        pyautogui.press('enter')
        time.sleep(.1)
    

def open_command_prompt(command: str | None = None, title: str | None = None) -> None:
    """
    Open a new Windows Terminal command prompt with an optional command and title.
    
    Args:
        command: Optional command to execute in the command prompt. If None, opens an empty prompt.
        title: Optional title for the command prompt window
    """
    if title and command:
        subprocess.Popen(['wt.exe', 'cmd.exe', '/k', f'title {title} && {command}']) #/k keeps the window open
    elif title:
        subprocess.Popen(['wt.exe', 'cmd.exe', '/k', f'title {title}'])
    elif command:
        subprocess.Popen(['wt.exe', 'cmd.exe', '/k', command])
    else:
        subprocess.Popen(['wt.exe', 'cmd.exe'])

# Example usage
if __name__ == "__main__":
    # # Open a simple command prompt
    # open_command_prompt()
    
    # # # Or open with a specific command
    # open_command_prompt("dir")
    
    # # # Open with a title
    # open_command_prompt(title="My Command Prompt")
    
    # # Open with both title and command
    # open_command_prompt("dir", title="Directory Listing")
    
    # Open PowerShell examples
    # open_powershell_prompt()  # Simple PowerShell window
    # open_powershell_prompt(title="Process List", command="Get-Process")  # PowerShell with command and title
    
    # Get handle to Windows Terminal process
    # wt_handle = open_powershell_prompt(
    #     title="Nice Terminal",
    #     command="Get-Process"
    # )
    # print(f"Windows Terminal process ID: {wt_handle.pid}")
    
    # Example of sending text to PowerShell using process handle
    title = f"Aider - {random.randint(0, 1000)}"
    process = open_powershell_prompt(title=title)
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