import asyncio

from agency_swarm.tools import BaseTool
from rich.console import Console

from voice_assistant.utils.aider_utils import tell_aider_several_things
from voice_assistant.utils.project_utils import get_tools_folder_path


class AiderPrepareToolCreation(BaseTool):
    """
    Prepares Aider for creating a new tool by dropping existing files and adding the appropriate ones to generate a new tool. 
    This ensures a clean state before starting tool creation.
    """

    async def run(self):
        """
        Sends the commands to the active Aider instance.
        """
        
        tools_path = await get_tools_folder_path()
        
        # Convert to relative path from git root
        tools_path = tools_path.replace("\\", "/")  # Ensure forward slashes
        
        lines = [
            "/drop",
            "/read-only .instructions/instructions.md",
            f"/read-only {tools_path}/*.py"
        ]
        return await tell_aider_several_things(lines)


if __name__ == "__main__":
    tool = AiderPrepareToolCreation()
    Console().print(asyncio.run(tool.run()))
