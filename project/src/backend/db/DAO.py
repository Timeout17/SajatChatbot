"""
A rendszerrel tőrténő adatmozgások itt történek
"""

import sqlite3
from project.src.backend.db.SQLconnection import DatabaseConnectionClass
from project.src.backend.models.Message import MessageClass
from project.src.backend.models.Person import Person
from project.src.backend.services.auth.PasswordService import PasswordService
from project.src.backend.models.Chat import ChatClass

class DAOCLass():

    def __init__(self, connection):
        self.conn: sqlite3.Connection  = connection

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
    def NewChat(self, user_id: int, title: str):
        """
        A felhasználó indíthat egy teljesen új chatet
        """
        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO chats(user_id, title, created_at) 
            VALUES (?, ?, datetime('now'))
            """, (user_id, title)
        )

        self.conn.commit()
        return cur.lastrowid

    def DeleteChat(self, user_id: int, chat_id: int):
        """
        A felhasználó törölheti az egyik chatjét
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                DELETE FROM chats WHERE user_id = ? AND chat_id = ?
                """,
                (user_id, chat_id,)
            )

            self.conn.commit()
        except Exception as e:
            print("Nincsen mit törölni")
            print(e)

    def ListMessages(self, chat_id: int, user_id: int) -> list[MessageClass]:
        """
        ki listázza az adott chat-hez tarotzó üzeneteket, majd a memóriához
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                SELECT * FROM message WHERE user_id = ? AND chat_id = ? ORDER BY timestamp
                """,
                (user_id, chat_id)
            )

            rows = cur.fetchall()
            messages = []

            for row in rows:
                messages.append(
                MessageClass(
                    uuid=row["uuid"],
                    user_id=row["user_id"],
                    chat_id=row["chat_id"],
                    message=row["message"],
                    role=row["role"],
                    id=row["id"],
                    timestamp=row["timestamp"]
                    )
                )

            return messages
        except Exception as e:
            print(e)
            return []


    def AddMessage(self, actual_message: MessageClass) -> int:
        """
        Az üzenet hozzá adása, MINDIG lefut amikor üzetetet írunk, vagy kapunk az A.I-tól
        """
        if (actual_message == None):
            return False
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                INSERT INTO message(uuid, user_id, chat_id, message, role, timestamp) VALUES(?, ?, ?, ?, ?, ?)
                """,
                    (
                        actual_message.uuid,
                        actual_message.user_id,
                        actual_message.chat_id,
                        actual_message.message,
                        actual_message.role,
                        actual_message.timestamp,
                    )
            )

            self.conn.commit() # módosítás kor kell, amikor csak lekérdezés van, akkor nem kell
            return cur.lastrowid

        except Exception as e:
            print("DB error:", e)
            return -1
         
    def AddMetaData(self, message_id: int, metadata):
        cur = self.conn.cursor()

        cur.execute("""
            INSERT INTO metadata_message(
                message_id,
                model,
                tokens_prompt,
                tokens_completion,
                tokens_total,
                response_id,
                created
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            message_id,
            metadata.model,
            metadata.tokens_prompt,
            metadata.tokens_completion,
            metadata.tokens_total,
            metadata.response_id,
            metadata.created
        ))

        self.conn.commit()
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
                firstname=row["firstname"],
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
                INSERT INTO users(username, lastname, firstname, email_address, role, password) 
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
            
            self.conn.commit()
            return True
        except Exception as e:
            print("DB error:", e)
            return False

    def LimitCheck():
        """
        Amint eléri a 20-at azutána összegzi egy A.I-al
        """
        pass
