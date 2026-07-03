"""
A felhasználó mint objektum, itt hozzuk létre

"""

from project.src.backend.Agent.Role import PersonRoleClass
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Person():

    """
    id: a felhasználó egyedi azonosítója\n
    username: a felhasználónak a neve ahogyan mi megszólítjuk\n
    lastname: felhasználó családneve/vezeték neve\n
    firstname: a felhasználó keresztneve\n
    email_address: a felhasználó e-mail címe\n
    role: a felhasználó rangja, eleve mindenki STANDARD_USER\n
    __password: a felhasználó jelszava hashelve
    """

    username: str
    lastname: str
    firstname: str
    email_address: str
    password: str
    id: int | None = None
    role: PersonRoleClass = PersonRoleClass.STANDARD_USER.value

