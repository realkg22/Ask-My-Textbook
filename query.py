import faiss
import pickle
import os
import numpy as np
import warnings
from openai import OpenAI
from rich import print
from rich.prompt import Prompt

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
index = faiss.read_index("biochem_index.faiss")

def load_chunks(chunks_filename):
    with open(chunks_filename, "rb") as f:
        chunks = pickle.load(f)
    return chunks

def fetch_context_chunks(user_query, chunks):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=user_query
    )

    # Match same dimensions as FAISS embedding dimension
    query_vector = np.array(response.data[0].embedding, dtype=np.float32).reshape(1, -1)

    # Retrieve 5 closest chunks, we can play around with this number
    k = 5
    distances, indices = index.search(query_vector, k)
    closest_chunks = [chunks[i] for i in indices[0]]

    return closest_chunks

def ask_textbook(user_input, chunks):
    context_text = "\n\n".join(chunks)
    prompt = f"""
        You are a tutor. Only answer questions using the provided context.
        If the answer is not in the context, say: "The context does not contain that information."
        Do not use outside knowledge.
        Answer the question based on the context below. Be concise and limit your response to 2-3 sentence.

        If you are told to be detailed or more specific, increase your response to a paragraph of 5-6 sentences.

        Context:
        {context_text}

        Question:
        {user_input}

        Answer:
        """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

user_input = Prompt.ask("[yellow]What would you like to ask your textbook???\n[/yellow]")
chunks = load_chunks("chunks.pkl")
context_chunks = fetch_context_chunks(user_input, chunks)
response = ask_textbook(user_input, context_chunks)
print(f"[green]{response}[/green]")


# index = faiss.read_index("biochem_index.faiss")
# with open("chunks.pkl", "rb") as f:
#     chunks = pickle.load(f)


# query = "Please explain growth factors of epidermal cells in a detailed manner."
# response = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=query
# )

# query_vector = np.array(response.data[0].embedding, dtype=np.float32).reshape(1, -1)

# k = 5
# distances, indices = index.search(query_vector, k)
# closest_chunks = [chunks[i] for i in indices[0]]

# context_text = "\n\n".join(closest_chunks)
# prompt = f"""
#     You are a tutor. Only answer questions using the provided context.
#     If the answer is not in the context, say: "The context does not contain that information."
#     Do not use outside knowledge.
#     Answer the question based on the context below. Be concise and limit your response to 2-3 sentence.

#     If you are told to be detailed or more specific, increase your response to a paragraph of 5-6 sentences.

#     Context:
#     {context_text}

#     Question:
#     {query}

#     Answer:
#     """
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": prompt}]
# )

# print(response.choices[0].message.content)


# for idx, dist in zip(indices[0], distances[0]):
#     print(f"Distance: {dist:.4f}")
#     print(f"Chunk: {chunks[idx]}\n---")

