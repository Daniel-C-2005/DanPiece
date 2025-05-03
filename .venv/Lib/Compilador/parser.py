"""
Analizador Sintáctico para el lenguaje DanCode con temática de One Piece
Utiliza PLY (Python Yacc) para reconocer la estructura sintáctica del lenguaje
"""

import ply.yacc as yacc
from lexer import tokens, agregar_simbolo, tabla_simbolos, hay_errores_lexicos

# Tabla de errores sintácticos
tabla_errores_sintacticos = []

# Árbol de derivación
arbol_derivacion = None

"""
Gramática BNF para el lenguaje DanCode con temática de One Piece:

programa : declaraciones
        | epsilon

declaraciones : declaraciones declaracion
              | declaracion

declaracion : declaracion_variable
            | declaracion_funcion
            | sentencia

declaracion_variable : tipo IDENTIFICADOR PUNTO_COMA
                     | tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA

tipo : TIPO_ENTERO        # akuma
     | TIPO_DECIMAL       # berry
     | TIPO_CADENA        # vivre_card
     | TIPO_BOOLEANO      # haki

declaracion_funcion : FUNCION IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque
                    # tecnica

parametros : lista_parametros
           | epsilon

lista_parametros : lista_parametros COMA parametro
                 | parametro

parametro : tipo IDENTIFICADOR

bloque : LLAVE_IZQ sentencias LLAVE_DER

sentencias : sentencias sentencia
           | sentencia
           | epsilon

sentencia : asignacion PUNTO_COMA
          | llamada_funcion PUNTO_COMA
          | sentencia_si
          | sentencia_mientras
          | sentencia_para
          | sentencia_retorno PUNTO_COMA
          | sentencia_imprimir PUNTO_COMA
          | sentencia_leer PUNTO_COMA

asignacion : IDENTIFICADOR ASIGNACION expresion

llamada_funcion : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER

argumentos : lista_argumentos
           | epsilon

lista_argumentos : lista_argumentos COMA expresion
                 | expresion

sentencia_si : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque
             | SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque SINO bloque
             # si_nakama, traidor

sentencia_mientras : MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque
                   # log_pose

sentencia_para : PARA PARENTESIS_IZQ asignacion PUNTO_COMA expresion PUNTO_COMA asignacion PARENTESIS_DER bloque
               # ir_hacia

sentencia_retorno : RETORNAR expresion
                  | RETORNAR
                  # zarpar

sentencia_imprimir : IMPRIMIR PARENTESIS_IZQ expresion PARENTESIS_DER
                   # proclamar

sentencia_leer : LEER PARENTESIS_IZQ IDENTIFICADOR PARENTESIS_DER
               # susurrar

expresion : expresion_logica

expresion_logica : expresion_relacional
                 | expresion_logica IGUAL expresion_relacional
                 | expresion_logica DIFERENTE expresion_relacional

expresion_relacional : expresion_aritmetica
                     | expresion_relacional MENOR expresion_aritmetica
                     | expresion_relacional MAYOR expresion_aritmetica
                     | expresion_relacional MENOR_IGUAL expresion_aritmetica
                     | expresion_relacional MAYOR_IGUAL expresion_aritmetica

expresion_aritmetica : termino
                     | expresion_aritmetica SUMA termino
                     | expresion_aritmetica RESTA termino

termino : factor
        | termino MULTIPLICACION factor
        | termino DIVISION factor

factor : IDENTIFICADOR
       | NUMERO_ENTERO
       | NUMERO_DECIMAL
       | CADENA_TEXTO
       | BOOLEANO_VERDADERO  # conquista
       | BOOLEANO_FALSO      # marina
       | NULO                # blip
       | PARENTESIS_IZQ expresion PARENTESIS_DER
       | llamada_funcion
"""

