"""
Amiket én hozzok létre kivételek, a könnyebb olvashatóság. és a védelem tekintetében
"""

class KliensNemTalalhato(Exception):
    def __init__(self, message="A kliens nem található"):
        super().__init__(message)



class TokenekSzamaElfogyot(Exception):
    def __init__(self, message="El fogyotak a tokenjeid"):
        super().__init__(message)   


