"""
A jelszó hashelésére szolgáló osztály
"""

import bcrypt


class PasswordService:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        A jelszó hashelése
        """
        return bcrypt.hashpw( # első alkalommal hasheli
            password.encode(), # azért kell encodeolni, mert string -> bytot csinál -> 1234 -> b'1234 lesz
            bcrypt.gensalt() # salt-ot is generálunk hozzá, hogy ha két 1234 jelszó van akkor legyen külböző
        ).decode() # majd itt nekünk a b'1234 -> 1234-et kell csinálni, azért decodeolunk a végén

    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        """
        A jelszó vissza fejtése
        """
        return bcrypt.checkpw(
            password.encode(), 
            hashed.encode()
            # mivel mind a kettő oldalt bytnak kell lenni ezért encodoljuk mind a kettőt
        )