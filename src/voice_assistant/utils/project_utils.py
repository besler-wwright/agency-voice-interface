import os

from voice_assistant.utils.git_utils import get_git_root


async def get_tools_folder_path() -> str:
    """
    Recursively searches for a 'tools' folder starting from the git root directory.
    Returns the full path of the first 'tools' folder found.
    
    Returns:
        str: Full path to the tools folder if found, otherwise raises FileNotFoundError
    """
    root_dir = await get_git_root()
    if not root_dir:
        raise FileNotFoundError("Git root directory not found")
    
    for root, dirs, _ in os.walk(root_dir):
        if 'tools' in dirs:
            return os.path.join(root, 'tools')
            
    raise FileNotFoundError("No 'tools' folder found in the project directory")
            