# Definir precedencias y asociatividad
precedence = (
    ('left', 'IGUAL', 'DIFERENTE'),
    ('left', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
)


# Reglas de la gramática
def p_programa(p):
    '''programa : declaraciones'''
    p[0] = ('programa', p[1])
    global arbol_derivacion
    arbol_derivacion = p[0]


def p_programa_vacio(p):
    '''programa : '''
    p[0] = ('programa', None)
    global arbol_derivacion
    arbol_derivacion = p[0]


def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                    | declaracion'''
    if len(p) == 3:
        if p[1] is None:
            p[0] = [p[2]]
        else:
            p[0] = p[1] + [p[2]] if isinstance(p[1], list) else [p[1], p[2]]
    else:
        p[0] = [p[1]]


def p_declaracion(p):
    '''declaracion : declaracion_variable
                  | declaracion_funcion
                  | sentencia'''
    p[0] = p[1]


def p_declaracion_variable(p):
    '''declaracion_variable : tipo IDENTIFICADOR PUNTO_COMA
                         | tipo IDENTIFICADOR ASIGNACION expresion PUNTO_COMA'''
    if len(p) == 4:
        p[0] = ('declaracion_variable', p[1], p[2], None)
        agregar_simbolo(p[2], p[1], None, p.lineno(2), 'global')
    else:
        p[0] = ('declaracion_variable', p[1], p[2], p[4])
        agregar_simbolo(p[2], p[1], p[4], p.lineno(2), 'global')


def p_tipo(p):
    '''tipo : TIPO_ENTERO
           | TIPO_DECIMAL
           | TIPO_CADENA
           | TIPO_BOOLEANO'''
    p[0] = p[1]


def p_declaracion_funcion(p):
    '''declaracion_funcion : FUNCION IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER bloque'''
    p[0] = ('declaracion_funcion', p[2], p[4], p[6])
    agregar_simbolo(p[2], 'tecnica', None, p.lineno(2), 'global')


def p_parametros(p):
    '''parametros : lista_parametros
                 | '''
    p[0] = p[1] if len(p) > 1 else []


def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA parametro
                       | parametro'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]] if isinstance(p[1], list) else [p[1], p[3]]
    else:
        p[0] = [p[1]]


def p_parametro(p):
    '''parametro : tipo IDENTIFICADOR'''
    p[0] = ('parametro', p[1], p[2])
    agregar_simbolo(p[2], p[1], None, p.lineno(2), f'param_{p[2]}')


def p_bloque(p):
    '''bloque : LLAVE_IZQ sentencias LLAVE_DER'''
    p[0] = ('bloque', p[2])


def p_sentencias(p):
    '''sentencias : sentencias sentencia
                 | sentencia
                 | '''
    if len(p) == 3:
        if p[1] is None:
            p[0] = [p[2]]
        else:
            p[0] = p[1] + [p[2]] if isinstance(p[1], list) else [p[1], p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_sentencia(p):
    '''sentencia : asignacion PUNTO_COMA
                | llamada_funcion PUNTO_COMA
                | sentencia_si
                | sentencia_mientras
                | sentencia_para
                | sentencia_retorno PUNTO_COMA
                | sentencia_imprimir PUNTO_COMA
                | sentencia_leer PUNTO_COMA'''
    p[0] = p[1]


def p_asignacion(p):
    '''asignacion : IDENTIFICADOR ASIGNACION expresion'''
    p[0] = ('asignacion', p[1], p[3])
    # Actualiza valor en tabla de símbolos si existe
    for simbolo in tabla_simbolos:
        if simbolo['nombre'] == p[1]:
            simbolo['valor'] = p[3]
            break


def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER'''
    p[0] = ('llamada_funcion', p[1], p[3])


def p_argumentos(p):
    '''argumentos : lista_argumentos
                 | '''
    p[0] = p[1] if len(p) > 1 else []


def p_lista_argumentos(p):
    '''lista_argumentos : lista_argumentos COMA expresion
                       | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]] if isinstance(p[1], list) else [p[1], p[3]]
    else:
        p[0] = [p[1]]


def p_sentencia_si(p):
    '''sentencia_si : SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque
                   | SI PARENTESIS_IZQ expresion PARENTESIS_DER bloque SINO bloque'''
    if len(p) == 6:
        p[0] = ('sentencia_si', p[3], p[5], None)
    else:
        p[0] = ('sentencia_si', p[3], p[5], p[7])


def p_sentencia_mientras(p):
    '''sentencia_mientras : MIENTRAS PARENTESIS_IZQ expresion PARENTESIS_DER bloque'''
    p[0] = ('sentencia_mientras', p[3], p[5])


def p_sentencia_para(p):
    '''sentencia_para : PARA PARENTESIS_IZQ asignacion PUNTO_COMA expresion PUNTO_COMA asignacion PARENTESIS_DER bloque'''
    p[0] = ('sentencia_para', p[3], p[5], p[7], p[9])


def p_sentencia_retorno(p):
    '''sentencia_retorno : RETORNAR expresion
                        | RETORNAR'''
    if len(p) == 3:
        p[0] = ('sentencia_retorno', p[2])
    else:
        p[0] = ('sentencia_retorno', None)


def p_sentencia_imprimir(p):
    '''sentencia_imprimir : IMPRIMIR PARENTESIS_IZQ expresion PARENTESIS_DER'''
    p[0] = ('sentencia_imprimir', p[3])


def p_sentencia_leer(p):
    '''sentencia_leer : LEER PARENTESIS_IZQ IDENTIFICADOR PARENTESIS_DER'''
    p[0] = ('sentencia_leer', p[3])


def p_expresion(p):
    '''expresion : expresion_logica'''
    p[0] = p[1]


def p_expresion_logica(p):
    '''expresion_logica : expresion_relacional
                       | expresion_logica IGUAL expresion_relacional
                       | expresion_logica DIFERENTE expresion_relacional'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expresion_logica', p[1], p[2], p[3])


