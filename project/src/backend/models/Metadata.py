from dataclasses import dataclass

@dataclass
class Metadata:
    model: str
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    response_id: str
    created: int