from dataclasses import dataclass
from typing import Dict, Optional

from agency_swarm import Agency


@dataclass
class AgencyInfo:
    agency: Agency
    description: str


class AgenciesRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgenciesRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._agencies: Dict[str, AgencyInfo] = {}
            self._initialized = True
    
    def register(self, name: str, agency: Agency, description: str = "") -> None:
        self._agencies[name] = AgencyInfo(agency, description)
    
    def get_agency(self, name: str) -> Optional[Agency]:
        return self._agencies[name].agency if name in self._agencies else None
    
    @property
    def agencies(self) -> Dict[str, Agency]:
        return {name: info.agency for name, info in self._agencies.items()}
    
    @property
    def agencies_string(self) -> str:
        return "\n".join(
            f"{name}: {info.description}"
            for name, info in self._agencies.items()
        )

    def get_available_agencies(self) -> str:
        return ", ".join(self._agencies.keys())
