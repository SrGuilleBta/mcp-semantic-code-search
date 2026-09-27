from mcp.server.mcpserver import MCPServer

from parser import parse_directory
from vector_db import obtener_coleccion, agregar_chunks, buscar

servidor = MCPServer(name = "mcp-semantic-code-search")

@servidor.tool()
def indexar_repositorio(ruta: str) -> str:
    """Analiza un repositorio de código Python y guarda sus funciones, 
    clases y métodos en la base de datos semántica."""
    coleccion = obtener_coleccion()
    chunks = parse_directory(ruta)
    agregar_chunks(coleccion, chunks)
    return f"Se han indexado {len(chunks)} chunks de código desde el repositorio."

@servidor.tool()
def buscar_codigo(pregunta: str) -> str:
    """Busca fragmentos de código relevantes para una pregunta en lenguaje natural."""
    coleccion = obtener_coleccion()
    resultados = buscar(coleccion, pregunta)
    if not resultados:
        return "No se encontraron resultados relevantes."
    
    respuesta = "Resultados de la búsqueda:\n"
    for match in resultados:
        respuesta += f"- {match['name']} ({match['type']}) en {match['file_path']} (distancia: {match['distance']:.4f})\n"
        respuesta += f"  Código:\n{match['code']}\n\n"
    
    return respuesta

if __name__ == "__main__":
    servidor.run()
