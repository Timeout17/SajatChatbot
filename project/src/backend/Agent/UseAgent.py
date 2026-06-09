"""
A lényeges logika, itt történik, mivel az A.i agent-t itt fogok válaszolni, kérdezni is
itt fogunk tudni.
"""

from groq import Groq, RateLimitError
from project.src.backend.Agent.CreateAgent import CreateCAgentClass
from project.src.backend.exceptions.SajatKivetelek import KliensNemTalalhato, BeszélgetésekSzamaElfogyot
from project.src.backend.Agent.AgentManager import AgentManagerClass
from project.src.backend.Agent.Role import RoleClass
from project.src.backend.Agent.Message import MessageClass
from project.src.backend.Agent.ContentCreateon import ContentCreatonClass
from project.src.backend.Agent.LLMService import LLMServiceClass
from project.src.backend.Agent.Metadatacreaton import MetadataCreatonClass


class UseAgentClass():

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.history = []
        self.manager = AgentManagerClass()

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
    
    def Memory(self, message: str, ai_message: str) -> None:           
        self.history.append({
            "role": RoleClass.USER.value,
            "content": message
        })

        self.history.append({
            "role": RoleClass.ASSISTANT.value,
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
        
        message: str = input("kérdez bármit: ")
        
        content: list[dict[str, str]] = ContentCreatonClass.create_message(self.history, message)
        response = LLMServiceClass.ChatService(self.manager, client, self.model, content)

        ai_answer: str = response.choices[0].message.content

        self.Memory(message=message, ai_message=ai_answer)

        metadata = MetadataCreatonClass.create_metadata(response)

        user_message: MessageClass = MessageClass(message=message, role=RoleClass.USER)
        ai_message: MessageClass = MessageClass(message=ai_answer, role=RoleClass.ASSISTANT, metadata=metadata)

        return ai_answer

    
    def __repr__(self):    
        return f"{self.model}, {self.manager}, {self.history}"
    
    def __str__(self):
        return f"model={self.model}, manager={self.manager}, history={self.history}"

if __name__ == "__main__":
    agent: UseAgentClass = UseAgentClass()
    while True:
        print(agent.Answer())