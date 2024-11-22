import win32con
import win32gui
from rich.console import Console


def list_visible_windows():
    """List all visible window titles and handles.
    
    Returns:
        list: A list of tuples containing (window_handle, window_title) for all visible windows.
        
    Note:
        This is a simpler version of list_all_windows(). Consider using list_all_windows() 
        with visible_only=True for more detailed window information.
    """
    windows = []
    
    def enum_window_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                results.append((hwnd, title))
    
    win32gui.EnumWindows(enum_window_callback, windows)
    return windows

def list_all_windows(*, visible_only: bool = False, enabled_only: bool = False, non_minimized_only: bool = False, title_contains: str|None = None, console_write_list: bool = False):
    """List windows based on specified filters with detailed window information.
    
    Args:
        visible_only (bool): If True, only include visible windows
        enabled_only (bool): If True, only include enabled windows (windows that can receive input)
        non_minimized_only (bool): If True, exclude minimized windows from results
        title_contains (str): If provided, only include windows whose titles contain this string (case-insensitive)
        console_write_list (bool): If True, prints the results to console using rich formatting
    
    Returns:
        list: List of dictionaries containing window information that matches all specified filters.
              Each dictionary contains:
                - 'handle': Window handle (hwnd)
                - 'title': Window title text
                - 'visible': Boolean indicating if window is visible
                - 'enabled': Boolean indicating if window can receive input
                - 'minimized': Boolean indicating if window is minimized
    
    Example:
        >>> # Get all visible Chrome windows
        >>> chrome_windows = list_all_windows(visible_only=True, title_contains="chrome")
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
    """Activate (bring to foreground) a window given its handle.
    
    Args:
        hwnd (int): Window handle to activate
        
    Note:
        If the window is minimized, it will be restored before being brought to the foreground.
        Prints activation attempt to console using rich formatting.
    """
    Console().print(f"Activating window with handle {hwnd}")
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def activate_window_by_title(query_title, partial_match=True):
    """Activate first window that matches the given title.
    
    Args:
        query_title (str): Window title to search for
        partial_match (bool): If True, matches substring. If False, requires exact match.
                            Case-insensitive in both modes.
    
    Returns:
        bool: True if matching window was found and activated, False if no match found
        
    Example:
        >>> # Activate any window containing "notepad" in title
        >>> activate_window_by_title("notepad")  # Returns True if found
        >>> # Activate window with exact title match
        >>> activate_window_by_title("Untitled - Notepad", partial_match=False)
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

