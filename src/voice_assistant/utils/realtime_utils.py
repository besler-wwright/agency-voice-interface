from dataclasses import dataclass
from enum import Enum, auto

@dataclass(frozen=True)
class RealtimeVoices:
    ALLOY: str = "alloy"
    ECHO: str = "echo" 
    SHIMMER: str = "shimmer"
    ASH: str = "ash"
    BALLAD: str = "ballad"
    CORAL: str = "coral"
    SAGE: str = "sage"
    VERSE: str = "verse"

    @classmethod
    def get_all_voices(cls) -> list[str]:
        """Returns a list of all available voice names"""
        return [
            cls.ALLOY,
            cls.ECHO,
            cls.SHIMMER, 
            cls.ASH,
            cls.BALLAD,
            cls.CORAL,
            cls.SAGE,
            cls.VERSE
        ]
