
from project.src.backend.Agent.Role import AgentRoleClass


class ContentCreatonClass():
    @staticmethod
    def create_message(history: list[str], message: str):
        return  [
                {
                "role": AgentRoleClass.SYSTEM.value,
                    "content": "Magyarul beszélsz. Kedves és segítő kész vagy"
                }
                ] + history +[
                {
                    "role": AgentRoleClass.USER.value,
                    "content": message
                }
            ]     
      
       
