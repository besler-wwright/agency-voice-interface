"""
Central registry for managing AI agencies in the voice assistant system.
This module implements the Singleton pattern to ensure a single source of truth
for all agency-related operations across the application.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from agency_swarm import Agency


@dataclass
class AgencyInfo:
    """
    Data container for agency information.
    
    Attributes:
        agency (Agency): The actual agency instance
        description (str): Human-readable description of the agency's purpose
    """
    agency: Agency
    description: str


class AgenciesRegistry:
    """
    Singleton registry for managing all AI agencies in the system.
    
    This class ensures that there is only one instance managing agencies
    throughout the application lifecycle, preventing duplicate registrations
    and maintaining consistency.
    
    Usage:
        # Get registry instance
        registry = AgenciesRegistry()
        
        # Register a new agency
        registry.register("ResearchAgent", research_agency, "Handles research tasks")
        
        # Get an agency
        agency = registry.get_agency("ResearchAgent")
    """
    
    # Singleton instance storage
    _instance = None

    def __new__(cls):
        """
        Ensures only one instance of AgenciesRegistry exists.
        
        Returns:
            AgenciesRegistry: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(AgenciesRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the registry if it hasn't been initialized yet.
        Only runs once due to the singleton pattern.
        """
        if not self._initialized:
            self._agencies: Dict[str, AgencyInfo] = {}
            self._initialized = True
    
    def register(self, name: str, agency: Agency, description: str = "") -> None:
        """
        Registers a new agency in the system.
        
        Args:
            name (str): Unique identifier for the agency
            agency (Agency): The agency instance to register
            description (str, optional): Human-readable description of the agency
        """
        self._agencies[name] = AgencyInfo(agency, description)
    
    def get_agency(self, name: str) -> Optional[Agency]:
        """
        Retrieves an agency by name.
        
        Args:
            name (str): The name of the agency to retrieve
            
        Returns:
            Optional[Agency]: The agency if found, None otherwise
        """
        return self._agencies[name].agency if name in self._agencies else None
    
    @property
    def agencies(self) -> Dict[str, Agency]:
        """
        Provides access to all registered agencies.
        
        Returns:
            Dict[str, Agency]: Dictionary mapping agency names to instances
        """
        return {name: info.agency for name, info in self._agencies.items()}
    
    @property
    def agencies_string(self) -> str:
        """
        Creates a human-readable string of all registered agencies.
        
        Returns:
            str: Multiline string with agency names and descriptions
        """
        return "\n".join(
            f"{name}: {info.description}"
            for name, info in self._agencies.items()
        )

    def get_available_agencies(self) -> str:
        """
        Gets a comma-separated list of available agency names.
        
        Returns:
            str: Comma-separated list of agency names
        """
        return ", ".join(self._agencies.keys())
