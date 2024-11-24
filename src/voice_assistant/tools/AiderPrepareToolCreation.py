import asyncio

from agency_swarm.tools import BaseTool

from voice_assistant.utils.aider_utils import generate_aider_window_title
from voice_assistant.utils.terminal import (
    send_multiple_lines_to_powershell,
    send_single_line_to_powershell,
)


class AiderCreateToolPreparation(BaseTool):
    """
    Prepares Aider for creating a new tool by dropping existing files and adding the appropriate ones to generate a new tool. 
    This ensures a clean state before starting tool creation.
    """

    def run(self):
        """
        Sends the /drop command to the active Aider instance.
        """
        # Run the async function in an event loop
        title = asyncio.run(generate_aider_window_title())
        lines = [
            "/drop",
            "/read-only .instructions/instructions.md",
            "/add src/voice_assistant/tools/*.py"
        ]
        send_multiple_lines_to_powershell(lines, title=title)
        
        return "Aider is ready to create a new tool"

if __name__ == "__main__":
    tool = AiderCreateToolPreparation()
    print(tool.run())
if __name__ == "__main__":
    tool = AiderCreateToolPreparation()
    print(tool.run())
