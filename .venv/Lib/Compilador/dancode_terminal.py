"""
Terminal interactiva para el lenguaje DanCode con temática de One Piece.
Este script permite ejecutar código DanCode de diferentes maneras:
1. Desde un archivo
2. En modo interactivo (línea por línea)
3. En modo de entrada múltiple (bloque de código)
"""

import os
import sys
import tempfile
from lexer import analizar as analizar_lexico, imprimir_tabla_simbolos, imprimir_errores_lexicos, hay_errores_lexicos, \
    tabla_errores_lexicos, tabla_simbolos
from parser import analizar as analizar_sintactico, imprimir_errores_sintacticos, hay_errores_sintacticos, \
    obtener_arbol_derivacion, imprimir_arbol, tabla_errores_sintacticos
from utils import OnePieceUtils, crear_reporte_html
from interpreter import Interpreter


def limpiar_pantalla():
    """Limpia la pantalla de la terminal según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')


def ejecutar_codigo(codigo, nombre_archivo="codigo_temporal.op", mostrar_reporte=True):
    """Ejecuta el código DanCode con temática One Piece y muestra los resultados"""
    print("\n🔍 Navegando por el código del Grand Line...")

    # Análisis léxico
    tokens = analizar_lexico(codigo)
    print(f"✅ Cartografía léxica completada. Se encontraron {len(tokens)} tesoros (tokens).")

    # Mostrar tokens encontrados
    print("\n🏆 TESOROS ENCONTRADOS (TOKENS) 🏆")
    print(f"{'TIPO':<15} {'VALOR':<20} {'LÍNEA':<8}")
    print("-" * 45)
    for i, tok in enumerate(tokens[:10]):  # Mostrar primeros 10 tokens
        print(f"{tok.type:<15} {str(tok.value):<20} {tok.lineno:<8}")
    if len(tokens) > 10:
        print(f"... y {len(tokens) - 10} tesoros más")

    # Imprimir tabla de símbolos con estilo One Piece
    OnePieceUtils.imprimir_tabla_simbolos_one_piece(tabla_simbolos)

    # Verificar si hay errores léxicos y mostrarlos
    print(f"\n🔎 BÚSQUEDA DE PIRATAS LÉXICOS...")
    if hay_errores_lexicos():
        print("\n❌ ¡PIRATAS LÉXICOS ENCONTRADOS! ❌")
        print("\n=== ERRORES LÉXICOS DEL GRAND LINE ===")
        imprimir_errores_lexicos()  # Imprimir errores léxicos
    else:
        print("\n✅ ¡NO HAY PIRATAS LÉXICOS EN ESTAS AGUAS!")

    # Análisis sintáctico
    resultado = analizar_sintactico(codigo)
    print(f"\n🧭 Cartografía sintáctica en proceso...")

    # Verificar si hay errores sintácticos y mostrarlos
    print(f"\n🔎 BÚSQUEDA DE PIRATAS SINTÁCTICOS...")
    if hay_errores_sintacticos():
        print("\n❌ ¡PIRATAS SINTÁCTICOS ENCONTRADOS! ❌")
        print("\n=== ERRORES SINTÁCTICOS DEL GRAND LINE ===")
        imprimir_errores_sintacticos()  # Imprimir errores sintácticos
    else:
        print("\n✅ ¡NO HAY PIRATAS SINTÁCTICOS EN ESTAS AGUAS!")

    # Generar árbol de derivación
    print("\n🌳 Trazando el mapa del tesoro (árbol de derivación)...")
    arbol = obtener_arbol_derivacion()

    if arbol:
        print("\n✨ ¡MAPA DEL TESORO COMPLETO! ✨")
        print("\n=== MAPA DEL TESORO (ÁRBOL DE DERIVACIÓN) ===")
        imprimir_arbol(arbol)
    else:
        print("\n❌ ¡No se pudo trazar el mapa del tesoro!")
        if not hay_errores_lexicos() and not hay_errores_sintacticos():
            print("⚠️ ¡Extraño! No hay errores pero no se generó el árbol.")

    # Ejecutar el código si no hay errores
    resultados_html = None

    if not hay_errores_lexicos() and not hay_errores_sintacticos() and arbol:
        print("\n🚀 EJECUTANDO EL CÓDIGO DEL GRAND LINE...")
        interpreter = Interpreter()
        try:
            interpreter.interpret(arbol)

            # Obtener la salida
            output = interpreter.get_output()

            print("\n📊 RESULTADOS DE LA EJECUCIÓN:")
            if output:
                for i, line in enumerate(output, 1):
                    print(f"  {i}. {line}")
            else:
                print("  No se generó ninguna salida.")

            print("\n✅ ¡EJECUCIÓN EXITOSA! El código ha sido ejecutado correctamente.")

            # Preparar los resultados para el HTML
            resultados_html = ""
            if output:
                resultados_html += "<ul>"
                for line in output:
                    resultados_html += f"<li class='output-line'>{line}</li>"
                resultados_html += "</ul>"
            else:
                resultados_html += "<p>No se generó ninguna salida.</p>"

        except Exception as e:
            print(f"\n❌ ERROR DE EJECUCIÓN: {str(e)}")
            print("\n❌ ¡LA TRIPULACIÓN HA FRACASADO! La ejecución falló debido a errores.")
            resultados_html = f"<p class='error'>Error de ejecución: {str(e)}</p>"

    # Crear reporte HTML si se solicita
    if mostrar_reporte:
        nombre_reporte = os.path.splitext(nombre_archivo)[0] + "_vivre_card.html"
        crear_reporte_html(
            nombre_archivo,
            codigo,
            tokens,
            hay_errores_lexicos(),
            hay_errores_sintacticos(),
            arbol,
            nombre_reporte,
            resultados_html
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
        print("\n❌ ¡LA TRIPULACIÓN HA FRACASADO! La navegación falló debido a errores.")
        return False
    else:
        print("\n✅ ¡GOMU GOMU NO COMPILATION! ¡Compilación exitosa!")
        return True


def modo_archivo():
    """Ejecuta código DanCode desde un archivo"""
    while True:
        ruta_archivo = input("\nIngresa la ruta del mapa del tesoro (.op o .dan): ")
        if ruta_archivo.lower() == 'zarpar' or ruta_archivo.lower() == 'salir' or ruta_archivo.lower() == 'exit':
            return

        if not os.path.isfile(ruta_archivo):
            print(f"❌ Error: No se encontró el mapa '{ruta_archivo}' en ninguna isla conocida")
            continue

        # Leer el contenido del archivo
        try:
            with open(ruta_archivo, 'r') as file:
                codigo = file.read()
        except Exception as e:
            print(f"❌ Error al leer el mapa: {str(e)}")
            continue

        # Ejecutar el código
        ejecutar_codigo(codigo, ruta_archivo)

        # Preguntar si desea analizar otro archivo
        if input("\n¿Deseas navegar hacia otro mapa? (s/n): ").lower() != 's':
            return


def modo_interactivo():
    """Modo interactivo para ejecutar código DanCode línea por línea"""
    historial_codigo = []

    print("\n=== MODO INTERACTIVO DEL THOUSAND SUNNY ===")
    print("Escribe líneas de código del Grand Line. Escribe 'ejecutar' para analizar el código.")
    print("Escribe 'limpiar' para borrar el diario de navegación, o 'zarpar' para volver al menú principal.")

    while True:
        # Mostrar un prompt estilo One Piece
        linea = input("\n🏴‍☠️ >>> ")

        # Verificar comandos especiales
        if linea.lower() == 'zarpar' or linea.lower() == 'salir' or linea.lower() == 'exit':
            return
        elif linea.lower() == 'limpiar' or linea.lower() == 'clear':
            historial_codigo = []
            print("Log Pose reiniciado. Diario de navegación limpio.")
            continue
        elif linea.lower() == 'ejecutar' or linea.lower() == 'run':
            if not historial_codigo:
                print("¡El mapa está en blanco! No hay código para ejecutar.")
                continue

            # Ejecutar el código acumulado
            codigo_completo = '\n'.join(historial_codigo)

            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.op', delete=False, mode='w') as temp_file:
                temp_file.write(codigo_completo)
                nombre_temp = temp_file.name

            # Ejecutar el código
            ejecutar_codigo(codigo_completo, nombre_temp)

            # Eliminar el archivo temporal
            try:
                os.remove(nombre_temp)
            except:
                pass

            continue
        elif linea.lower() == 'mostrar' or linea.lower() == 'show':
            if not historial_codigo:
                print("El diario de navegación está vacío. No hay código para mostrar.")
            else:
                print("\n=== DIARIO DE NAVEGACIÓN ACTUAL ===")
                for i, linea_codigo in enumerate(historial_codigo, 1):
                    print(f"{i}: {linea_codigo}")
            continue

        # Agregar la línea al historial
        historial_codigo.append(linea)


def modo_bloque():
    """Modo de entrada múltiple para escribir bloques de código DanCode"""
    print("\n=== MODO ISLA WHOLE CAKE (BLOQUE DE CÓDIGO) ===")
    print("Escribe tu código del Grand Line. Termina con una línea que contenga solo '---'.")
    print("Para cancelar, escribe 'zarpar' en una línea por sí sola.")

    lineas_codigo = []

    while True:
        linea = input("")

        if linea == '---':
            break
        elif linea.lower() == 'zarpar' or linea.lower() == 'salir' or linea.lower() == 'exit':
            return

        lineas_codigo.append(linea)

    if not lineas_codigo:
        print("El mapa está en blanco. No se ingresó código.")
        return

    # Unir las líneas en un solo bloque de código
    codigo_completo = '\n'.join(lineas_codigo)

    # Imprimir el código completo para verificación
    print("\n=== CÓDIGO A ANALIZAR ===")
    print(codigo_completo)
    print("=========================")

    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.op', delete=False, mode='w') as temp_file:
        temp_file.write(codigo_completo)
        nombre_temp = temp_file.name

    print(f"Archivo temporal creado: {nombre_temp}")

    # Ejecutar el código
    ejecutar_codigo(codigo_completo, nombre_temp)

    # Eliminar el archivo temporal
    try:
        os.remove(nombre_temp)
    except Exception as e:
        print(f"No se pudo eliminar el archivo temporal: {str(e)}")


def menu_principal():
    """Menú principal de la terminal DanCode con tema de One Piece"""
    while True:
        limpiar_pantalla()
        # Mostrar el banner de One Piece
        print(OnePieceUtils.generar_banner_one_piece())
        print("🔰 TERMINAL DEL GRAND LINE 🔰")
        print("================================")
        print("1. Cargar y ejecutar un mapa del tesoro (.op)")
        print("2. Modo Den Den Mushi (interactivo)")
        print("3. Modo Isla Whole Cake (bloque de código)")
        print("4. Zarpar (Salir)")
        print("================================")

        opcion = input("Selecciona una opción, Nakama (1-4): ")

        if opcion == '1':
            modo_archivo()
        elif opcion == '2':
            modo_interactivo()
        elif opcion == '3':
            modo_bloque()
        elif opcion == '4':
            print("\n¡Hasta que nos volvamos a encontrar en el Grand Line! 👋")
            break
        else:
            input("¡Te has desviado de la ruta! Opción no válida. Presiona Enter para continuar...")


# Punto de entrada principal
if __name__ == "__main__":
    # Si se proporciona un argumento, asumir que es un archivo
    if len(sys.argv) > 1:
        ruta_archivo = sys.argv[1]
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, 'r') as file:
                    codigo = file.read()
                ejecutar_codigo(codigo, ruta_archivo)
            except Exception as e:
                print(f"❌ Error al navegar por el mapa: {str(e)}")
        else:
            print(f"❌ Error: No se encontró el mapa '{ruta_archivo}' en ninguna isla conocida")
    else:
        # Mostrar el menú principal
        menu_principal()