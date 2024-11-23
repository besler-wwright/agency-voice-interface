from .git_utils import get_repository_name

async def get_aider_window_title() -> str:
    """
    Generates the window title for Aider terminal window.
    
    Returns:
        str: Window title in format "Aider - {repo_name}"
    """
    git_repo_name = await get_repository_name()
    return f"Aider - {git_repo_name}"
