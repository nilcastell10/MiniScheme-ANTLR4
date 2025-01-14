from antlr4 import InputStream, CommonTokenStream
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from visitor import Visitor
from errorListener import SchemeErrorListener



def main():
    """Punt d'entrada principal."""
    from sys import argv

    if len(argv) < 2:
        print("Ús: python3 scheme.py <nom_fitxer>")
        return

    file_name = argv[1]  # Aquesta línia ara està correctament alineada

    try:
        with open(file_name, "r") as file:
            input_data = file.read()
    except FileNotFoundError:
        print(f"Fitxer '{file_name}' no trobat. Assegura't que el fitxer existeix al directori.")
        return

    input_stream = InputStream(input_data)

    # Crear el lexer i afegir el manejador d'errors
    lexer = schemeLexer(input_stream)
    lexer.removeErrorListeners()  # Eliminar els listeners per defecte
    # Afegir el listener personalitzat
    lexer.addErrorListener(SchemeErrorListener())

    # Crear el parser i afegir el manejador d'errors
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    parser.removeErrorListeners()  # Eliminar els listeners per defecte
    # Afegir el listener personalitzat
    parser.addErrorListener(SchemeErrorListener())

    try:
        tree = parser.root()
    except Exception as e:
        print(e)  # Imprimir només el missatge d'error
        return

    # Crear el visitador i avaluar l'AST
    visitor = Visitor()
    try:
        visitor.visit(tree)
    except Exception as e:
        print(e)  # Imprimir només el missatge d'error sense traça


if __name__ == "__main__":
    main()
