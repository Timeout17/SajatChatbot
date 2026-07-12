from project.src.DocumentProccess.DocumentProcesser import DocumentumProcesserClass
from pathlib import Path
import os

class SystemClass():
    

    def __init__(self):
        self.documentum_processer = DocumentumProcesserClass()
        self.db_path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "result"

    def work(self, file_absolute_path: str):
        doc = self.documentum_processer.processing(file_absolute_path)

        tiszta_filenev = Path(file_absolute_path).stem # csak a fájl nevet adj vissza, kiterjesztés nélkül

        file_url = self.db_path / f"{tiszta_filenev}.md"

        with open(file_url, mode="a", encoding="utf-8") as fajl:
            fajl.write(doc)

        print(f"--> SIKER: A fájl mentve a RESULT mappába: {file_url}")