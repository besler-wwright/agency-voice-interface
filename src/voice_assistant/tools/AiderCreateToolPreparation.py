from agency_swarm.tools import BaseTool
from pydantic import Field
import asyncio
from voice_assistant.utils.aider_utils import generate_aider_window_title
from voice_assistant.utils.terminal import send_single_line_to_powershell

class AiderCreateToolPreparation(BaseTool):
    """
    Prepares Aider for creating a new tool by sending the /drop command to clear any existing changes.
    This ensures a clean state before starting tool creation.
    """

    def run(self):
        """
        Sends the /drop command to the active Aider instance.
        """
        # Run the async function in an event loop
        title = asyncio.run(generate_aider_window_title())
        send_single_line_to_powershell("/drop", title=title)
        return "Sent /drop command to Aider to clear pending changes"

if __name__ == "__main__":
    tool = AiderCreateToolPreparation()
    print(tool.run())
