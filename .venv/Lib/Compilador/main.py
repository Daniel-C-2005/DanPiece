"""
Punto de entrada principal para el compilador DanCode con temática de One Piece
Ejecuta el analizador léxico y sintáctico sobre un archivo fuente
"""

import sys
import os
from lexer import analizar as analizar_lexico, imprimir_tabla_simbolos, imprimir_errores_lexicos, hay_errores_lexicos, \
    tabla_errores_lexicos
from parser import analizar as analizar_sintactico, imprimir_errores_sintacticos, hay_errores_sintacticos, \
    obtener_arbol_derivacion, imprimir_arbol, tabla_errores_sintacticos
from utils import OnePieceUtils, crear_reporte_html


def compilar_archivo(nombre_archivo):
    """Compila un archivo fuente de DanCode con temática One Piece"""
    print(f"🚀 Navegando hacia el mapa del tesoro: {nombre_archivo}")

    # Verificar que el archivo existe
    if not os.path.isfile(nombre_archivo):
        print(f"❌ Error: ¡No se encontró el mapa '{nombre_archivo}' en ninguna isla conocida!")
        return False

    # Leer el contenido del archivo
    try:
        with open(nombre_archivo, 'r') as file:
            codigo_fuente = file.read()
    except Exception as e:
        print(f"❌ Error al desenrollar el mapa: {str(e)}")
        return False

    # Análisis léxico
    print("\n🔍 Calibrando el Log Pose (Análisis léxico)...")
    tokens = analizar_lexico(codigo_fuente)
    print(f"✅ Cartografía léxica completada. Se encontraron {len(tokens)} tesoros (tokens).")

    # Imprimir tabla de símbolos con estilo One Piece
    OnePieceUtils.imprimir_tabla_simbolos_one_piece(tabla_simbolos)

    # Verificar si hay errores léxicos y mostrarlos
    print(f"\n📊 Verificando errores léxicos... encontrados: {len(tabla_errores_lexicos)}")
    if len(tabla_errores_lexicos) > 0:
        print("\n=== ERRORES LÉXICOS DEL GRAND LINE ===")
        imprimir_errores_lexicos()  # Imprimir errores léxicos

    # Análisis sintáctico
    print("\n🔍 Trazando la ruta del Grand Line (Análisis sintáctico)...")
    resultado = analizar_sintactico(codigo_fuente)
    print(f"✅ Ruta trazada correctamente.")

    # Verificar si hay errores sintácticos y mostrarlos
    print(f"\n📊 Verificando errores sintácticos... encontrados: {len(tabla_errores_sintacticos)}")
    if len(tabla_errores_sintacticos) > 0:
        print("\n=== ERRORES SINTÁCTICOS DEL GRAND LINE ===")
        imprimir_errores_sintacticos()  # Imprimir errores sintácticos

    # Generar árbol de derivación
    print("\n🌳 Dibujando el mapa del tesoro (Árbol de derivación)...")
    arbol = obtener_arbol_derivacion()

    print(f"¿Se obtuvo árbol de derivación? {'Sí' if arbol else 'No'}")

    if arbol:
        print("✅ ¡Mapa del tesoro completado con éxito!")
        print("\n=== MAPA DEL TESORO (ÁRBOL DE DERIVACIÓN) ===")
        imprimir_arbol(arbol)
    else:
        print("❌ ¡No se pudo trazar el mapa del tesoro! Hay piratas enemigos (errores) en el código.")

        # Si no hay árboles pero tampoco errores, esto es un problema interno
        if len(tabla_errores_lexicos) == 0 and len(tabla_errores_sintacticos) == 0:
            print("⚠️ ¡Esto es extraño! No se encontraron errores, pero tampoco se generó un árbol.")
            print("   Puede ser un problema en la implementación del parser o en el manejo de la gramática.")

    # Crear reporte HTML
    nombre_reporte = os.path.splitext(nombre_archivo)[0] + "_vivre_card.html"
    crear_reporte_html(
        nombre_archivo,
        codigo_fuente,
        tokens,
        hay_errores_lexicos(),
        hay_errores_sintacticos(),
        arbol,
        nombre_reporte
    )
    print(f"\n📄 Se ha creado una Vivre Card (reporte) en: {nombre_reporte}")

    # Abrir el reporte en el navegador (opcional)
    try:
        import webbrowser
        webbrowser.open(nombre_reporte)
    except Exception as e:
        print(f"No se pudo abrir la Vivre Card automáticamente: {str(e)}")

    # Verificar si la compilación fue exitosa
    if hay_errores_lexicos() or hay_errores_sintacticos():
        print("\n❌ ¡La tripulación ha fracasado! La navegación falló debido a errores.")
        return False
    else:
        print("\n✅ ¡GOMU GOMU NO COMPILATION! ¡Compilación exitosa!")
        return True


# Punto de entrada principal
if __name__ == "__main__":
    # Mostrar el banner de One Piece
    print(OnePieceUtils.generar_banner_one_piece())
    print("🔰 COMPILADOR DEL GRAND LINE v1.0 🔰")
    print("Un compilador de códigos piratas en Python con PLY (Python Lex-Yacc)")

    if len(sys.argv) > 1:
        # Compilar archivo especificado en la línea de comandos
        nombre_archivo = sys.argv[1]
        compilar_archivo(nombre_archivo)
    else:
        # Mostrar mensaje de uso si no se especifica un archivo
        print("\n⚠️ ¡Se necesita un mapa del tesoro para navegar!")
        print("\nUso: python main.py <archivo.op>")
        print("\nEjemplo: python main.py mapa_del_tesoro.op")