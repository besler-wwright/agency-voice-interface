import subprocess


def open_terminal():
    """Open a new Windows Terminal window."""
    try:
        # Try Windows Terminal first
        subprocess.Popen(['wt.exe'])
    except FileNotFoundError:
        # Fall back to Command Prompt if Windows Terminal isn't available
        subprocess.Popen(['cmd.exe'])

def open_terminal_with_command(command):
    """Open a new Windows Terminal window and execute a command."""
    try:
        subprocess.Popen(['wt.exe', 'powershell.exe', '-NoExit', '-Command', command])
    except FileNotFoundError:
        subprocess.Popen(['cmd.exe', '/k', command])

# Example usage
if __name__ == "__main__":
    # Open a simple terminal
    open_terminal()
    
    # Or open with a specific command
    open_terminal_with_command("dir")