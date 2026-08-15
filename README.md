# Sistema de gestión de biblioteca

Este proyecto es una aplicación de consola escrita en Python para gestionar una biblioteca. Permite registrar usuarios, registrar libros y llevar el control de los préstamos, incluyendo la fecha en la que se realizó cada préstamo. Actualmente es una aplicación de línea de comandos; en el futuro se planea agregar una interfaz gráfica.

## Características

- Registro de usuarios con datos básicos (nombre, identificación, contacto).
- Registro de libros (título, autor, ISBN, año, disponibilidad).
- Registro y seguimiento de préstamos con fecha de préstamo y posible fecha de devolución.
- Búsqueda y listado de usuarios y libros.
- Gestión básica de estado de disponibilidad de los libros.

## Requisitos

- Python 3.8 o superior
- (Opcional) Virtualenv para aislar dependencias

## Instalación

1. Clonar el repositorio:

   git clone https://github.com/Blangel-code/sistema-de-gestion-de-biblioteca.git
   cd sistema-de-gestion-de-biblioteca

2. (Opcional) Crear y activar un entorno virtual:

   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate

3. Instalar dependencias (si existen):

   pip install -r requirements.txt

> Nota: Si el proyecto no contiene un archivo requirements.txt, es posible que no haya dependencias externas y bastará con tener Python instalado.

## Uso

Ejecuta el script principal desde la consola. Dependiendo del nombre del archivo principal, puede ser alguno de los siguientes ejemplos:

   python main.py
   # o
   python app.py

Sigue las indicaciones en pantalla para:

- Registrar usuarios
- Agregar libros
- Registrar préstamos
- Consultar listados y buscar por criterios

## Estructura del proyecto (ejemplo)

- README.md
- main.py / app.py  <- punto de entrada de la aplicación
- modules/ o src/   <- módulos con la lógica de la aplicación
- data/              <- archivos de datos (por ejemplo, JSON o CSV)
- requirements.txt

Ajusta la estructura según los archivos reales del repositorio.

## Buenas prácticas y mejoras propuestas

- Añadir persistencia con una base de datos (SQLite, PostgreSQL) en lugar de archivos planos.
- Implementar validaciones más robustas para datos de usuarios y libros.
- Añadir una interfaz gráfica (Tkinter, PyQt, web con Flask/Django) para mejorar la experiencia.
- Añadir pruebas unitarias y CI (GitHub Actions) para asegurar la calidad del código.

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con tu cambio: `git checkout -b feature/mi-cambio`
3. Realiza tus cambios y haz commit.
4. Envía un pull request describiendo los cambios realizados.

## Licencia

Indica aquí la licencia del proyecto (por ejemplo, MIT) o elimina esta sección si aún no has decidido una.

## Contacto

Para dudas o sugerencias, abre un issue en el repositorio o contacta al autor.
