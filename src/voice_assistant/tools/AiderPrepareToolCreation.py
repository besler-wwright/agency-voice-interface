import asyncio

from agency_swarm.tools import BaseTool
from voice_assistant.utils.project_utils import get_tools_folder_path

from voice_assistant.utils.aider_utils import generate_aider_window_title
from voice_assistant.utils.terminal import send_multiple_lines_to_powershell


class AiderCreateToolPreparation(BaseTool):
    """
    Prepares Aider for creating a new tool by dropping existing files and adding the appropriate ones to generate a new tool. 
    This ensures a clean state before starting tool creation.
    """

    async def run(self):
        """
        Sends the commands to the active Aider instance.
        """
        title = await generate_aider_window_title()
        tools_path = await get_tools_folder_path()
        
        # Convert to relative path from git root
        tools_path = tools_path.replace("\\", "/")  # Ensure forward slashes
        
        lines = [
            "/drop",
            "/read-only .instructions/instructions.md",
            f"/add {tools_path}/*.py"
        ]
        send_multiple_lines_to_powershell(lines, title=title)
        
        return "Aider is ready to create a new tool"

if __name__ == "__main__":
    tool = AiderCreateToolPreparation()
    print(asyncio.run(tool.run()))
