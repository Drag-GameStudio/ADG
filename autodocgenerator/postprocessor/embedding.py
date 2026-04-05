from google import genai
from google.genai import types
import numpy as np
from typing import Any
import numpy as np

def bubble_sort_by_dist(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][1] > arr[j + 1][1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def get_len_btw_vectors(vector1, vector2) -> float:
    diff = np.linalg.norm(np.array(vector1) - np.array(vector2))
    return float(diff)

def sort_vectors(root_vector, other: dict[str, Any]) -> list[str]:
    sort_list: list[tuple[str, float]] = []

    for el in other:
        len_btw = get_len_btw_vectors(root_vector, other[el])
        sort_list.append((el, len_btw))

    sort_list = bubble_sort_by_dist(sort_list)
    result_list = [el[0] for el in sort_list]

    return result_list

class Embedding:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def get_vector(self, prompt: str) -> list:
        text_response = self.client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=prompt,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )

        if text_response.embeddings is None:
            raise Exception("promblem with embedding")

        return list(text_response.embeddings[0])[0][1]
    


