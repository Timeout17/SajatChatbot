"""
A Message osztály, ami el tárolja, és rendezi az üzeneteket, és a hozzá kellő adatokat

"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Optional, Dict
from project.src.backend.Agent.Role import PersonRoleClass



@dataclass(frozen=True)
class MessageClass:
    """
        message: az üzenet amit kapunk, vagy írunk\n
        role: vagy mi vagyunk, vagy a rendszer, vagy az A.I amit ír\n
        id: ez egy egyedi sor azonosító, ami szerin tudjuk tárolni az adatokat\n
        timestamp: az aktuális dátum, és idő amikor írva volt az üzenet\n
        metadata: egyéb információ amit az A.I, vagy a rendszer írt\n
    """
    user_id: int
    chat_id: int 
    message: str
    role: PersonRoleClass
    id: str = field(default_factory=lambda: str(uuid.uuid4()), repr=False)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict] = None

    # field nekünk arra kell, hogy többet tudjunk a módosítani az objektum viselkedésén
    # azért kell nekünk a field() mert maga a MessageClass majd betöltődik
        # majd utána az értékek, amikt kiszámolt azok maradnak, és ezeket fogja 
        # mindig bele rakni az új objektumokba, ezért kell nekünk a field(), hogy mindig más legyen
        # a time, és az id is, mind a kettő más legyen, a fenti kódban értekben nem érték van el tárolva, hanem a számolás
        # hoz kellő függvény, amivel kiszámolju. 
        # ezért a default_factory, mindig lefut, és mindig kiszámolják az értéket