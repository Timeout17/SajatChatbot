from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ChatClass():
    id: int 
    user_id: int
    title: str
    created_at: datetime