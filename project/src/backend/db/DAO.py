"""
A rendszerrel tőrténő adatmozgások itt történek
"""


from project.src.backend.db.SQLconnection import DatabaseConnectionClass
from project.src.backend.models.Message import MessageClass
from project.src.backend.models.Person import Person
from project.src.backend.auth.PasswordService import PasswordService
from project.src.backend.models.Chat import ChatClass

class DAOCLass():

    def __init__(self, connection):
        self.conn: DatabaseConnectionClass = connection

    def ListChats(self, user_id: int) -> list[ChatClass]:
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                SELECT * FROM chats WHERE user_id = ?
                """,
                (user_id,)
            )

            rows = cur.fetchall()
            chats = []

            if (len(rows) == 0):
                return []

            for row in rows:
                chats.append(
                    ChatClass(
                        id=row["id"],
                        user_id=row["user_id"],
                        title=row["title"],
                        created_at=row["created_at"]
                    )
                )

            return chats
        except Exception as e:
            print(e)
    
    # generálunk egy chat_id-t az autoincrementtel
    def NewChat():
        """
        A felhasználó indíthat egy teljesen új chatet
        """
        pass

    def DeleteChat():
        """
        A felhasználó törölheti az egyik chatjét
        """
        pass

    def AddMessage(self, actual_message: MessageClass) -> bool:
        """
        Az üzenet hozzá adása, MINDIG lefut amikor üzetetet írunk, vagy kapunk az A.I-tól
        """
        if (actual_message == None):
            return False
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                INSERT INTO message(id, user_id, chat_id, message, role, time, metadata) VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        actual_message.id,
                        actual_message.user_id,
                        actual_message.chat_id,
                        actual_message.message,
                        actual_message.role,
                        actual_message.timestamp,
                        actual_message.metadata
                    )
            )

            self.conn.commit() # módosítás kor kell, amikor csak lekérdezés van, akkor nem kell
            return True

        except Exception as e:
            print("DB error:", e)
            return False

    def DeleteMessage():
        """
        Ez akkor fut le, ha a 20 messagenél többet írtunk, ilyenkor törli a meglévőket
        """
        pass

    def ModifyMessage():
        """
        Tudja módosítani az üzeneteti ha szeretné
        """
        pass
    
    def UserConnention(self, username: str, password: str) -> Person:
        """
        A már regisztrál felhasználókat fogja ellenőrizni, hogy megfelelőek-e
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                SELECT * FROM users WHERE username = ?
                """,
                (username,)
            )

            row = cur.fetchone()

            if row is None:
                return None

            if not PasswordService.verify(password, row["password"]):
                return None

            return Person(
                id=row["id"],
                username=row["username"],
                lastname=row["lastname"],
                firtstname=row["firstname"],
                email_address=row["email_address"],
                role=row["role"],
                password=None
            )


        except Exception as e:
                print("DB error:", e)
                return None

        # generálunk egy user_id-t az autoincrementtel
    def NewUser(self, user) -> bool:
        """
        Legelső alkalommal hozzá adja a felhasználót a táblához
        """
        if (user is None):
            return False
        try:
            cur = self.conn.cursor()
            
            cur.execute(
                """
                INSERT INTO users(username, lastname, firstname, email, role, password) 
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                    (
                        user.username, 
                        user.lastname, 
                        user.firstname, 
                        user.email_address, 
                        user.role, 
                        user.password
                        )
                    )
            
            cur.conn.commit()
            return True
        except Exception as e:
            print("DB error:", e)
            return False

    def LimitCheck():
        """
        Amint eléri a 20-at azutána összegzi egy A.I-al
        """
        pass
