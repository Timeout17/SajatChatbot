"""
Itt pedig el tároljuk, hogy és kezeljuk az adatokat
"""

from enum import Enum

class RoleClass(Enum):
    USER: str = "user"
    ASSISTANT: str = "assistant"
    SYSTEM: str = "system"