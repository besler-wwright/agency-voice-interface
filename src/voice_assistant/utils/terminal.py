import subprocess


def open_terminal(command: str | None = None, title: str | None = None) -> None:
    """
    Open a new terminal window (Windows Terminal or CMD) with an optional command and title.
    
    Args:
        command: Optional command to execute in the terminal. If None, opens an empty terminal.
        title: Optional title for the terminal window (only works with Windows Terminal/PowerShell)
    """
    try:
        # Windows Terminal
        if title and command:
            subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', 
                            f'$host.ui.RawUI.WindowTitle = "{title}"; {command}'])
        elif title:
            subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', 
                            f'$host.ui.RawUI.WindowTitle = "{title}"'])
        elif command:
            subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', command])
        else:
            subprocess.Popen(['wt.exe'])
    except FileNotFoundError:
        # Fallback to Command Prompt
        if command:
            subprocess.Popen(['cmd.exe', '/k', command])
        else:
            subprocess.Popen(['cmd.exe'])

# Example usage
if __name__ == "__main__":
    # Open a simple terminal
    # open_terminal()
    
    # Or open with a specific command
    # open_terminal("dir")
    
    # Open with a title
    open_terminal(title="My Terminal")
    
    # Open with both title and command
    # open_terminal("dir", title="Directory Listing")
