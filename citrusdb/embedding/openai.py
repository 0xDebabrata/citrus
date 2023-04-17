import os
from typing import List
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embeddings(data: List[str], model = "text-embedding-ada-002"):
    strings = [text.replace("\n", " ") for text in data]

    response = openai.Embedding.create(
            model=model,
            input=strings)

    return [result["embedding"] for result in response["data"]]


