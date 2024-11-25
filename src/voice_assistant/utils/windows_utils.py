import win32con
import win32gui
from rich.console import Console


def list_visible_windows():
    """
    Lists all visible windows on the system.
    
    Returns:
        list: A list of tuples containing (window handle, window title) for all visible windows
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
    """
    Lists all windows with optional filtering criteria.
    
    Args:
        visible_only (bool): Only include visible windows if True
        enabled_only (bool): Only include enabled windows if True
        non_minimized_only (bool): Exclude minimized windows if True
        title_contains (str|None): Only include windows whose titles contain this string
        console_write_list (bool): Print results to console if True
    
    Returns:
        list: A list of dictionaries containing window information with keys:
            - handle: Window handle
            - title: Window title
            - visible: Whether window is visible
            - enabled: Whether window is enabled
            - minimized: Whether window is minimized
    """
    windows = []
    
    def enum_window_callback(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if title:  # Only include windows with titles
            visible = bool(win32gui.IsWindowVisible(hwnd))
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
    """
    Activates (brings to foreground) a window given its handle.
    
    Args:
        hwnd: Window handle to activate
        
    Note:
        If the window is minimized, it will be restored before being brought to the foreground
    """
    # Console().print(f"Activating window with handle {hwnd}")
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def get_hwnd_for_window_by_title(query_title, partial_match=True, activate_if_found=True):
    """
    Finds and optionally activates a window by its title.
    
    Args:
        query_title (str): The title to search for
        partial_match (bool): If True, matches substring. If False, requires exact match
        activate_if_found (bool): If True, brings window to front when found
    
    Returns:
        int: Window handle if found, 0 if not found
    """
    windows = list_all_windows()
    
    for window in windows:
        title = window['title']
        if (partial_match and query_title.lower() in title.lower()) or \
           (not partial_match and query_title.lower() == title.lower()):
            if activate_if_found:
                activate_window_by_handle(window['handle'])
            return window['handle']
    return 0


def maximize_window_by_handle(hwnd):
    """
    Maximizes a window given its handle.
    
    Args:
        hwnd: Window handle to maximize
        
    Returns:
        bool: True if successful, False if the window handle is invalid
    """
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return True
    except Exception:
        return False


# Example usage
if __name__ == "__main__":
    c = Console()

    # # List all windows
    c.print("\nAll windows:")
    windows = list_all_windows(console_write_list=True, visible_only=True)

    # # Example filtering
    # c.print("\nVisible, non-minimized windows:")
    # filtered_windows = list_all_windows(visible_only=True, non_minimized_only=True, console_write_list=True)
        
    # # Example Filtering 2: 
    # chrome_windows = list_all_windows(title_contains="chrome", console_write_list=True)

    # # Example: Activate a window by title
    # search_title = "Notepad"
    # notepad_activated = activate_window_by_title(search_title)  # Will activate first window containing "Notepad"
    # c.print(f"activated [{search_title}]: {notepad_activated}" )
    
    # Example - Looking for Aider
    search_title = "Aider"
    aider_windows = list_all_windows(title_contains="Aider", console_write_list=True)
    hwnd = get_hwnd_for_window_by_title('Aider')
    c.print(f"activated [{search_title}]: with handle {hwnd}")

    # Example - Maximize a window
    hwnd = get_hwnd_for_window_by_title('Notepad')
    if hwnd:
        maximize_window_by_handle(hwnd)
        c.print(f"Maximized window with handle {hwnd}")

