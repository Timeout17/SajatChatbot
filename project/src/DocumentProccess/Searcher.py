import os
from pathlib import Path
from langchain_chroma import Chroma
from project.src.DocumentProccess.Embedding_service import EmbeddingService 

class SearcherClass():
    def __init__(self):
        self.db_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "vector_db"

        self.embedding_service = EmbeddingService()

        self.embedding_fuction = self.embedding_service.get_embedding_function()

        self.db = Chroma(persist_directory=self.db_path, embedding_function=self.embedding_fuction)
   
    def search(self, text: str, top_k: int = 3):

        result = self.db.similarity_search(text, k=top_k)

        if not result:
            return 

        kontextus = "\n\n".join([doc.page_content for doc in result])
        
        return kontextus