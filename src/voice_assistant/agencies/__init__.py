import importlib
import os

from rich.console import Console

from voice_assistant.tools.registry import AgenciesRegistry


def initialize_registry():
    """Initialize the registry with all available agencies."""
    registry = AgenciesRegistry()
    c = Console()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    c.print(f"[bold green]Loading agencies from {current_dir}[/bold green]")

    for agency_folder in os.listdir(current_dir):
        agency_path = os.path.join(current_dir, agency_folder)
        if os.path.isdir(agency_path) and agency_folder != "__pycache__":
            try:
                c.print(f"\t[dim]Inspecting Module: {agency_folder}[/dim]")
                agency_module = importlib.import_module(f"voice_assistant.agencies.{agency_folder}.agency")
                agency = getattr(agency_module, "agency")
                description = f"Agency with agents: {', '.join(agent.name for agent in agency.agents)}"
                registry.register(agency_folder, agency, description)
                c.print("\t[green]Agency registered successfully.[/green]")
            except (ImportError, AttributeError) as e:
                c.print(f"Error loading agency {agency_folder}: {e}")

    return registry

# Initialize the registry when this module is imported
registry = initialize_registry()
