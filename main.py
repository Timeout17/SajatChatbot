from pathlib import Path
from project.src.backend.db.SQLconnection import DatabaseConnectionClass
from project.src.backend.db.DAO import DAOCLass
from project.src.backend.services.auth.AuthService import AuthServiceClass
from project.src.backend.models.Person import Person
from project.src.backend.Agent.UseAgent import UseAgentClass
from project.src.backend.models.Chat import ChatClass
from project.src.backend.services.Chat.ChatService import ChatServiceClass
from project.src.backend.db.DatabaseInitializer import DatabaseInitializerClass
from project.src.backend.services.auth.PasswordService import PasswordService


def main():

    base_dir = Path(__file__).parent
    db = DatabaseConnectionClass(base_dir)
    conn = db.connect()

    try: # azért kell try-finally, hogy a close mindig lefusson

        user_dao = DAOCLass(conn)
        auth_service = AuthServiceClass(user_dao)
        initializer = DatabaseInitializerClass(conn)
        initializer.Initialize()
        
        """
        kezelő felület
        """

        """
        Van-e fiókod 1
        na nincsen akkor 2
        """

        print("""
              ################################
              #         Regisztrálni         #
              #             Vagy             #
              #         Bejelentkezni        #
              #Regisztráció: 1               #
              #Befejeletkezés: 2             #
              ################################
              """)

        coice: int = int(input("Döntés: "))
        if (coice == 2):
            username: str = input("Mi a neved: ")
            password: str = input("Mi a jelszavad: ")
            current_person: Person = auth_service.Login(username=username, password=password)

        else:
             firstname: str = input("Mi a keresztneved: ")
             lastname: str = input("Mi a vezetékneved: ")
             username: str = input("Mi a felhasználóneved: ")
             raw_password: str = input("Mi a jelszavad: ")
             email: str = input("Mi az emailcímed: ")

             hashed_password = PasswordService.hash_password(raw_password)

             user = Person(
                username=username,
                firstname=firstname,
                lastname=lastname,
                password=hashed_password,
                email_address=email,
             )
             user_dao.NewUser(user)

             current_person: Person = auth_service.Login(username=username, password=raw_password)
             chats = user_dao.ListChats(current_person.id)


             if len(chats) == 0:
                 chat_id = user_dao.CreateChat(current_person.id, "Default chat")
             else:
                 chat_id = chats[0].id

        
        if (current_person is None):
                return
        current_person_all_chats = user_dao.ListChats(current_person.id)

        if len(current_person_all_chats) == 0:
            chat_id = user_dao.NewChat(current_person.id, "Default chat")
        else:
            for chat in current_person_all_chats:
                print(f"{chat.id} - {chat.title}")

            valid_ids = [chat.id for chat in current_person_all_chats]

            print("""
                ###################################
                #         törölni akarsz chatet:  #       
                #         létrehozni:             #
                #         használni:              #
                #                                 #
                # törölni akarsz: 1               #  
                #létrehozni: 2                    #
                # használni: 3                    # 
                ###################################
                """)
            dontes: int = int(input("Döntés: "))
            match dontes:
                case 1:
                    chat_id = int(input("Melyik chatet akarod: "))
                    if chat_id not in valid_ids:
                        print("❌ Hibás chat ID!")
                        return
                    user_dao.DeleteChat(current_person.id, chat_id)
                case 2:
                    neve: str = input("Neve a chatnek: ")
                    chat_id: int = user_dao.NewChat(current_person.id, neve)
                case _:
                    chat_id = int(input("Melyik chatet akarod: "))
                    if chat_id not in valid_ids:
                        print("❌ Hibás chat ID!")
                        return

        agent = UseAgentClass()
        localchat = ChatServiceClass(user_dao, agent)

        message = input("Mi a kérdésed: ")
        answer = localchat.send_message(current_person.id, chat_id, message)

        print(answer)

    finally:
            db.close(conn)

if __name__ == "__main__":
    main()