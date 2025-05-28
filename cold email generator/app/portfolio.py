import pandas as pd
import chromadb
import uuid
import os
import pandas as pd

class Portfolio:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # This gets the directory of portfolio.py
        file_path = os.path.join(base_dir, 'resource', 'my_portfolio.csv')  # Correct path relative to portfolio.py
        self.data = pd.read_csv(file_path)


# class Portfolio:
#     def __init__(self, file_path="app/resource/my_portfolio.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
