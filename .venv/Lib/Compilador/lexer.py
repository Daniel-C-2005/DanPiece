"""
Analizador Léxico para el lenguaje DanCode con temática de One Piece
Utiliza PLY (Python Lex-Yacc) para reconocer los tokens del lenguaje
"""

import ply.lex as lex
import sys

# Lista de palabras reservadas con temática de One Piece
palabras_reservadas = {
    'akuma': 'TIPO_ENTERO',         # entero
    'berry': 'TIPO_DECIMAL',        # decimal
    'vivre_card': 'TIPO_CADENA',    # cadena
    'haki': 'TIPO_BOOLEANO',        # booleano
    'conquista': 'BOOLEANO_VERDADERO', # verdadero
    'marina': 'BOOLEANO_FALSO',     # falso
    'si_nakama': 'SI',              # si
    'traidor': 'SINO',              # sino
    'log_pose': 'MIENTRAS',         # mientras
    'ir_hacia': 'PARA',             # para
    'tecnica': 'FUNCION',           # funcion
    'zarpar': 'RETORNAR',           # retornar
    'blip': 'NULO',                 # nulo
    'proclamar': 'IMPRIMIR',        # imprimir
    'susurrar': 'LEER'              # leer
}

# Lista de tokens
tokens = [
             'IDENTIFICADOR',
             'NUMERO_ENTERO',
             'NUMERO_DECIMAL',
             'CADENA_TEXTO',
             'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION',
             'PARENTESIS_IZQ', 'PARENTESIS_DER',
             'LLAVE_IZQ', 'LLAVE_DER',
             'PUNTO_COMA', 'COMA',
             'ASIGNACION',
             'IGUAL', 'DIFERENTE',
             'MENOR', 'MAYOR',
             'MENOR_IGUAL', 'MAYOR_IGUAL',
         ] + list(palabras_reservadas.values())

# Tabla de símbolos
tabla_simbolos = []

# Tabla de errores léxicos
tabla_errores_lexicos = []

# Comentarios de una línea: // comentario
def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass

# Comentarios multilínea: /* comentario */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_ASIGNACION = r'='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_PUNTO_COMA = r';'
t_COMA = r','

t_DIVISION = r'/'  # ← DEBE IR DESPUÉS de los comentarios
# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'


# Regla para seguimiento de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Regla para reconocer números decimales
def t_NUMERO_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    agregar_simbolo(t.value, 'berry', t.value, t.lexer.lineno, 'global')
    return t


# Regla para reconocer números enteros
def t_NUMERO_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    agregar_simbolo(t.value, 'akuma', t.value, t.lexer.lineno, 'global')
    return t


# Regla para reconocer cadenas de texto
def t_CADENA_TEXTO(t):
    r'"([^"\\]|\\["\\])*"'
    t.value = t.value[1:-1]  # Quitar las comillas
    agregar_simbolo(t.value, 'vivre_card', t.value, t.lexer.lineno, 'global')
    return t


# Regla para reconocer identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica si es una palabra reservada
    t.type = palabras_reservadas.get(t.value, 'IDENTIFICADOR')
    if t.type == 'IDENTIFICADOR':
        agregar_simbolo(t.value, None, None, t.lexer.lineno, 'global')
    return t


# Manejo de errores léxicos
# Manejo de errores léxicos mejorado
def t_error(t):
    mensaje = f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}"
    registrar_error_lexico(t.value[0], t.lexer.lineno, mensaje)
    print(f"\n❌ ERROR LÉXICO: {mensaje}")
    t.lexer.skip(1)

# Función para agregar símbolos a la tabla de símbolos
def agregar_simbolo(nombre, tipo, valor, linea, alcance):
    # Verifica si el símbolo ya existe en el mismo alcance
    for simbolo in tabla_simbolos:
        if simbolo['nombre'] == nombre and simbolo['alcance'] == alcance:
            # Actualizar el valor si ya existe
            simbolo['tipo'] = tipo if tipo else simbolo['tipo']
            simbolo['valor'] = valor if valor is not None else simbolo['valor']
            return

    # Si no existe, agregar nuevo símbolo
    tabla_simbolos.append({
        'nombre': nombre,
        'tipo': tipo,
        'valor': valor,
        'linea': linea,
        'alcance': alcance
    })


# Función para registrar errores léxicos
def registrar_error_lexico(token, linea, mensaje):
    tabla_errores_lexicos.append({
        'token': token,
        'linea': linea,
        'mensaje': mensaje
    })


# Construir el lexer
lexer = lex.lex()


# Función para analizar una cadena de entrada
def analizar(data):
    lexer.input(data)
    tokens_encontrados = []

    # Vaciar tablas para nuevo análisis
    tabla_simbolos.clear()
    tabla_errores_lexicos.clear()

    # Tokenizar la entrada
    for tok in lexer:
        tokens_encontrados.append(tok)

    return tokens_encontrados


# Función para imprimir la tabla de símbolos
def imprimir_tabla_simbolos():
    print("\n=== TABLA DE SÍMBOLOS ===")
    print(f"{'NOMBRE':<15} {'TIPO':<12} {'VALOR':<10} {'LÍNEA':<8} {'ALCANCE':<10}")
    print("-" * 62)
    for simbolo in tabla_simbolos:
        print(
            f"{str(simbolo['nombre']):<15} {str(simbolo['tipo']):<12} {str(simbolo['valor']):<10} {str(simbolo['linea']):<8} {simbolo['alcance']:<10}")


# Función para imprimir la tabla de errores léxicos
def imprimir_errores_lexicos():
    print("\n=== ERRORES LÉXICOS ===")
    if not tabla_errores_lexicos:
        print("No se encontraron errores léxicos.")
        return

    print(f"{'TOKEN':<10} {'LÍNEA':<8} {'MENSAJE':<50}")
    print("-" * 70)
    for error in tabla_errores_lexicos:
        print(f"{error['token']:<10} {str(error['linea']):<8} {error['mensaje']:<50}")


# Función para verificar si hay errores léxicos
def hay_errores_lexicos():
    return len(tabla_errores_lexicos) > 0


# Si este archivo se ejecuta directamente
if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            data = file.read()
        tokens = analizar(data)
        print("Tokens encontrados:")
        for tok in tokens:
            print(tok)
        imprimir_tabla_simbolos()
        imprimir_errores_lexicos()
    else:
        print("Uso: python lexer.py archivo.op")