import numpy as np
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from citrusdb import Client

app = FastAPI()
client = Client(persist_directory="citrus")

@app.post("/index")
def create_index(index_name: str, max_elements: int = 1000, allow_replace_deleted: bool = True, M = 64, ef_construction = 200):
    try:
        client.create_index(
            name=index_name,
            max_elements=max_elements,
            allow_replace_deleted=allow_replace_deleted,
            M=M,
            ef_construction=ef_construction
        )
        return {"message": f"Index '{index_name}' created successfully."}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

@app.post("/insert")
def insert_elements(index_name: str, elements: list[dict]):
    try:
        embeddings = None
        texts = None
        ids = [element["id"] for element in elements]

        keys = elements[0].keys()
        if "embedding" in keys:
            embeddings = np.asarray([element["embedding"] for element in elements], np.float32)
        if "text" in keys:
            texts = [element["text"] for element in elements]

        metadatas = [element["metadata"] for element in elements]

        client.add(index=index_name, ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        return {"message": f"{len(ids)} vectors indexed."}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

@app.get("/search")
def semantic_search(index_name: str, search: dict, k: int = 1):
    try:
        res = client.query(index=index_name, query_embeddings=np.asarray([search["embedding"]]), k=k)
        if res:
            results, distances = res
            response = []
            for i, result in enumerate(results):
                for j, id in result:
                    obj = {"id": id, "similarity_score": 1 - distances[i][j]}
                    response.append(obj)  # Assuming documents is accessible here
            return {"results": response}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

'''
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

