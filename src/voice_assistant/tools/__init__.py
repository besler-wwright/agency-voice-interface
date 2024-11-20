import importlib
import os
from typing import Any, Dict, List, Type

from agency_swarm.tools import BaseTool
from rich.console import Console

c = Console()



def load_tools() -> List[Type[BaseTool]]:
    tools = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    c.print(f"[bold blue]Loading tools from {current_dir}[/bold blue]")
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            c.print(f"\t[dim]Inspecting Module: {module_name}[/dim]")
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


def prepare_tool_schemas(tools: List[Type[BaseTool]]) -> List[Dict[str, Any]]:
    """Prepare the schemas for the tools.
    
    Args:
        tools: List of tool classes to prepare schemas for
    
    Returns:
        List[Dict[str, Any]]: A list of tool schemas ready for OpenAI consumption
    """
    tool_schemas = []
    for tool in tools:
        tool_schema = {k: v for k, v in tool.openai_schema.items() if k != "strict"}
        tool_type = getattr(tool, "type", "function")
        tool_schemas.append({**tool_schema, "type": tool_type})
    return tool_schemas
