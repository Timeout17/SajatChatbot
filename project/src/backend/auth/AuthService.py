"""
A bejelentkezést, regisztrációt, és a jelszó szabályokat itt vizsgáljuk
"""


from project.src.backend.auth.PasswordService import PasswordService
from project.src.backend.models.Person import Person
from project.src.backend.db.DAO import DAOCLass
import re

class AuthServiceClass():
    def __init__(self, user_dao: DAOCLass):
        self.user_dao = user_dao

    def Registration(self, username: str, lastname: str, firstname: str, password: str, email: str):
        if not self.ValidatePassword(password):
            return 
        
        hash_password = PasswordService().hash_password(password)

        user = Person(
            username=username,
            lastname=lastname,
            firtstname=firstname,
            email_address=email,
            password = hash_password
        )

        self.user_dao.NewUser(user)


    def Login(self, username: str, password: str):
        current_user: Person = self.user_dao.UserConnention(username=username, password=password)

        return current_user


    def ValidatePassword(self, password: str) -> bool:
        if len(password) < 8:
            return False

        if not re.search(r"[A-Z]", password): # A-Z-ig minden nagy betű
            return False

        if not re.search(r"[a-z]", password): # a-z ig minden kis betű
            return False

        if not re.search(r"\d", password): # bármilyen szám
            return False

        if not re.search(r"[!@#$%^&*]", password): # a []-ben lévő karakterek
            return False

        return True