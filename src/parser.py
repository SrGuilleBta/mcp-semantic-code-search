import os
import ast

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    arbol = ast.parse(source)

    chunks = []
    for nodo in arbol.body:
        if isinstance(nodo, ast.FunctionDef):
            chunk = {
            "name": nodo.name,
            "type": "function",
            "file_path": file_path,
            "start_line": nodo.lineno,
            "end_line": nodo.end_lineno,
            "code": ast.get_source_segment(source, nodo),
            }
            chunks.append(chunk)
        elif isinstance(nodo, ast.ClassDef):
            chunk = {
                "name": nodo.name,
                "type": "class",
                "file_path": file_path,
                "start_line": nodo.lineno,
                "end_line": nodo.end_lineno,
                "code": ast.get_source_segment(source, nodo),
            }
            chunks.append(chunk)

            for miembro in nodo.body:
                if isinstance(miembro, ast.FunctionDef):
                    metodo_chunk = {
                        "name": nodo.name + "." + miembro.name,
                        "type": "method",
                        "file_path": file_path,
                        "start_line": miembro.lineno,
                        "end_line": miembro.end_lineno,
                        "code": ast.get_source_segment(source, miembro),
                    }
                    chunks.append(metodo_chunk)


    return chunks


def parse_directory(root_dir):
    ignorar = {".git", "__pycache__", "venv", ".venv", "node_modules", "data"}

    todos_los_chunks = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignorar]

        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                todos_los_chunks.extend(parse_file(file_path))

    return todos_los_chunks




if __name__ == "__main__":
    resultados = parse_directory("src")
    print(f"Total de chunks encontrados: {len(resultados)}")
    for chunk in resultados:
        print(chunk["name"], "->", chunk["type"], "|", chunk["file_path"])





