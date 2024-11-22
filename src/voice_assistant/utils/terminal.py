import subprocess

def open_terminal(command: str | None = None) -> None:
    """
    Open a new terminal window (Windows Terminal or CMD) with an optional command.
    
    Args:
        command: Optional command to execute in the terminal. If None, opens an empty terminal.
    """
    try:
        # Windows Terminal
        if command:
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
    open_terminal()
    
    # Or open with a specific command
    open_terminal("dir")
