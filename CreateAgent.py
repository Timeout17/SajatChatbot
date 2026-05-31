"""
Itt létrehozzuk a agentet amivel dolgozni fogunk, egy statikus osztályal
Modulokhoz, a groq és az os-t használom

"""
from groq import Groq
import os

class CreateCAgentClass():
    @staticmethod    
    def create_client():
        return Groq(api_key=os.getenv("GROQ_API_KEY"))
    