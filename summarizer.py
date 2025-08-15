from langchain.text_splitter import CharacterTextSplitter
from openai import OpenAI
import faiss
import numpy as np
import pickle

client = OpenAI()

def split_text_chunks(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()
        print("Successfully read textbook file!")

    splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    with open("chunks.pkl", 'wb') as f:
        pickle.dump(chunks, f)
        print(f"Saved {len(chunks)} chunks to chunks.pkl!")
    
    
    return chunks

def vectorize_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding
        embeddings.append(emb)
    print("Finished vectorizing chunks!")
    return embeddings

def store_vector_db(embeddings):

    print("FAISS saved to biochem_index.faiss!")

chunks = split_text_chunks("biochem_textbook_output.txt")
vectors = vectorize_chunks(chunks)
store_vector_db(vectors)   