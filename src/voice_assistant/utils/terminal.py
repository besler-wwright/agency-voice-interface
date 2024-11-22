import subprocess
import time
from typing import Optional, TypedDict, Union

import win32con
import win32gui
import win32process


class ProcessWindowContext(TypedDict, total=False):
    handle: Optional[int]
    pid: int

class PowerShellWindowContext(TypedDict, total=False):
    handle: Optional[int]
    title: Optional[str]


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


def send_text_to_powershell_by_handle(process: subprocess.Popen, text: str) -> bool:
    """
    Send text to a PowerShell window using its process handle.
    
    Args:
        process: The subprocess.Popen handle of the PowerShell window
        text: The text to send to the PowerShell window
    
    Returns:
        bool: True if text was sent successfully, False otherwise
    """
    def find_window_by_pid(hwnd, ctx):
        if not win32gui.IsWindowVisible(hwnd):
            return True
            
        # Get the process ID for the window
        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == ctx['pid']:
                ctx['handle'] = hwnd
                return False  # Stop enumeration
        except:
            pass
        return True

    # Context to store the found window handle
    context: ProcessWindowContext = {'handle': None, 'pid': process.pid}

    # Find the window associated with the process
    win32gui.EnumWindows(find_window_by_pid, context)
    
    if not context['handle']:
        return False

    # Activate the window
    win32gui.SetForegroundWindow(context['handle'])
    time.sleep(0.1)  # Give window time to come to foreground

    # Send the text character by character
    for char in text:
        win32gui.SendMessage(context['handle'], win32con.WM_CHAR, ord(char), 0)
    
    # Send Enter key
    win32gui.SendMessage(context['handle'], win32con.WM_CHAR, 0x0D, 0)
    
    return True

def send_text_to_powershell(text: str, target: Optional[Union[str, subprocess.Popen]] = None) -> bool:
    """
    Send text to a PowerShell window.
    
    Args:
        text: The text to send to the PowerShell window
        target: Optional target identifier:
                - If str: treated as window title to search for
                - If subprocess.Popen: used as process handle
                - If None: tries to find any PowerShell window
    
    Returns:
        bool: True if text was sent successfully, False otherwise
    """
    # If target is a process handle, use the handle-based method
    if isinstance(target, subprocess.Popen):
        return send_text_to_powershell_by_handle(target, text)
        
    # Otherwise use the window title based method
    def find_powershell_window(hwnd, ctx):
        if not win32gui.IsWindowVisible(hwnd):
            return
        
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
            
        # If window_title is provided, look for exact match
        if ctx.get('title'):
            if ctx['title'] in title:
                ctx['handle'] = hwnd
                return False  # Stop enumeration
        # Otherwise look for any PowerShell window
        elif 'PowerShell' in title:
            ctx['handle'] = hwnd
            return False  # Stop enumeration
        return True

    # Context to store the found window handle
    context: PowerShellWindowContext = {'handle': None}
    if isinstance(target, str):
        context['title'] = target

    # Find the PowerShell window
    win32gui.EnumWindows(find_powershell_window, context)
    
    if not context['handle']:
        return False

    # Activate the window
    win32gui.SetForegroundWindow(context['handle'])
    time.sleep(0.1)  # Give window time to come to foreground

    # Send the text character by character
    for char in text:
        win32gui.SendMessage(context['handle'], win32con.WM_CHAR, ord(char), 0)
    
    # Send Enter key
    win32gui.SendMessage(context['handle'], win32con.WM_CHAR, 0x0D, 0)
    
    return True

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
    # open_powershell_prompt(title="Process List")  # PowerShell with command and title
    
    # Get handle to Windows Terminal process
    # wt_handle = open_powershell_prompt(
    #     title="Nice Terminal",
    #     command="Get-Process"
    # )
    # print(f"Windows Terminal process ID: {wt_handle.pid}")
    
    # Example of sending text to PowerShell using process handle
    ps = open_powershell_prompt(title="Test PowerShell")
    time.sleep(2)  # Wait for window to open
    
    # Send using process handle
    success = send_text_to_powershell("Get-Process | Select-Object -First 5", ps)
    if success:
        print("Text sent successfully using handle")
    else:
        print("Failed to send text using handle")
        
    # Send using window title
    success = send_text_to_powershell("Get-Date", "Test PowerShell")
    if success:
        print("Text sent successfully using title")
    else:
        print("Failed to send text using title")
