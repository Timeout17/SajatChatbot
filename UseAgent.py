"""
A lényeges logika, itt történik, mivel az A.i agent-t itt fogok válaszolni, kérdezni is
itt fogunk tudni.
"""

import os
from groq import Groq, RateLimitError
from CreateAgent import CreateCAgentClass
from SajatKivetelek import KliensNemTalalhato, BeszélgetésekSzamaElfogyot
from AgentManager import AgentManagerClass


class UseAgentClass():

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.history = []
        self.manager = AgentManagerClass()

    def Answer(self) -> str:
        """
        A már létrehozott Agent-t használjuk
        """
        client = None

        try:
            client: CreateCAgentClass = CreateCAgentClass.create_client()

        except KliensNemTalalhato as e:
            print(e)

        
        message: str = input("kérdez bármit: ")

        content: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "Magyarul beszélsz. Kedves és segítő kész vagy"
            }
            ] + self.history +[
            {
                "role": "user",
                "content": message
            }
        ]     
        try:
            response = client.chat.completions.create(
                model = self.model,
                messages = content,
                temperature = 0.5,
                max_completion_tokens = 1024,
            )

        except RateLimitError as r:
            print("API limit túlterhelve")

        except BeszélgetésekSzamaElfogyot as e:
            print("Saját limit elérve")
        ai_answer: str = response.choices[0].message.content 
        
        self.history.append({
            "role": "user",
            "content": message
        })

        self.history.append({
            "role": "assistant",
            "content": ai_answer
        })


        self.manager.used += 1
        return ai_answer

if __name__ == "__main__":
    agent: UseAgentClass = UseAgentClass()
    while True:
        print(agent.Answer())