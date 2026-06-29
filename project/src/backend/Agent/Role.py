"""
Itt pedig el tároljuk, hogy és kezeljuk az adatokat
"""

from enum import Enum

class AgentRoleClass(Enum):
    USER: str = "user"
    ASSISTANT: str = "assistant"
    SYSTEM: str = "system"


class PersonRoleClass(Enum):
    STANDARD_USER: str = "user"
    ADMIN: str = "admin"
    MODERATOR: str = "moderator"
    PREMIUM_USER: str = "premium user"
