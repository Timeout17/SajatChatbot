import sqlite3

class DatabaseInitializerClass():
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn


    def CreateUserTable(self):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    email_address TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL,
                    password TEXT NOT NULL
                );
                """
            )

            self.conn.commit()


        except sqlite3.Error as e:
            print(e)

    def CreateChatTable(self):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT,
                    created_at NUMERIC,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );
                """
            )


            self.conn.commit()


        except sqlite3.Error as e:
            print(e)


    def CreateMessage(self):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS message (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    message TEXT,
                    role TEXT,
                    timestamp NUMERIC,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(chat_id) REFERENCES chats(id)
                );
                """
            )


            self.conn.commit()


        except sqlite3.Error as e:
            print(e)

    def CreateMetadata(self):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """
                CREATE TABLE metadata_message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,

                model TEXT NOT NULL,
                tokens_prompt INTEGER NOT NULL,
                tokens_completion INTEGER NOT NULL,
                tokens_total INTEGER NOT NULL,

                response_id TEXT NOT NULL,
                created INTEGER NOT NULL,

                FOREIGN KEY(message_id) REFERENCES message(id)
            );
                """
            )


            self.conn.commit()


        except sqlite3.Error as e:
            print(e)
        
    def Initialize(self):
        self.CreateChatTable()
        self.CreateMessage()
        self.CreateUserTable()    
        self.CreateMetadata()
