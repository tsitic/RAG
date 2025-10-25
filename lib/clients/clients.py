from typing import TypedDict


import chromadb


from lib.processors import DataProcessor
from lib.models import Embedder

class DBClient:
    def __init__(self, path: str = "./chroma_db", collection_name: str = "rf_constitution"):
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=path)
        self.processor = DataProcessor()
   
        try:
            self.client.get_collection(name=self.collection_name)

            print(f"Collection {self.collection_name} has been found") # change to logger

        except Exception:
            self.collection = self.client.create_collection(name=self.collection_name,
                                                            embedding_function=self.embedder)

            print(f"Collection {self.collection_name} has not been found") # change to logger
            print(f"Collection {self.collection_name} has been created") # change to logger

    def embedder(self, texts):
        return Embedder.encode(texts=texts)
    
    def load_data(self, path):
        try:
            with open(path, "r", encoding="UTF-8") as f:
                text = f.read()

        except (FileExistsError, FileNotFoundError) as e:
            print(f"Problem with loading a data: {e}") # change to logger
            raise
        chunks = self.processor.process(text=text) # change to logger
        print(f"Loaded {len(chunks)} chunks.")

        return chunks

    def extract_data(self):
        chunks = self.load_data("data/raw/processed")
        
        if not chunks:
            print(f"No chunks to load") 

        documents = []
        metadatas = []
        ids = []

        for i, document in enumerate(chunks):
            documents.append(document["text"])
            metadatas.append(document["metadata"])

            doc_part = document["metadata"]["document_part"]
            
            if doc_part == "Preamble":
                ids.append(f"preamble")

            elif doc_part == "Section":
                section_num = document["metadata"]["section"]
                ids.append(f"section_{section_num}")

            elif doc_part == "Chapter":
                chapter_num = document["metadata"]["chapter"]
                ids.append(f"chapter_{chapter_num}")
            
            elif doc_part == "Article":
                article_num = document["metadata"]["article"]
                ids.append(f"article_{article_num}")
            
            else:
                ids.append(i)
            
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            print(f"Successfully added {len(chunks)} in database.") # change to logger
        
        except Exception:
            print(f"Something went wrong during adding chunks in database")# change to logger
            raise
        
    def search(self, query: str, n_results: int, where: dict = None) -> chromadb.QueryResult | None:

        try:
            results = self.collection.query(
                query_texts=query,
                n_results=n_results,
                where=where
            )
            return results
        
        except Exception as e:
            print(f"Something went wrong during database search") # change to logger
            return None

                


#Отдельные сервисы