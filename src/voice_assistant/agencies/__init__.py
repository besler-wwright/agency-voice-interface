import importlib
import os

from agency_swarm import Agency
from rich.console import Console


def load_agencies() -> dict[str, Agency]:
    c = Console()
    agencies = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    c.print(f"[bold green]Loading agencies from {current_dir}[/bold green]")

    for agency_folder in os.listdir(current_dir):
        agency_path = os.path.join(current_dir, agency_folder)
        if os.path.isdir(agency_path) and agency_folder != "__pycache__":
            try:
                c.print(f"\t[dim]Inspecting Module: {agency_folder}[/dim]")
                agency_module = importlib.import_module(f"voice_assistant.agencies.{agency_folder}.agency")
                c.print("\t[green]Agency loaded successfully.[/green]")
                agencies[agency_folder] = getattr(agency_module, "agency")
            except (ImportError, AttributeError) as e:
                c.print(f"Error loading agency {agency_folder}: {e}")

    return agencies


# Load all agencies
AGENCIES: dict[str, Agency] = load_agencies()

AGENCIES_AND_AGENTS_STRING = "\n".join(
    f"Agency '{agency_name}' has the following agents: {', '.join(agent.name for agent in agency.agents)}"
    for agency_name, agency in AGENCIES.items()
)
print("Available Agencies and Agents:\n", AGENCIES_AND_AGENTS_STRING)  # Debug print
