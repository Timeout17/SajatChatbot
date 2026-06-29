"""
A lényeges logika, itt történik, mivel az A.i agent-t itt fogok válaszolni, kérdezni is
itt fogunk tudni.
"""

from project.src.backend.Agent.CreateAgent import CreateCAgentClass
from project.src.backend.exceptions.SajatKivetelek import KliensNemTalalhato, BeszélgetésekSzamaElfogyot
from project.src.backend.Agent.AgentManager import AgentManagerClass
from project.src.backend.Agent.Role import AgentRoleClass
from project.src.backend.models.Message import MessageClass
from project.src.backend.Agent.ContentCreateon import ContentCreatonClass
from project.src.backend.Agent.LLMService import LLMServiceClass
from project.src.backend.Agent.Metadatacreaton import MetadataCreatonClass
from project.src.backend.db.DAO import DAOCLass


class UseAgentClass():

    def __init__(self, current_user_id: int, chat_id: int, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.history = []
        self.manager = AgentManagerClass()
        self.user_id = current_user_id
        self.user_id = chat_id
        
    def DefineAgent(self) -> None | CreateCAgentClass:
        """
        Létrehozzuk a clienset amivel dolgozni fogunk
        """
        client = None

        try:
            client: CreateCAgentClass = CreateCAgentClass.create_client()

        except KliensNemTalalhato as e:
            print(e)

        return client
    
    """
    ez lesz át írva majd a sqliteos insert
    """
    def Memory(self, message: str, ai_message: str) -> None:           
        self.history.append({
            "role": AgentRoleClass.USER.value,
            "content": message
        })

        self.history.append({
            "role": AgentRoleClass.ASSISTANT.value,
            "content": ai_message
        })

        self.manager.used += 1

    def Answer(self) -> str:

        """
        A már létrehozott Agent-t használjuk
        """

        client: CreateCAgentClass | None = self.DefineAgent()

        if (client == None):
            return "a kliens nem található"
        
        message: str = input("kérdezz bármit: ")
        
        content: list[dict[str, str]] = ContentCreatonClass.create_message(self.history, message)
        response = LLMServiceClass.ChatService(self.manager, client, self.model, content)

        ai_answer: str = response.choices[0].message.content

        self.Memory(message=message, ai_message=ai_answer)

        metadata = MetadataCreatonClass.create_metadata(response)

        user_message: MessageClass = MessageClass(message=message, role=AgentRoleClass.USER, user_id=self.user_id)
        ai_message: MessageClass = MessageClass(message=ai_answer, role=AgentRoleClass.ASSISTANT, metadata=metadata, user_id=self.user_id)



        return ai_answer

    
    def __repr__(self):    
        return f"{self.model}, {self.manager}, {self.history}"
    
    def __str__(self):
        return f"model={self.model}, manager={self.manager}, history={self.history}"

if __name__ == "__main__":
    agent: UseAgentClass = UseAgentClass()
    while True:
        print(agent.Answer())