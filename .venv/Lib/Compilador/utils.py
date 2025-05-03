"""
Utilidades para el compilador DanCode con temática de One Piece
Proporciona funciones auxiliares para diferentes fases del compilador
"""

import os
import sys
import json
import datetime

# Mapeo de palabras reservadas originales a temática One Piece
MAPEO_PALABRAS = {
    # Tipos de datos
    'entero': 'akuma',  # Como una fruta del diablo, otorga poder básico
    'decimal': 'berry',  # Valor monetario decimal
    'cadena': 'vivre_card',  # Cadena = texto = una carta que indica conexión
    'booleano': 'haki',  # Verdadero/falso = voluntad fuerte o no

    # Valores booleanos
    'verdadero': 'conquista',  # Haki del rey: verdadero
    'falso': 'marina',  # Oposición falsa (enemigo del prota)

    # Estructuras de control
    'si': 'si_nakama',  # Si una condición se cumple con un nakama
    'sino': 'traidor',  # Sino: alternativa negativa o traición
    'mientras': 'log_pose',  # Mientras se mantenga el rumbo (navegación)
    'para': 'ir_hacia',  # Para llegar a una meta

    # Funciones y retorno
    'funcion': 'tecnica',  # Técnicas especiales como "Gomu Gomu no..."
    'retornar': 'zarpar',  # Retornar a donde se llamó

    # Valores especiales y E/S
    'nulo': 'blip',  # Sin valor, como un blip del Den Den Mushi
    'imprimir': 'proclamar',  # Proclamar algo, como un anuncio o grito épico
    'leer': 'susurrar',  # Leer datos = recibir susurros del mar (información)
}

# Mapeo inverso para convertir de One Piece a original
MAPEO_INVERSO = {v: k for k, v in MAPEO_PALABRAS.items()}


class OnePieceUtils:
    @staticmethod
    def palabra_a_one_piece(palabra):
        """Convierte una palabra reservada estándar a su equivalente de One Piece"""
        return MAPEO_PALABRAS.get(palabra, palabra)

    @staticmethod
    def one_piece_a_palabra(palabra_op):
        """Convierte una palabra reservada de One Piece a su equivalente estándar"""
        return MAPEO_INVERSO.get(palabra_op, palabra_op)

    @staticmethod
    def convertir_codigo_a_one_piece(codigo):
        """Convierte código DanCode estándar a código con temática de One Piece"""
        for palabra, palabra_op in MAPEO_PALABRAS.items():
            # Reemplazar solo palabras completas
            codigo = codigo.replace(f" {palabra} ", f" {palabra_op} ")
            codigo = codigo.replace(f"\n{palabra} ", f"\n{palabra_op} ")
            codigo = codigo.replace(f"{palabra}\n", f"{palabra_op}\n")
            codigo = codigo.replace(f"{palabra};", f"{palabra_op};")
            # Para caso especial al inicio de archivo
            if codigo.startswith(f"{palabra} "):
                codigo = f"{palabra_op} " + codigo[len(palabra) + 1:]
        return codigo

    @staticmethod
    def convertir_codigo_a_estandar(codigo_op):
        """Convierte código DanCode con temática de One Piece a código estándar"""
        for palabra_op, palabra in MAPEO_INVERSO.items():
            # Reemplazar solo palabras completas
            codigo_op = codigo_op.replace(f" {palabra_op} ", f" {palabra} ")
            codigo_op = codigo_op.replace(f"\n{palabra_op} ", f"\n{palabra} ")
            codigo_op = codigo_op.replace(f"{palabra_op}\n", f"{palabra}\n")
            codigo_op = codigo_op.replace(f"{palabra_op};", f"{palabra};")
            # Para caso especial al inicio de archivo
            if codigo_op.startswith(f"{palabra_op} "):
                codigo_op = f"{palabra} " + codigo_op[len(palabra_op) + 1:]
        return codigo_op

    @staticmethod
    def imprimir_tabla_simbolos_one_piece(tabla_simbolos):
        """Imprime la tabla de símbolos con los tipos en formato One Piece"""
        print("\n=== TABLA DE SÍMBOLOS DEL GRAND LINE ===")
        print(f"{'NOMBRE':<15} {'TIPO':<12} {'VALOR':<10} {'LÍNEA':<8} {'ALCANCE':<10}")
        print("-" * 62)
        for simbolo in tabla_simbolos:
            tipo = simbolo['tipo']
            # Convertir el tipo si es una palabra reservada estándar
            if tipo in MAPEO_PALABRAS:
                tipo = MAPEO_PALABRAS[tipo]
            print(
                f"{str(simbolo['nombre']):<15} {str(tipo):<12} {str(simbolo['valor']):<10} {str(simbolo['linea']):<8} {simbolo['alcance']:<10}")

    @staticmethod
    def guardar_tabla_simbolos(tabla_simbolos, nombre_archivo):
        """Guarda la tabla de símbolos en un archivo JSON"""
        try:
            with open(nombre_archivo, 'w') as archivo:
                json.dump(tabla_simbolos, archivo, indent=4)
            print(f"✓ Tabla de símbolos guardada en {nombre_archivo}")
            return True
        except Exception as e:
            print(f"✗ Error al guardar la tabla de símbolos: {str(e)}")
            return False

    @staticmethod
    def cargar_tabla_simbolos(nombre_archivo):
        """Carga la tabla de símbolos desde un archivo JSON"""
        try:
            with open(nombre_archivo, 'r') as archivo:
                tabla = json.load(archivo)
            print(f"✓ Tabla de símbolos cargada desde {nombre_archivo}")
            return tabla
        except Exception as e:
            print(f"✗ Error al cargar la tabla de símbolos: {str(e)}")
            return []

    @staticmethod
    def imprimir_error_colorizado(tipo, mensaje, linea=None):
        """Imprime un mensaje de error formateado"""
        if linea:
            print(f"[ERROR {tipo}] Línea {linea}: {mensaje}")
        else:
            print(f"[ERROR {tipo}] {mensaje}")

    @staticmethod
    def imprimir_aviso_colorizado(mensaje):
        """Imprime un mensaje de aviso formateado"""
        print(f"[AVISO] {mensaje}")

    @staticmethod
    def imprimir_exito_colorizado(mensaje):
        """Imprime un mensaje de éxito formateado"""
        print(f"[ÉXITO] {mensaje}")

    @staticmethod
    def obtener_extension_one_piece(ruta_archivo):
        """Convierte un archivo .dan a .op o viceversa"""
        nombre, extension = os.path.splitext(ruta_archivo)
        if extension.lower() == '.dan':
            return nombre + '.op'
        elif extension.lower() == '.op':
            return nombre + '.dan'
        else:
            # Si no es ninguna de las extensiones esperadas, añade .op
            return ruta_archivo + '.op'

    @staticmethod
    def generar_banner_one_piece():
        """Genera un banner de texto para el compilador One Piece"""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   █▀▄ ▄▀█ █▄░█ █▀▀ █▀█ █▀▄ █▀▀   █▀█ █▄░█ █▀▀   █▀█ █ █▀▀ █▀▀ █▀▀  ║
