
from project.src.backend.exceptions.SajatKivetelek import BeszélgetésekSzamaElfogyot 

class AgentManagerClass():
    def __init__(self):
        self.used = 0

    def check_limit(self):
        if self.used > 1400:
            raise BeszélgetésekSzamaElfogyot()  