def p_expresion_relacional(p):
    '''expresion_relacional : expresion_aritmetica
                           | expresion_relacional MENOR expresion_aritmetica
                           | expresion_relacional MAYOR expresion_aritmetica
                           | expresion_relacional MENOR_IGUAL expresion_aritmetica
                           | expresion_relacional MAYOR_IGUAL expresion_aritmetica'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expresion_relacional', p[1], p[2], p[3])


def p_expresion_aritmetica(p):
    '''expresion_aritmetica : termino
                           | expresion_aritmetica SUMA termino
                           | expresion_aritmetica RESTA termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expresion_aritmetica', p[1], p[2], p[3])


def p_termino(p):
    '''termino : factor
               | termino MULTIPLICACION factor
               | termino DIVISION factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('termino', p[1], p[2], p[3])


def p_factor(p):
    '''factor : IDENTIFICADOR
              | NUMERO_ENTERO
              | NUMERO_DECIMAL
              | CADENA_TEXTO
              | BOOLEANO_VERDADERO
              | BOOLEANO_FALSO
              | NULO
              | PARENTESIS_IZQ expresion PARENTESIS_DER
              | llamada_funcion'''
    if len(p) == 2:
        if isinstance(p[1], str) and p[1] in ['conquista', 'marina', 'blip']:
            p[0] = ('factor', p[1])
        else:
            p[0] = ('factor', p[1])
    else:
        p[0] = p[2]  # Para expresiones entre paréntesis


# Método para manejar errores sintácticos
# Método mejorado para manejar errores sintácticos
def p_error(p):
    global parser
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (línea {p.lineno})"
        token_esperado = determinar_token_esperado(p)
        registrar_error_sintactico(p.value, p.lineno, token_esperado, mensaje)
        print(f"\n✖️ ERROR SINTÁCTICO: {mensaje}")
        print(f"   Token esperado: {token_esperado}")

        # Intentamos recuperarnos del error
        parser.errok()

        # Método de recuperación: saltar hasta el siguiente punto y coma
        tok = None
        while True:
            tok = parser.token()
            if not tok or tok.type == 'PUNTO_COMA':
                break
            print(f"   ⚓ Saltando token: {tok.value}")
            parser.errok()
    else:
        mensaje = "Error de sintaxis al final del archivo"
        registrar_error_sintactico("EOF", "EOF", None, mensaje)
        print(f"\n✖️ ERROR SINTÁCTICO: {mensaje}")


# Función para determinar el token esperado en caso de error
def determinar_token_esperado(p):
    # Lógica simple para determinar qué token podría esperarse
    # Esto es una simplificación, en un compilador real sería más complejo
    if p.type == 'IDENTIFICADOR':
        return "Posiblemente una asignación '=' o una llamada a función '('"
    elif p.type == 'PARENTESIS_IZQ':
        return "Una expresión o ')'"
    elif p.type == 'LLAVE_IZQ':
        return "Una declaración, sentencia o '}'"
    else:
        return "Indeterminado"


# Función para registrar errores sintácticos
def registrar_error_sintactico(token, linea, token_esperado, mensaje):
    tabla_errores_sintacticos.append({
        'token': token,
        'linea': linea,
        'token_esperado': token_esperado,
        'mensaje': mensaje,
        'recuperacion': "Salto hasta ';' o token de sincronización"
    })


# Función para imprimir la tabla de errores sintácticos
def imprimir_errores_sintacticos():
    print("\n=== ERRORES SINTÁCTICOS ===")
    if not tabla_errores_sintacticos:
        print("No se encontraron errores sintácticos.")
        return

    print(f"{'TOKEN':<15} {'LÍNEA':<8} {'TOKEN ESPERADO':<25} {'MENSAJE':<30} {'RECUPERACIÓN':<20}")
    print("-" * 100)
    for error in tabla_errores_sintacticos:
        print(
            f"{str(error['token']):<15} {str(error['linea']):<8} {str(error['token_esperado']):<25} {error['mensaje']:<30} {error['recuperacion']:<20}")


# Función para verificar si hay errores sintácticos
def hay_errores_sintacticos():
    return len(tabla_errores_sintacticos) > 0


# Función para imprimir el árbol de derivación de forma jerárquica
def imprimir_arbol(nodo, nivel=0):
    if nodo is None:
        return

    if isinstance(nodo, tuple):
        print('  ' * nivel + f"- {nodo[0]}")
        for hijo in nodo[1:]:
            imprimir_arbol(hijo, nivel + 1)
    elif isinstance(nodo, list):
        for item in nodo:
            imprimir_arbol(item, nivel)
    else:
        print('  ' * nivel + f"- {nodo}")


# Construir el parser
parser = yacc.yacc()


# Función para analizar una cadena de entrada
def analizar(data):
    global arbol_derivacion
    arbol_derivacion = None
    tabla_errores_sintacticos.clear()

    resultado = parser.parse(data)
    return resultado


# Función para obtener el árbol de derivación
def obtener_arbol_derivacion():
    if hay_errores_lexicos() or hay_errores_sintacticos():
        print("❌ No se puede generar el árbol de derivación porque el código contiene errores léxicos o sintácticos.")
        return None
    return arbol_derivacion


# Si este archivo se ejecuta directamente
if __name__ == "__main__":
    import sys
    from lexer import analizar as analizar_lexico, imprimir_tabla_simbolos, imprimir_errores_lexicos

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            data = file.read()

        # Análisis léxico
        tokens = analizar_lexico(data)
        imprimir_tabla_simbolos()
        imprimir_errores_lexicos()

        # Análisis sintáctico
        resultado = analizar(data)
        imprimir_errores_sintacticos()

        # Imprimir árbol de derivación si no hay errores
        arbol = obtener_arbol_derivacion()
        if arbol:
            print("\n=== ÁRBOL DE DERIVACIÓN ===")
            imprimir_arbol(arbol)
    else:
        print("Uso: python parser.py archivo.op")