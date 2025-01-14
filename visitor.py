from schemeVisitor import schemeVisitor


class Visitor(schemeVisitor):
    """Classe per interpretar el codi en Scheme."""

    def __init__(self):
        self.environment = {}  # Diccionari per emmagatzemar variables i funcions definides

    def visitRoot(self, ctx):
        """Visita el node arrel i processa totes les expressions o definicions."""
        result = None
        for child in ctx.children:
            result = self.visit(child)  # Avalua cada node fill
        return result

    def visitVardef(self, ctx):
        """Tracta la definició d'una variable."""
        var_name = ctx.IDENTIFIER().getText()  # Nom de la variable
        value = self.visit(ctx.expression())  # Valor de la variable
        self.environment[var_name] = value  # Desa la variable a l'entorn
        return value

    def visitFuncdef(self, ctx):
        """Tracta la definició d'una funció."""
        func_name = ctx.IDENTIFIER().getText()  # Nom de la funció
        parameters = [p.getText()
                      for p in ctx.parameters().IDENTIFIER()]  # Paràmetres
        body = ctx.expression()  # Cos de la funció
        self.environment[func_name] = {
            "params": parameters,
            "body": body}  # Desa la funció a l'entorn
        return func_name

    def visitfuncCall(self, ctx):
        """Tracta una crida a funcions."""
        func_name = ctx.IDENTIFIER().getText()
        if func_name not in self.environment:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: Funció '{func_name}' no definida.")
        func = self.environment[func_name]

        if "params" in func:  # Funció definida per l'usuari
            arguments = [self.visit(arg) for arg in ctx.expression()]
            local_env = {
                param: arg for param,
                arg in zip(
                    func["params"],
                    arguments)}
            old_env = self.environment.copy()
            self.environment.update(local_env)

            result = None
            for expr in func["body"]:
                result = self.visit(expr)

            self.environment = old_env
            return result
        elif callable(func):  # Funció predefinida
            arguments = [self.visit(arg) for arg in ctx.expression()]
            return func(*arguments)
        else:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: La funció '{func_name}' no és callable.")

    def visitOperatorExpression(self, ctx):
        """Tracta operacions amb operadors aritmètics."""
        operator = ctx.operator().getText()

        if len(ctx.expression()) < 2:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: Operació matemàtica '{operator}' necessita almenys dos operands.")

        operand1 = self.visit(ctx.expression(0))
        operand2 = self.visit(ctx.expression(1))

        if operator == "+":
            return operand1 + operand2
        elif operator == "-":
            return operand1 - operand2
        elif operator == "*":
            return operand1 * operand2
        elif operator == "/":
            return operand1 / operand2
        elif operator == "mod":
            return operand1 % operand2
        else:
            raise Exception(f"Error a la línia {line}, columna {column}: Operador no reconegut: {operator}")

    def visitCondExpression(self, ctx):
        """Tracta les expressions cond (condicional)."""
        if ctx.IF():
            condition = self.visit(ctx.expression(0))
            if condition == "#t":
                return self.visit(ctx.expression(1))
            else:
                return self.visit(ctx.expression(2))

        elif ctx.COND():
            for cond_clause in ctx.condClause():
                if cond_clause.ELSE():  # Si troba un else
                    # Avalua totes les expressions associades a l'else i
                    # retorna l'últim resultat
                    result = None
                    for expr in cond_clause.expression():
                        result = self.visit(expr)
                    return result
                condition = self.visit(
                    cond_clause.expression(0))  # Avalua la condició
                if condition == "#t":
                    # Avalua totes les expressions associades a la condició
                    # certa
                    result = None
                    for expr in cond_clause.expression()[1:]:
                        result = self.visit(expr)
                    return result
            return None

    def visitLogicalExpression(self, ctx):
        """Tracta expressions lògiques (and, or, not, etc.)."""
        logical = ctx.logical().getText()
        operand1 = self.visit(ctx.expression(0))

        if logical == "not":
            return "#t" if operand1 == "#f" else "#f"

        if len(ctx.expression()) < 2:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: Operació lògica '{logical}' necessita almenys dos operands.")

        operand2 = self.visit(ctx.expression(1))

        if logical == "and":
            return "#t" if operand1 == "#t" and operand2 == "#t" else "#f"
        elif logical == "or":
            return "#t" if operand1 == "#t" or operand2 == "#t" else "#f"
        elif logical == "=":
            return "#t" if operand1 == operand2 else "#f"
        elif logical == "<":
            return "#t" if operand1 < operand2 else "#f"
        elif logical == ">":
            return "#t" if operand1 > operand2 else "#f"
        elif logical == "<=":
            return "#t" if operand1 <= operand2 else "#f"
        elif logical == ">=":
            return "#t" if operand1 >= operand2 else "#f"
        elif logical == "<>":
            return "#f" if operand1 == operand2 else "#t"
        else:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: Operador lògic '{logical}' no reconegut.")

    def visitLetExpression(self, ctx):
        """Tracta les expressions let (entorns locals)."""
        local_env = self.environment.copy()
        for declaration in ctx.declaration():
            var_name = declaration.IDENTIFIER().getText()
            value = self.visit(declaration.expression())
            local_env[var_name] = value

        old_env = self.environment
        self.environment = local_env

        result = None
        for expr in ctx.expression():
            result = self.visit(expr)

        self.environment = old_env
        return result

    def format_list(self, lst):
        """Converteix una llista Python al format de llistes de Scheme."""
        if isinstance(lst, list):
            return f"({' '.join(map(self.format_list, lst))})"
        return str(lst)

    def visitInoutExpression(self, ctx):
        """Tracta operacions d'entrada/sortida (display, read, newline)."""
        if ctx.DISPLAY():
            value = self.visit(ctx.expression())
            if isinstance(value, list):
                # Formata la llista al format de Scheme
                value = self.format_list(value)
            print(value, end="")  # No salta de línia
            return value
        elif ctx.READ():
            # Leer entrada del usuario
            value = input().strip()
            # Detectar si es una lista citada
            if value.startswith("'(") and value.endswith(")"):
                # Eliminar el "'" inicial y los paréntesis externos
                list_content = value[2:-1].strip()
                # Procesar los elementos de la lista
                elements = list_content.split()  # Separar por espacios
                processed_elements = []
                for element in elements:
                    # Convertir cada elemento a su tipo correspondiente
                    if element.isdigit():
                        processed_elements.append(
                            int(element))  # Convertir a int
                    elif element.replace('.', '', 1).isdigit():
                        processed_elements.append(
                            float(element))  # Convertir a float
                    elif element in ("#t", "#f"):
                        processed_elements.append(element)  # Booleano
                    else:
                        processed_elements.append(element.strip('"'))  # Cadena
                return processed_elements
            # Procesar como valor simple si no es una lista citada
            if value.isdigit():
                return int(value)  # Convertir a int
            elif value.replace('.', '', 1).isdigit():
                return float(value)  # Convertir a float
            elif value in ("#t", "#f"):
                return value  # Booleano
            else:
                return value.strip('"')  # Cadena
        elif ctx.NEWLINE():
            print()
            return None

    def visitQuotedExpression(self, ctx):
        """Tracta llistes literals citades ('(1 2 3))."""
        elements = ctx.literal()
        return [self.visitLiteral(elem) for elem in elements]

    def visitListExpression(self, ctx):
        """Tracta operacions de llista (car, cdr, cons, null?)."""
        if ctx.CAR():
            lst = self.visit(ctx.expression(0))
            if not isinstance(lst, list):
                line = ctx.start.line
                column = ctx.start.column
                raise Exception(f"Error a la línia {line}, columna {column}: CAR només funciona amb llistes. Valor rebut: {lst}")
            return lst[0] if lst else None
        elif ctx.CDR():
            lst = self.visit(ctx.expression(0))
            if not isinstance(lst, list):
                line = ctx.start.line
                column = ctx.start.column
                raise Exception(f"Error a la línia {line}, columna {column}: CDR només funciona amb llistes. Valor rebut: {lst}")
            return lst[1:] if lst else []
        elif ctx.CONS():
            first = self.visit(ctx.expression(0))
            rest = self.visit(ctx.expression(1))
            if not isinstance(rest, list):
                line = ctx.start.line
                column = ctx.start.column
                raise Exception(f"Error a la línia {line}, columna {column}: CONS espera una llista com a segon operand. Valor rebut: {rest}")
            return [first] + rest
        elif ctx.NULLP():
            lst = self.visit(ctx.expression(0))
            if not isinstance(lst, list):
                line = ctx.start.line
                column = ctx.start.column
                raise Exception(f"Error a la línia {line}, columna {column}: NULLP només funciona amb llistes. Valor rebut: {lst}")
            return "#t" if not lst else "#f"
        else:
            line = ctx.start.line
            column = ctx.start.column
            raise Exception(f"Error a la línia {line}, columna {column}: Operació de llista no reconeguda: {ctx.getText()}")

    def visitLiteral(self, ctx):
        """Tracta literals (números, booleans i cadenes)."""
        if ctx.NUMBER():
            number_text = ctx.NUMBER().getText()
            return float(number_text) if '.' in number_text else int(
                number_text)
        elif ctx.BOOLEAN():
            return "#t" if ctx.BOOLEAN().getText() == "#t" else "#f"
        elif ctx.STRING():
            return ctx.STRING().getText().strip('"')
        return None

    def visitExpression(self, ctx):
        """Determina el tipus d'expressió i delega la seva avaluació."""
        if ctx.literal():
            return self.visitLiteral(ctx.literal())
        elif ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            if var_name not in self.environment:
                line = ctx.start.line
                column = ctx.start.column
                raise Exception(f"Error a la línia {line}, columna {column}: Variable '{var_name}' no definida.")
            return self.environment.get(var_name, None)
        elif ctx.operatorExpression():
            return self.visitOperatorExpression(ctx.operatorExpression())
        elif ctx.logicalExpression():
            return self.visitLogicalExpression(ctx.logicalExpression())
        elif ctx.funcCall():
            return self.visitfuncCall(ctx.funcCall())
        elif ctx.inoutExpression():
            return self.visitInoutExpression(ctx.inoutExpression())
        elif ctx.quotedExpression():
            return self.visitQuotedExpression(ctx.quotedExpression())
        elif ctx.listExpression():
            return self.visitListExpression(ctx.listExpression())
        elif ctx.condExpression():
            return self.visitCondExpression(ctx.condExpression())
        elif ctx.letExpression():
            return self.visitLetExpression(ctx.letExpression())
        return None