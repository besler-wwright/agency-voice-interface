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

def list_all_windows(*, visible_only: bool = False, enabled_only: bool = False, non_minimized_only: bool = False, title_contains: str|None = None):
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
    return windows


def activate_window_by_handle(hwnd):
    """Activate a window given its handle."""
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
    
    for hwnd, title in windows:
        if (partial_match and query_title.lower() in title.lower()) or \
           (not partial_match and query_title.lower() == title.lower()):
            activate_window_by_handle(hwnd)
            return True
    return False

# Example usage
if __name__ == "__main__":
    c = Console()

    # List all windows
    windows = list_all_windows()
    for window in windows:
        c.print(window)

    # Example filtering
    c.print("\nVisible, non-minimized windows:")
    filtered_windows = list_all_windows(visible_only=True, non_minimized_only=True)
    for window in filtered_windows:
        c.print(window)
        
        
    c.print("\nWindows containing 'chrome':")
    chrome_windows = list_all_windows(title_contains="chrome")
    for window in chrome_windows:
        c.print(window)

    # Example: Activate a window by title
    search_title = "Notepad"
    found_notepad = activate_window_by_title(search_title)  # Will activate first window containing "Notepad"
    c.print(f"found {search_title}: {found_notepad}" )
    
    search_title = "Aider"
    found_aider = activate_window_by_title('Aider:')
    c.print(f"found [{search_title}]: {found_aider}")
