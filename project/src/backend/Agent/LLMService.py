
from project.src.backend.exceptions.SajatKivetelek import BeszélgetésekSzamaElfogyot, KliensNemTalalhato
from groq import RateLimitError
from project.src.backend.Agent.AgentManager import AgentManagerClass

class LLMServiceClass():
    @staticmethod
    def ChatService(manager: AgentManagerClass, client: str, model: str, content: str):
        try:
            manager.check_limit()
            
            response = client.chat.completions.create(
                model = model,
                messages = content,
                temperature = 0.5,
                max_completion_tokens = 1024,
            )

        except RateLimitError as r:
            print("API limit túlterhelve")

        except BeszélgetésekSzamaElfogyot as e:
            print("Saját limit elérve")

        return response
        