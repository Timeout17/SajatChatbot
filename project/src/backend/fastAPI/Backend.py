import os
import sys
import shutil

sys.path.append(os.getcwd()) 

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path

# --- RENDSZERED IMPORTJAI ---
from project.src.backend.db.SQLconnection import DatabaseConnectionClass
from project.src.backend.db.DAO import DAOCLass
from project.src.backend.services.auth.AuthService import AuthServiceClass
from project.src.backend.services.auth.PasswordService import PasswordService
from project.src.backend.models.Person import Person
from project.src.backend.Agent.UseAgent import UseAgentClass
from project.src.backend.services.Chat.ChatService import ChatServiceClass
from project.src.backend.db.DatabaseInitializer import DatabaseInitializerClass
from project.src.DocumentProccess.System import SystemClass 
from project.src.DocumentProccess.Searcher import SearcherClass

app = FastAPI(title="Nagy Vállalati RAG API")

class Message(BaseModel):
    user_id: int
    chat_id: int
    prompt: str

@app.post("/new_chat")
def create_new_chat(user_id: int):
    base_dir = Path("c:/SajatChatbot V1/project")
    db = DatabaseConnectionClass(base_dir)
    conn = None
    try:
        conn = db.connect()
        user_dao = DAOCLass(conn)
        
        new_chat_id = user_dao.NewChat(user_id, title="New chat") 
        return {"chat_id": new_chat_id}
    except Exception as e:
        # KŐKEMÉNY DEBUG: Ez kiírja a terminálba a pontos SQLite hibaüzenetet!
        print(f"❌ NEW_CHAT SQL HIBA: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Hiba az új chat létrehozásakor: {str(e)}")
    finally:
        if conn is not None:
            db.close(conn)

@app.get("/get_user_chats")
def get_user_chats(user_id: int):
    base_dir = Path("c:/SajatChatbot V1/project")
    db = DatabaseConnectionClass(base_dir)
    conn = None
    try:
        conn = db.connect()
        user_dao = DAOCLass(conn)
        
        # JAVÍTÁS: A te valódi DAO függvényedet hívjuk meg!
        chats = user_dao.ListChats(user_id) 
        
        return chats  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hiba a chatek lekérésekor: {str(e)}")
    finally:
        if conn is not None:
            db.close(conn)

@app.post("/registration")
def BackEnd_Registration(username: str, firstname: str, lastname: str, email: str, password: str):
    base_dir = Path("c:/SajatChatbot V1/project") 
    db = DatabaseConnectionClass(base_dir)
    conn = None

    try:
        conn = db.connect()
        user_dao = DAOCLass(conn)
        auth = AuthServiceClass(user_dao)

        Person = auth.Registration(username, lastname, firstname, password, email)

        if user_dao.NewUser(Person):
            return {"status": "sikeres regisztráció", "user_id": Person.id}
        else:
            return{"status": "már létezik ilyen felhasználó"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adatbázis hiba bejelentkezéskor: {str(e)}")
    
    finally:
        if conn is None:
            db.close()
            print("--> SQL kapcsolat sikeresen lezárva a regisztráció után.")


@app.post("/Login")
def BackEnd_Login(username: str, password: str):

    base_dir = Path("c:/SajatChatbot V1/project") 
    db = DatabaseConnectionClass(base_dir)
    conn = None

    try:
        conn = db.connect() # Kinyitjuk az SQL kaput
        
        user_dao = DAOCLass(conn)
        auth = AuthServiceClass(user_dao)

        person = auth.Login(username, password)

        if person is not None:
            return {"status": "fasza minden", "user_id": person.id}
        else:
            return {"status": "Nem tudom mi legyen most", "detail": "Hibás adatok!"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adatbázis hiba bejelentkezéskor: {str(e)}")
        
    finally:
        # Biztonságosan bezárjuk az ajtót, hogy ne ragadjon be az SQLite fájl
        if conn is not None:
            db.close(conn)
    

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    library_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "library"
    library_dir.mkdir(parents=True, exist_ok=True)

    file_path = library_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print("El kezdtem ezen dolgozni")
    system = SystemClass()

    system.work(file_path)
    print("töröltem amit kell")

    os.remove(file_path)
    print("vissza adtam amit kell")
    return {"status": "success", "detail": "Feldolgozva!"}



@app.post("/query")
def search_rag(request: Message):
    try:
        print(f"--> Keresés indítása a következő prompttal: {request.prompt}")
        base_dir = Path("c:/SajatChatbot V1/project")
        db = DatabaseConnectionClass(base_dir)

        conn = db.connect()
        agent = UseAgentClass()
        user_dao=DAOCLass(conn)

        localchat = ChatServiceClass(user_dao, agent)

        answer = localchat.send_message(request.user_id, request.chat_id, request.prompt)

        print(f"--> Keresés sikeres! Visszakapott adat típusa: {type(answer)}")

        return {"status": "succes", "result": answer}
    
    except Exception as e:

        import traceback
        error_details = traceback.format_exc()
        print(f"❌ BACKEND HIBA:\n{error_details}")
        
        raise HTTPException(status_code=500, detail=f"Hiba a BookSearcher-ben: {str(e)}")
    
    finally:

        if conn is not None:
            db.close(conn)
            print("--> SQL kapcsolat sikeresen lezárva a háttérben.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)