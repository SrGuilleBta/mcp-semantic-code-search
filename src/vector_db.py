import chromadb
from chromadb.utils import embedding_functions


def agregar_chunks(coleccion, chunks):
    ids = []
    documents = []
    metadatas = []

    ids_nuevos_por_archivo = {}
    for chunk in chunks:
        chunk_id = chunk["file_path"] + "::" + chunk["name"] + "::" + str(chunk["start_line"])
        ids.append(chunk_id)
        documents.append(chunk["code"])
        metadatas.append({
            "name": chunk["name"],
            "type": chunk["type"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
        })

        if chunk["file_path"] not in ids_nuevos_por_archivo:
            ids_nuevos_por_archivo[chunk["file_path"]] = set()
        ids_nuevos_por_archivo[chunk["file_path"]].add(chunk_id)

    for archivo, ids_nuevos in ids_nuevos_por_archivo.items():
        existentes = coleccion.get(where={"file_path": archivo})
        ids_a_borrar = [id_existente for id_existente in existentes["ids"] if id_existente not in ids_nuevos]
        if ids_a_borrar:
            coleccion.delete(ids=ids_a_borrar)

    coleccion.upsert(ids=ids, documents=documents, metadatas=metadatas)


def obtener_coleccion():
    funcion_embedding = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    cliente = chromadb.PersistentClient(path="/app/data/chroma")
    coleccion = cliente.get_or_create_collection(name= "code_chunks", embedding_function=funcion_embedding)

    return coleccion


def buscar(coleccion, pregunta, n_resultados=5):
    resultado = coleccion.query(query_texts=[pregunta], n_results=n_resultados)

    matches = []
    for i in range(len(resultado["documents"][0])):
        matches.append({
            "name": resultado["metadatas"][0][i]["name"],
            "type": resultado["metadatas"][0][i]["type"],
            "file_path": resultado["metadatas"][0][i]["file_path"],
            "code": resultado["documents"][0][i],
            "distance": resultado["distances"][0][i],
        })

    return matches


if __name__ == "__main__":
    from parser import parse_file
    coleccion = obtener_coleccion()
    chunks = parse_file("src/ejemplo.py")
    agregar_chunks(coleccion, chunks)

    resultados = buscar(coleccion, "a function that adds two numbers")
    for match in resultados: 
        print(match["name"], "-", match["distance"])