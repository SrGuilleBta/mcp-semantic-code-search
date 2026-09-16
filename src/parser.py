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
                "start_line": nodo.lineno,
                "end_line": nodo.end_lineno,
                "code": ast.get_source_segment(source, nodo),
            }
            chunks.append(chunk)
        elif isinstance(nodo, ast.ClassDef):
            chunk = {
                "name": nodo.name,
                "type": "class",
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
                        "start_line": miembro.lineno,
                        "end_line": miembro.end_lineno,
                        "code": ast.get_source_segment(source, miembro),
                    }
                    chunks.append(metodo_chunk)


    return chunks

if __name__ == "__main__":
    resultados = parse_file("src/ejemplo.py")
    for chunk in resultados:
        print(chunk["name"], "->", chunk["type"])
        print(chunk["code"])
        print("---")





