import subprocess


def open_powershell(command: str | None = None, title: str | None = None) -> None:
    """
    Open a new Windows Terminal PowerShell window with an optional command and title.
    
    Args:
        command: Optional command to execute in PowerShell. If None, opens an empty shell.
        title: Optional title for the PowerShell window
    """
    ps_init = "Import-Module PSReadLine; "
    if title and command:
        subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', f'{ps_init}$host.ui.RawUI.WindowTitle="{title}"; {command}'])
    elif title:
        subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', f'{ps_init}$host.ui.RawUI.WindowTitle="{title}"'])
    elif command:
        subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', f'{ps_init}{command}'])
    else:
        subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', ps_init])


def open_command_prompt(command: str | None = None, title: str | None = None) -> None:
    """
    Open a new Windows Terminal command prompt with an optional command and title.
    
    Args:
        command: Optional command to execute in the command prompt. If None, opens an empty prompt.
        title: Optional title for the command prompt window
    """
    if title and command:
        subprocess.Popen(['wt.exe', 'cmd.exe', '/k', f'title {title} && {command}'])
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
    open_powershell()  # Simple PowerShell window
    # open_powershell("Get-Process", title="Process List")  # PowerShell with command and title
