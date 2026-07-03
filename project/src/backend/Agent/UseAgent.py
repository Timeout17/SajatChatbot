"""
A lényeges logika, itt történik, mivel az A.i agent-t itt fogok válaszolni, kérdezni is
itt fogunk tudni.
"""

from project.src.backend.Agent.CreateAgent import CreateCAgentClass
from project.src.backend.exceptions.SajatKivetelek import KliensNemTalalhato, BeszélgetésekSzamaElfogyot
from project.src.backend.Agent.AgentManager import AgentManagerClass
from project.src.backend.Agent.ContentCreateon import ContentCreatonClass
from project.src.backend.Agent.LLMService import LLMServiceClass
from project.src.backend.Agent.Metadatacreaton import MetadataCreatonClass
from project.src.backend.Agent.AIResponse import AIResponseClass


class UseAgentClass():

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.manager = AgentManagerClass()
        self.client = self.DefineAgent()

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
    def Answer(self, message: str, history: list) -> AIResponseClass:

        """
        A már létrehozott Agent-t használjuk
        """

        if self.client is None:
            return "Klines nem találhato"
                
        content: list[dict[str, str]] = ContentCreatonClass.create_message(history, message)

        response = LLMServiceClass.ChatService(
            self.manager,                                    
            self.client, 
            self.model, 
            content
            )

        ai_answer: str = response.choices[0].message.content
        metadata = MetadataCreatonClass.create_metadata(response)

        return AIResponseClass(
            message=ai_answer,
            metadata=metadata
        )

if __name__ == "__main__":
    agent = UseAgentClass()

    history = []

    while True:
        message = input("Te: ")
        response = agent.Answer(message, history)
        print("AI:", response)

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})