import win32con
import win32gui
from rich.console import Console


def list_visible_windows():
    """List all visible window titles and handles."""
    windows = []
    
    def enum_window_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                results.append((hwnd, title))
    
    win32gui.EnumWindows(enum_window_callback, windows)
    return windows

def list_all_windows(*, visible_only: bool = False, enabled_only: bool = False, non_minimized_only: bool = False, title_contains: str|None = None, console_write_list: bool = False):
    """List windows based on specified filters.
    
    Args:
        visible_only (bool): If True, only include visible windows
        enabled_only (bool): If True, only include enabled windows
        non_minimized_only (bool): If True, exclude minimized windows
        title_contains (str): If provided, only include windows whose titles contain this string (case-insensitive)
    
    Returns:
        list: List of dictionaries containing window information that matches all specified filters
    """
    windows = []
    
    def enum_window_callback(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if title:  # Only include windows with titles
            visible = win32gui.IsWindowVisible(hwnd)
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            enabled = bool(style & win32con.WS_DISABLED == 0)
            minimized = bool(style & win32con.WS_MINIMIZE)
            
            # Apply filters
            if visible_only and not visible:
                return
            if enabled_only and not enabled:
                return
            if non_minimized_only and minimized:
                return
            if title_contains and title_contains.lower() not in title.lower():
                return
                
            results.append({
                'handle': hwnd,
                'title': title,
                'visible': visible,
                'enabled': enabled,
                'minimized': minimized
            })
    
    win32gui.EnumWindows(enum_window_callback, windows)
    if console_write_list:
        c = Console()
        if title_contains and console_write_list:
            c.print(f"\nWindows containing '{title_contains}':")
        if len(windows) == 0 and console_write_list:
            c.print("[yellow]No windows found[/yellow]")
        for window in windows:
            c.print(window)
    return windows


def activate_window_by_handle(hwnd):
    """Activate a window given its handle."""
    Console().print(f"Activating window with handle {hwnd}")
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def activate_window_by_title(query_title, partial_match=True):
    """Activate first window that matches the given title.
    
    Args:
        title (str): Window title to search for
        partial_match (bool): If True, matches substring. If False, requires exact match.
    
    Returns:
        bool: True if window was found and activated, False otherwise
    """
    windows = list_all_windows()
    
    for window in windows:
        title = window['title']
        if (partial_match and query_title.lower() in title.lower()) or \
           (not partial_match and query_title.lower() == title.lower()):
            activate_window_by_handle(window['handle'])
            return True
    return False


# Example usage
if __name__ == "__main__":
    c = Console()

    # List all windows
    c.print("\nAll windows:")
    windows = list_all_windows(console_write_list=True)

    # Example filtering
    c.print("\nVisible, non-minimized windows:")
    filtered_windows = list_all_windows(visible_only=True, non_minimized_only=True, console_write_list=True)
        
    # Example Filtering 2: 
    chrome_windows = list_all_windows(title_contains="chrome", console_write_list=True)

    # Example: Activate a window by title
    search_title = "Notepad"
    notepad_activated = activate_window_by_title(search_title)  # Will activate first window containing "Notepad"
    c.print(f"activated [{search_title}]: {notepad_activated}" )
    
    # Example - Looking for Aider
    search_title = "Aider"
    aider_windows = list_all_windows(title_contains="Aider", console_write_list=True)
    aider_activated = activate_window_by_title('Aider')
    c.print(f"activated [{search_title}]: {aider_activated}")

