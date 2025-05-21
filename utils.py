# utils.py
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
import faiss
import os

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text, chunk_size=300, overlap=50):
    splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.create_documents([text])

def embed_chunks(chunks, model):
    texts = [doc.page_content for doc in chunks]
    return model.encode(texts), texts

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index
