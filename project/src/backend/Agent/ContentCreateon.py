
from project.src.backend.Agent.Role import RoleClass


class ContentCreatonClass():
    def create_message(history: list[str], message: str):
        return  [
                {
                "role": RoleClass.SYSTEM.value,
                    "content": "Magyarul beszélsz. Kedves és segítő kész vagy"
                }
                ] + history +[
                {
                    "role": RoleClass.USER.value,
                    "content": message
                }
            ]     
      
       
