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

def list_all_windows():
    """List all windows, including invisible/inactive ones."""
    windows = []
    
    def enum_window_callback(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if title:  # Only include windows with titles
            visible = win32gui.IsWindowVisible(hwnd)
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            results.append({
                'handle': hwnd,
                'title': title,
                'visible': visible,
                'enabled': bool(style & win32con.WS_DISABLED == 0),
                'minimized': bool(style & win32con.WS_MINIMIZE)
            })
    
    win32gui.EnumWindows(enum_window_callback, windows)
    return windows


def activate_window_by_handle(hwnd):
    """Activate a window given its handle."""
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def activate_window_by_title(title, partial_match=True):
    """Activate first window that matches the given title.
    
    Args:
        title (str): Window title to search for
        partial_match (bool): If True, matches substring. If False, requires exact match.
    
    Returns:
        bool: True if window was found and activated, False otherwise
    """
    windows = list_visible_windows()
    
    for hwnd, window_title in windows:
        if (partial_match and title.lower() in window_title.lower()) or \
           (not partial_match and title.lower() == window_title.lower()):
            activate_window_by_handle(hwnd)
            return True
    return False

# Example usage
if __name__ == "__main__":
    # List all windows
    windows = list_all_windows()
    for window in windows:
            print(f"Handle: {window['handle']} | "
                f"Title: {window['title']} | "
                f"Visible: {window['visible']} | "
                f"Enabled: {window['enabled']} | "
                f"Minimized: {window['minimized']}")    

    # Example: Activate a window by title
    search_title = "Notepad"
    found_notepad = activate_window_by_title(search_title)  # Will activate first window containing "Notepad"
    c = Console()
    c.print(f"found {search_title}: {found_notepad}" )
    
    search_title = "Aider"
    found_aider = activate_window_by_title('Aider:')
    c.print(f"found [{search_title}]: {found_aider}")