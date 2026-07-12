import os
from docling.document_converter import DocumentConverter
from pathlib import Path

class DocumentumProcesserClass():

    def __init__(self):
        
        self.path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent / "library"
        # abszolút elérési útját, a mappának

    def processing(self, file: str):
        converter = DocumentConverter()
        source = self.path / file
        doc = converter.convert(source).document

        return doc.export_to_markdown()
if __name__ == "__main__":
    x = DocumentumProcesserClass()

    print(x.path)
