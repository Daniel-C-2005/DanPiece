"""
Intérprete para el lenguaje DanCode con temática de One Piece
Ejecuta código DanCode a partir de su árbol de derivación
"""


class Environment:
    """Ambiente para almacenar variables y funciones"""

    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def define_variable(self, name, value):
        """Define una variable en el ambiente actual"""
        self.variables[name] = value

    def get_variable(self, name):
        """Obtiene una variable del ambiente actual o de sus padres"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise RuntimeError(f"Variable no definida: {name}")

    def define_function(self, name, params, body):
        """Define una función en el ambiente actual"""
        self.functions[name] = (params, body)

    def get_function(self, name):
        """Obtiene una función del ambiente actual o de sus padres"""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise RuntimeError(f"Función no definida: {name}")


class Interpreter:
    """Intérprete para el lenguaje DanCode"""

    def __init__(self):
        self.global_env = Environment()
        self.output = []  # Para almacenar las salidas de proclamar()
        self.return_value = None  # Para manejar valores de retorno de funciones

    def interpret(self, ast):
        """Interpreta un árbol de sintaxis abstracta (AST)"""
        if ast is None:
            return None
        return self._evaluate(ast, self.global_env)

    def get_output(self):
        """Obtiene todas las salidas generadas"""
        return self.output

    def _evaluate(self, node, env):
        """Evalúa un nodo del AST"""
        if isinstance(node, tuple):
            node_type = node[0]

            # Manejo de declaraciones y sentencias
            if node_type == 'programa':
                return self._evaluate_program(node, env)
            elif node_type == 'declaracion_variable':
                return self._evaluate_variable_declaration(node, env)
            elif node_type == 'asignacion':
                return self._evaluate_assignment(node, env)
            elif node_type == 'declaracion_funcion':
                return self._evaluate_function_declaration(node, env)
            elif node_type == 'llamada_funcion':
                return self._evaluate_function_call(node, env)
            elif node_type == 'sentencia_si':
                return self._evaluate_if_statement(node, env)
            elif node_type == 'sentencia_mientras':
                return self._evaluate_while_loop(node, env)
            elif node_type == 'sentencia_para':
                return self._evaluate_for_loop(node, env)
            elif node_type == 'sentencia_retorno':
                return self._evaluate_return_statement(node, env)
            elif node_type == 'sentencia_imprimir':
                return self._evaluate_print_statement(node, env)
            elif node_type == 'bloque':
                return self._evaluate_block(node, env)

            # Manejo de expresiones
            elif node_type == 'expresion':
                return self._evaluate(node[1], env)
            elif node_type == 'expresion_logica':
                return self._evaluate_logical_expression(node, env)
            elif node_type == 'expresion_relacional':
                return self._evaluate_relational_expression(node, env)
            elif node_type == 'expresion_aritmetica':
                return self._evaluate_arithmetic_expression(node, env)
            elif node_type == 'termino':
                return self._evaluate_term(node, env)
            elif node_type == 'factor':
                return self._evaluate_factor(node, env)
            else:
                print(f"Nodo no manejado: {node_type}")

        elif isinstance(node, list):
            # Evaluar una lista de nodos
            result = None
            for item in node:
                result = self._evaluate(item, env)
                # Si encontramos un valor de retorno, salir del bucle
                if self.return_value is not None:
                    break
            return result

        # Para valores literales
        return node

    # Métodos para evaluar diferentes tipos de nodos
    def _evaluate_program(self, node, env):
        """Evalúa un programa completo"""
        return self._evaluate(node[1], env)

    def _evaluate_variable_declaration(self, node, env):
        """Evalúa una declaración de variable"""
        _, tipo, name, expr = node if len(node) == 4 else (node[0], node[1], node[2], None)
        value = None
        if expr:
            value = self._evaluate(expr, env)
        env.define_variable(name, value)
        return value

    def _evaluate_assignment(self, node, env):
        """Evalúa una asignación"""
        _, name, expr = node
        value = self._evaluate(expr, env)
        try:
            # Intentar actualizar la variable existente
            var = env.get_variable(name)
            env.define_variable(name, value)
        except RuntimeError:
            # Si no existe, crear una nueva
            env.define_variable(name, value)
        return value

    def _evaluate_function_declaration(self, node, env):
        """Evalúa una declaración de función"""
        _, name, params, body = node
        env.define_function(name, params, body)
        return None

    def _evaluate_function_call(self, node, env):
        """Evalúa una llamada a función"""
        _, name, args_nodes = node

        # Evaluar los argumentos
        args = []
        for arg_node in args_nodes:
            args.append(self._evaluate(arg_node, env))

        # Manejar funciones incorporadas
        if name == 'proclamar' or name == 'imprimir':
            if args:
                output_str = str(args[0])
                self.output.append(output_str)
                print(f"SALIDA: {output_str}")
            return None

        # Obtener la función definida por el usuario
        try:
            params, body = env.get_function(name)

            # Crear un nuevo ambiente para la función
            function_env = Environment(env)

            # Definir los parámetros como variables
            for i, param_node in enumerate(params):
                if i < len(args):
                    if isinstance(param_node, tuple) and param_node[0] == 'parametro':
                        # param_node es ('parametro', tipo, nombre)
                        param_name = param_node[2]
                        param_value = args[i]
                        function_env.define_variable(param_name, param_value)

            # Resetear el valor de retorno
            self.return_value = None

            # Ejecutar el cuerpo de la función
            self._evaluate(body, function_env)

            # Obtener el valor de retorno si existe
            result = self.return_value

            # Resetear el valor de retorno
            self.return_value = None

            return result
        except RuntimeError as e:
            self.output.append(f"Error: {str(e)}")
            print(f"Error al llamar a la función: {str(e)}")
            return None

    def _evaluate_if_statement(self, node, env):
        """Evalúa una sentencia if"""
        _, condition, if_body, else_body = node
        condition_value = self._evaluate(condition, env)

        if condition_value:
            return self._evaluate(if_body, env)
        elif else_body:
            return self._evaluate(else_body, env)
        return None

    def _evaluate_while_loop(self, node, env):
        """Evalúa un bucle while"""
        _, condition, body = node
        result = None

        while self._evaluate(condition, env):
            result = self._evaluate(body, env)
            # Si encontramos un valor de retorno, salir del bucle
            if self.return_value is not None:
                break

        return result

    def _evaluate_for_loop(self, node, env):
        """Evalúa un bucle for"""
        _, init, condition, increment, body = node
        result = None

        # Inicialización
        self._evaluate(init, env)

        # Bucle
        while self._evaluate(condition, env):
            result = self._evaluate(body, env)
            # Si encontramos un valor de retorno, salir del bucle
            if self.return_value is not None:
                break
            self._evaluate(increment, env)

        return result

    def _evaluate_return_statement(self, node, env):
        """Evalúa una sentencia return"""
        _, expr = node if len(node) > 1 else (node[0], None)
        if expr:
            self.return_value = self._evaluate(expr, env)
        else:
            self.return_value = None
        return self.return_value

    def _evaluate_print_statement(self, node, env):
        """Evalúa una sentencia de impresión"""
        _, expr = node
        value = self._evaluate(expr, env)
        output_str = str(value)
        self.output.append(output_str)
        print(f"SALIDA: {output_str}")
        return None

    def _evaluate_block(self, node, env):
        """Evalúa un bloque de código"""
        _, statements = node
        return self._evaluate(statements, env)

    def _evaluate_logical_expression(self, node, env):
        """Evalúa una expresión lógica"""
        if len(node) == 2:
            return self._evaluate(node[1], env)

        _, left, op, right = node
        left_val = self._evaluate(left, env)
        right_val = self._evaluate(right, env)

        if op == '==' or op == 'IGUAL':
            return left_val == right_val
        elif op == '!=' or op == 'DIFERENTE':
            return left_val != right_val

        return None

    def _evaluate_relational_expression(self, node, env):
        """Evalúa una expresión relacional"""
        if len(node) == 2:
            return self._evaluate(node[1], env)

        _, left, op, right = node
        left_val = self._evaluate(left, env)
        right_val = self._evaluate(right, env)

        if op == '<' or op == 'MENOR':
            return left_val < right_val
        elif op == '>' or op == 'MAYOR':
            return left_val > right_val
        elif op == '<=' or op == 'MENOR_IGUAL':
            return left_val <= right_val
        elif op == '>=' or op == 'MAYOR_IGUAL':
            return left_val >= right_val

        return None

    def _evaluate_arithmetic_expression(self, node, env):
        """Evalúa una expresión aritmética"""
        if len(node) == 2:
            return self._evaluate(node[1], env)

        _, left, op, right = node
        left_val = self._evaluate(left, env)
        right_val = self._evaluate(right, env)

        if op == '+' or op == 'SUMA':
            # Manejar concatenación de cadenas
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            return left_val + right_val
        elif op == '-' or op == 'RESTA':
            return left_val - right_val

        return None

    def _evaluate_term(self, node, env):
        """Evalúa un término"""
        if len(node) == 2:
            return self._evaluate(node[1], env)

        _, left, op, right = node
        left_val = self._evaluate(left, env)
        right_val = self._evaluate(right, env)

        if op == '*' or op == 'MULTIPLICACION':
            return left_val * right_val
        elif op == '/' or op == 'DIVISION':
            if right_val == 0:
                self.output.append("Error: División por cero")
                print("Error: División por cero")
                return 0
            return left_val / right_val

        return None

    def _evaluate_factor(self, node, env):
        """Evalúa un factor"""
        # Si factor es solo un valor, devolver ese valor
        if len(node) == 2:
            factor = node[1]
            if isinstance(factor, tuple):
                if factor[0] == 'llamada_funcion':
                    return self._evaluate(factor, env)
            elif isinstance(factor, str):
                # Valores booleanos y nulo
                if factor == 'conquista':
                    return True
                elif factor == 'marina':
                    return False
                elif factor == 'blip':
                    return None

                # Intenta buscar la variable
                try:
                    return env.get_variable(factor)
                except RuntimeError:
                    # Si no es una variable, es un literal de cadena
                    return factor

            # Números y otros valores
            return factor

        # Si es una expresión entre paréntesis, evaluarla
        return self._evaluate(node[1], env)