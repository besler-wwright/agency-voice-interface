import subprocess


def open_powershell_prompt(command: str | None = None, title: str | None = None) -> None:
    """
    Open a new Windows Terminal PowerShell window with an optional command and title.
    
    Args:
        command: Optional command to execute in PowerShell. If None, opens an empty shell.
        title: Optional title for the PowerShell window
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

    subprocess.Popen(base_command)


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
    open_powershell_prompt(title="Process List", command="Get-Process")  # PowerShell with command and title
