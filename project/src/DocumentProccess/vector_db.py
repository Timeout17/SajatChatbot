import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from Embedding_service import EmbeddingService

class VectorDBService():

    def __init__(self):
        self.db_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "vector_db"

        self.embedding_service = EmbeddingService()

        self.embedding_fuction = self.embedding_service.get_embedding_function()

    def save_markdown_to_chroma(self, markdown_path: Path) -> None:

        with open(markdown_path, "r", mode="utf-8") as file:
            text: str = file.read()

        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")
        ])


        chucks = splitter.split_text(text)


        db = Chroma.from_documents(
            documents=chucks,
            embedding=self.embedding_fuction,
            persist_directory=self.db_path
        )