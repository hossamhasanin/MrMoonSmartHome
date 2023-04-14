from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

r = faiss.IndexFlatIP(384)
with open("G:\\Projects\AI\\rasaChat\\bot\\models\\rooms_embeddings.pkl", "rb") as file:
        stored_data = pickle.load(file)
        r.add(stored_data['embeddings'])

model = SentenceTransformer("G:\\Projects\\AI\\rasaChat\\bot\\models\\all-MiniLM-L12-v2")