# DanCode: One Piece Edition

![One Piece Banner](https://www.xtrafondos.com/wallpapers/personajes-de-one-piece-10552.jpg)

## 🏴‍☠️ Navegando por el Grand Line del Código

DanCode: One Piece Edition es un compilador e intérprete para un lenguaje de programación simple con temática del popular anime y manga One Piece. Este proyecto implementa un analizador léxico, un analizador sintáctico y un intérprete que permite ejecutar programas escritos en este lenguaje temático.

## 📜 Características Principales

- **Analizador Léxico**: Reconoce tokens y genera la tabla de símbolos
- **Analizador Sintáctico**: Verifica la estructura del código y genera el árbol de derivación
- **Intérprete**: Ejecuta el código analizado y muestra los resultados
- **Terminal Interactiva**: Interfaz para escribir y ejecutar código de diferentes formas
- **Reportes HTML**: Genera "Vivre Cards" (reportes) con información detallada
- **Temática One Piece**: Palabras reservadas y mensajes relacionados con el universo pirata

## 🗿 Palabras Reservadas con Temática de One Piece

| Palabra Original | Palabra One Piece | Explicación |
|-----------------|-------------------|-------------|
| entero          | akuma             | Como una fruta del diablo, otorga poder básico |
| decimal         | berry             | Valor monetario decimal |
| cadena          | vivre_card        | Cadena = texto = una carta que indica conexión |
| booleano        | haki              | Verdadero/falso = voluntad fuerte o no |
| verdadero       | conquista         | Haki del rey: verdadero |
| falso           | marina            | Oposición falsa (enemigo del protagonista) |
| si              | si_nakama         | Si una condición se cumple con un nakama |
| sino            | traidor           | Sino: alternativa negativa o traición |
| mientras        | log_pose          | Mientras se mantenga el rumbo (navegación) |
| para            | ir_hacia          | Para llegar a una meta |
| funcion         | tecnica           | Técnicas especiales como "Gomu Gomu no..." |
| retornar        | zarpar            | Retornar a donde se llamó |
| nulo            | blip              | Sin valor, como un blip del Den Den Mushi |
| imprimir        | proclamar         | Proclamar algo, como un anuncio o grito épico |
| leer            | susurrar          | Leer datos = recibir susurros del mar (información) |

## 🧩 Estructura del Proyecto

El proyecto está compuesto por los siguientes archivos principales:

- **lexer.py**: Analizador léxico utilizando PLY (Python Lex-Yacc)
- **parser.py**: Analizador sintáctico que genera el árbol de derivación
- **utils.py**: Utilidades y funciones auxiliares
- **interpreter.py**: Intérprete que ejecuta el código analizado
- **dancode_terminal.py**: Terminal interactiva para el usuario
- **main.py**: Punto de entrada principal para el compilador

## 🚀 Requisitos

- Python 3.6 o superior
- Biblioteca PLY (Python Lex-Yacc)

## 📦 Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tuusuario/dancode-one-piece.git
   cd dancode-one-piece
   ```

2. Instala las dependencias:
   ```
   pip install ply
   ```

## 🎮 Uso

### Terminal Interactiva

```
python dancode_terminal.py
```

La terminal ofrece tres modos de operación:
1. **Cargar y ejecutar un archivo**: Para ejecutar código desde un archivo .op
2. **Modo Den Den Mushi (interactivo)**: Para escribir código línea por línea
3. **Modo Isla Whole Cake (bloque)**: Para escribir bloques de código

### Compilación Directa

```
python main.py archivo.op
```

### Convertir Código

Para convertir entre código estándar y código con temática One Piece:

```
python utils.py --to-one-piece archivo.dan   # Convierte a temática One Piece
python utils.py --to-standard archivo.op     # Convierte a sintaxis estándar
```

## 📝 Ejemplos de Código

### Ejemplo Simple

```
// Declaración de variables
akuma tesoro = 100;
berry recompensa = 50.5;
vivre_card capitan = "Luffy";

// Impresión de valores
proclamar("El tesoro vale: " + tesoro);
proclamar("La recompensa es: " + recompensa);
proclamar("El capitán es: " + capitan);
```

### Función y Condicional

```
// Función para calcular el nivel de poder
tecnica poder_pirata(akuma base, berry multiplicador) {
    zarpar base * multiplicador;
}

// Uso de condicionales
akuma nivel = poder_pirata(100, 1.5);
si_nakama (nivel > 100) {
    proclamar("¡Es un pirata poderoso!");
} traidor {
    proclamar("Necesita más entrenamiento...");
}
```

### Bucle

```
// Bucle mientras (log_pose)
akuma contador = 1;
log_pose (contador <= 5) {
    proclamar("Día " + contador + " en el Grand Line");
    contador = contador + 1;
}
```

## 🎓 ¿Cómo Funciona?

1. **Análisis Léxico**: El código fuente se analiza token por token.
2. **Análisis Sintáctico**: Se verifica la estructura gramatical y se genera el árbol de derivación.
3. **Ejecución**: El intérprete recorre el árbol de derivación y ejecuta las instrucciones.
4. **Generación de Reportes**: Se crea un informe HTML con los resultados de la compilación y ejecución.

## 🌟 Características del Lenguaje

- Tipos de datos: entero (akuma), decimal (berry), cadena (vivre_card), booleano (haki)
- Estructuras de control: if-else (si_nakama-traidor), while (log_pose), for (ir_hacia)
- Funciones: definición (tecnica) y retorno (zarpar)
- Operaciones: aritméticas, lógicas, relacionales
- Salida estándar: proclamar()

## 📈 Posibles Mejoras Futuras

- Agregar más funciones predefinidas
- Implementar estructuras de datos avanzadas (arrays, diccionarios)
- Desarrollar un entorno de desarrollo integrado (IDE)
- Generar código objeto o bytecode para ejecución más eficiente
- Implementar manejo de excepciones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:
1. Haz un fork del repositorio
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autor

- Daniel - *Desarrollo inicial*

---

¡Embárcate en la aventura de programar con temática pirata y encuentra el One Piece del código!
