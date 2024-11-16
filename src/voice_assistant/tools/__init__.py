import importlib

# import logging
import os

from agency_swarm.tools import BaseTool
from rich.console import Console

c = Console()
# logger = logging.getLogger(__name__)


def load_tools():
    tools = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    c.print(f"[bold blue]Loading tools from {current_dir}[/bold blue]")
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            c.print(f"\t[yellow]Inspecting Module: {module_name}[/yellow]")
            module = importlib.import_module(f"voice_assistant.tools.{module_name}")
            for name, obj in module.__dict__.items():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, BaseTool)
                    and obj != BaseTool
                ):
                    tools.append(obj)
                    c.print(f"\t[blue]Loading tool: {name}[/blue]")
    return tools


def prepare_tool_schemas():
    """Prepare the schemas for the tools."""
    tool_schemas = []
    for tool in TOOLS:
        tool_schema = {k: v for k, v in tool.openai_schema.items() if k != "strict"}
        tool_type = getattr(tool, "type", "function")
        tool_schemas.append({**tool_schema, "type": tool_type})
        # c.print("\n\nTool Schema:",tool_schema )   
    return tool_schemas


# Load all tools
TOOLS: list[BaseTool] = load_tools()
TOOL_SCHEMAS = prepare_tool_schemas()
