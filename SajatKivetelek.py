"""
Amiket én hozzok létre kivételek, a könnyebb olvashatóság. és a védelem tekintetében
"""

class KliensNemTalalhato(Exception):
    def __init__(self, message="A kliens nem található"):
        super().__init__(message)



class BeszélgetésekSzamaElfogyot(Exception):
    def __init__(self, message="Nem tudsz többet beszélni vele"):
        super().__init__(message) 


