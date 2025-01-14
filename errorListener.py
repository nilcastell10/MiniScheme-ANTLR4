from antlr4.error.ErrorListener import ErrorListener


class SchemeErrorListener(ErrorListener):
    """Listener personalitzat per capturar errors de sintaxi."""

    def __init__(self):
        super(SchemeErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Error de sintaxi a la línia {line}, columna {column}: {msg}")
