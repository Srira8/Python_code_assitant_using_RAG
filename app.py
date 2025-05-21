# app.py

from utils import load_data, chunk_text, embed_chunks, build_faiss_index
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import faiss
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    print("🔐 Loading API key...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables.")

    client = OpenAI(api_key=api_key)

    print("📄 Loading knowledge base...")
    text = load_data("data/python_basics.txt")
    print("✅ Loaded text.")

    print("✂️ Chunking text...")
    chunks = chunk_text(text)
    print(f"✅ Chunked into {len(chunks)} segments.")

    print("🤖 Loading sentence transformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("🔍 Generating embeddings...")
    embeddings, texts = embed_chunks(chunks, model)
    print(f"✅ Generated {len(embeddings)} embeddings.")

    print("📦 Building FAISS index...")
    index = build_faiss_index(np.array(embeddings))
    print("✅ Index ready.")
    
except Exception as e:
    print("❌ Error during initialization:", e)
    exit(1)

def retrieve_context(query, k=3):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, k)
    return "\n".join([texts[i] for i in I[0]])

def generate_answer(query):
    context = retrieve_context(query)
    prompt = f"""You are a helpful Python coding assistant. Use the following context to answer the question:

Context:
{context}

Question:
{query}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("\n🟢 Assistant is ready. Type your Python questions (or type 'exit' to quit):\n")
    while True:
        try:
            query = input("Ask a Python question: ")
            if query.lower() in ['exit', 'quit']:
                print("👋 Exiting assistant.")
                break
            answer = generate_answer(query)
            print("\nAnswer:", answer, "\n")
        except Exception as e:
            print("⚠️ Error during query processing:", e)