║   █▄▀ █▀█ █░▀█ █▄▄ █▄█ █▄▀ ██▄   █▄█ █░▀█ ██▄   █▀▀ █ ██▄ █▄▄ ██▄  ║
║                                                                  ║
║              Compilador con temática del Grand Line              ║
║                 ¡Encuentra el One Piece del código!                ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return banner

    @staticmethod
    def verificar_requisitos_instalacion():
        """Verifica si todos los requisitos están instalados"""
        try:
            import ply.lex
            import ply.yacc
            return True
        except ImportError as e:
            print(f"✗ Error: Faltan dependencias para ejecutar el compilador.")
            print(f"Ejecuta: pip install ply")
            return False


# Función para crear reportes HTML
def crear_reporte_html(nombre_archivo, codigo, tokens, hay_errores_lex, hay_errores_sint, arbol, nombre_reporte,
                       resultados_html=None):
    """Crea un reporte HTML con la información del análisis y ejecución"""
    # Obtener nombre del archivo sin la ruta
    nombre_base = os.path.basename(nombre_archivo)

    # Contenido HTML con estilo pirata
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vivre Card: {nombre_base}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f2e9d8; /* Pergamino */
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            border-radius: 5px;
            position: relative;
            overflow: hidden;
        }}
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" opacity="0.05"><text x="10" y="40" font-family="Arial" font-size="30" transform="rotate(45 50,50)">ONE PIECE</text></svg>');
            pointer-events: none;
        }}
        h1, h2, h3 {{
            color: #c70039; /* Rojo One Piece */
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ffc107; /* Amarillo Sombrero de Paja */
        }}
        .status {{
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }}
        .success {{
            background-color: #4caf50;
            color: white;
        }}
        .error {{
            background-color: #f44336;
            color: white;
        }}
        pre {{
            background-color: #2c3e50; /* Azul marino */
            color: #ecf0f1; /* Blanco hueso */
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .token {{
            margin-bottom: 5px;
            padding: 5px;
            background-color: #e3f2fd;
            border-radius: 3px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #ffc107; /* Amarillo Sombrero de Paja */
            color: #333;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
            color: #777;
        }}
        .pirateFlag {{
            display: block;
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="black"/><circle cx="50" cy="50" r="30" fill="white" stroke="black" stroke-width="2"/><circle cx="50" cy="40" r="5" fill="black"/><path d="M30,65 Q50,85 70,65" stroke="black" stroke-width="2" fill="none"/></svg>');
            background-repeat: no-repeat;
            background-position: center;
        }}
        .results {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .output-line {{
            margin-bottom: 8px;
            padding: 5px;
            background-color: #f5f5f5;
            border-radius: 3px;
            border-left: 4px solid #c70039;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="pirateFlag"></div>
        <h1>Vivre Card (Reporte de Compilación)</h1>

        <h2>🗺️ Información del Mapa</h2>
        <table>
            <tr>
                <th>Nombre del Mapa</th>
                <td>{nombre_base}</td>
            </tr>
            <tr>
                <th>Fecha de Navegación</th>
                <td>{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td>
            </tr>
            <tr>
                <th>Tamaño del Mapa</th>
                <td>{len(codigo)} caracteres</td>
            </tr>
            <tr>
                <th>Líneas de Navegación</th>
                <td>{codigo.count(os.linesep) + 1}</td>
            </tr>
        </table>

        <h2>📜 Mapa del Tesoro (Código)</h2>
        <pre>{codigo}</pre>

        <h2>🧭 Estado de la Navegación</h2>
        <div class="status {'error' if hay_errores_lex or hay_errores_sint else 'success'}">
            {'❌ ¡NAVEGACIÓN FALLIDA! Se encontraron errores en el código.' if hay_errores_lex or hay_errores_sint else '✅ ¡NAVEGACIÓN EXITOSA! El código se compiló correctamente.'}
        </div>

        <h2>💰 Tesoros Encontrados (Tokens)</h2>
        <div style="max-height: 300px; overflow-y: auto;">
    """

    # Agregar tokens al reporte
    if tokens:
        for i, token in enumerate(tokens):
            tipo = token.type
            valor = token.value
            linea = token.lineno
            html += f"""
            <div class="token">
                <strong>Tesoro #{i + 1}:</strong> Tipo: <span style="color: #c70039;">{tipo}</span>, 
                Valor: <span style="color: #0077b6;">{valor}</span>, 
                Línea: {linea}
            </div>
            """
    else:
        html += "<p>No se encontraron tesoros (tokens) en el código.</p>"

    # Agregar sección para el árbol sintáctico si existe
    if arbol:
        html += """
        </div>

        <h2>🌳 Mapa del Tesoro (Árbol Sintáctico)</h2>
        <div style="max-height: 500px; overflow-y: auto; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
        """

        # Función para generar HTML del árbol
        def generar_html_arbol(nodo, nivel=0):
            if nodo is None:
                return ""

            html_nodo = ""
            indent = '&nbsp;&nbsp;' * nivel

            if isinstance(nodo, tuple):
                html_nodo += f"<div>{indent}📍 <strong>{nodo[0]}</strong></div>"
                for hijo in nodo[1:]:
                    html_nodo += generar_html_arbol(hijo, nivel + 1)
            elif isinstance(nodo, list):
                for item in nodo:
                    html_nodo += generar_html_arbol(item, nivel)
            else:
                html_nodo += f"<div>{indent}🔹 {nodo}</div>"

            return html_nodo

        html += generar_html_arbol(arbol)
        html += "</div>"

    # Agregar resultados de ejecución si existen y no hay errores
    if resultados_html and not hay_errores_lex and not hay_errores_sint:
        html += f"""
        <h2>🚀 Resultados de la Ejecución</h2>
        <div class="results">
            {resultados_html}
        </div>
        """

    # Cerrar el HTML
    html += """        
        <div class="footer">
            <p>Generado por DanCode: One Piece Edition • La búsqueda del One Piece del código continúa...</p>
        </div>
    </div>
</body>
</html>
    """

    # Guardar el reporte HTML
    with open(nombre_reporte, 'w', encoding='utf-8') as f:
        f.write(html)

    return nombre_reporte


# Función para realizar una conversión de código en la línea de comandos
def main():
    if len(sys.argv) < 3:
        print(f"Uso: python utils.py [--to-one-piece|--to-standard] archivo.dan")
        return

    modo = sys.argv[1]
    archivo = sys.argv[2]

    try:
        with open(archivo, 'r') as f:
            codigo = f.read()

        if modo == '--to-one-piece':
            resultado = OnePieceUtils.convertir_codigo_a_one_piece(codigo)
            extension = OnePieceUtils.obtener_extension_one_piece(archivo)
        elif modo == '--to-standard':
            resultado = OnePieceUtils.convertir_codigo_a_estandar(codigo)
            extension = OnePieceUtils.obtener_extension_one_piece(archivo)
        else:
            print(f"Modo no válido. Use --to-one-piece o --to-standard")
            return

        with open(extension, 'w') as f:
            f.write(resultado)

        print(f"✓ Archivo convertido y guardado como: {extension}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    # Mostrar el banner
    print(OnePieceUtils.generar_banner_one_piece())
    # Ejecutar la función principal
    main()