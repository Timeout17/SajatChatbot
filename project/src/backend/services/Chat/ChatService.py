from project.src.backend.db.DAO import DAOCLass
from project.src.backend.Agent.UseAgent import UseAgentClass
from project.src.backend.models.Message import MessageClass
from project.src.backend.Agent.Role import AgentRoleClass
from project.src.backend.Agent.Metadatacreaton import MetadataCreatonClass

class ChatServiceClass():
    def __init__(self, dao: DAOCLass, agent: UseAgentClass):
        self.dao = dao
        self.agent = agent

    def send_message(self, user_id: int, chat_id: int, message: str):
        print("USER ID:", user_id)
        print("CHAT ID:", chat_id)
        # létrehozzuk az üzenet objektumot
        msg: MessageClass = MessageClass(
            user_id=user_id, 
            chat_id=chat_id, 
            message=message, 
            role=AgentRoleClass.USER.value
            )

        # hozzáadom a saját üzenetemet
        user_message_id = self.dao.AddMessage(msg)

        # üzenetek lekérdezése
        memory: list[MessageClass] = self.dao.ListMessages(chat_id=chat_id, user_id=user_id)

        memory = [
            {
                "role": m.role,
                "content": m.message
            }
            for m in memory
        ]
        # az A.I válasza
        result = self.agent.Answer(message, memory)

        
        # A.I válasz obketumosítása
        ai_msg: MessageClass = MessageClass(
            user_id=user_id, 
            chat_id=chat_id, 
            message=result.message, 
            role=AgentRoleClass.ASSISTANT.value,
            )
        
            
        
        # Az A.I válaszát is el rakjuk
        ai_message_id = self.dao.AddMessage(ai_msg)
        print("AI message id:", ai_message_id)

        self.dao.AddMetaData(ai_message_id, result.metadata)


        return result.message



        
       
