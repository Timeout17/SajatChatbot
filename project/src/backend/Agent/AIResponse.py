from dataclasses import dataclass

@dataclass
class AIResponseClass():
    message: str
    metadata: dict | None = None