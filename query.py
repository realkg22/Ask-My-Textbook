import faiss
import pickle
import os
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from transformers import pipeline

index = faiss.read_index("biochem_index.faiss")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

query = "During prolonged fasting, explain how the liver shifts from glycogenolysis to gluconeogenesis and ketone body production, and predict the impact on brain metabolism."
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_vector = np.array(response.data[0].embedding, dtype=np.float32).reshape(1, -1)

k = 5
distances, indices = index.search(query_vector, k)
closest_chunks = [chunks[i] for i in indices[0]]

context_text = "\n\n".join(closest_chunks)
prompt = f"""
    Answer the question based on the context below. Be very concise and limit your response to 2 sentences, explain like I'm a 16 year old and make simple analogies to make explanations simpler.

    Context:
    {context_text}

    Question:
    {query}

    Answer:
    """
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)


# for idx, dist in zip(indices[0], distances[0]):
#     print(f"Distance: {dist:.4f}")
#     print(f"Chunk: {chunks[idx]}\n---")

