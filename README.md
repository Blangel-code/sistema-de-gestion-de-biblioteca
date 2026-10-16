# Sistema de gestión de biblioteca

Este proyecto es una aplicación de consola escrita en Python para gestionar una biblioteca. Permite registrar usuarios, registrar libros y llevar el control de los préstamos, incluyendo la fecha en la que se realizó cada préstamo. Actualmente es una apliación de Interfaz

<img width="1260" height="679" alt="proyecto-biblioteca-1" src="https://github.com/user-attachments/assets/bac06878-f969-4bbf-a6bf-f4b81d1e1310" />
<img width="1263" height="681" alt="proyecto-biblioteca-4" src="https://github.com/user-attachments/assets/5b94122f-b042-4d4b-a0c8-6d2949dac142" />
<img width="1265" height="682" alt="proyecto-biblioteca-3" src="https://github.com/user-attachments/assets/4b5fb473-7251-4a26-8cac-244a84b38921" />
<img width="1262" height="679" alt="proyecto-biblioteca-2" src="https://github.com/user-attachments/assets/812d4dfa-f8ab-4066-95fc-0ee72185492e" />


## Características

- Registro de usuarios con datos básicos (nombre, identificación y edad).
- Registro de libros (título, autor, ISBN, año y disponibilidad).
- Registro y seguimiento de préstamos con fecha de préstamo.
- Búsqueda y listado de usuarios y libros.
- Gestión básica de estado de disponibilidad de los libros.
- Creación de informes mediante PDF o archivos .csv.
- Estadísticas globales de libros y usuarios

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clonar el repositorio:

   git clone https://github.com/Blangel-code/sistema-de-gestion-de-biblioteca.git
   cd sistema-de-gestion-de-biblioteca

## Uso

Ejecuta el script principal desde la consola. "Sistema_de_Gestion_de_Biblioteca.py"
Para retroceder o salir de las opciones escribir "salir" o "0"

Sigue las indicaciones en pantalla para:

- Registrar usuarios
- Agregar libros
- Registrar préstamos
- Consultar listados
- Reportes sobre el uso de la app

## Estructura del proyecto

- README.md
- main.py  <- punto de entrada de la aplicación
- Querys.py
- Config.py
- views/*.py <- secciones de la interfaz gráfica
- componets/modals.py <- componentes modales para las interfaces graficas
- data/data.db
- data/exports/
- LICENSE.txt

Ajusta la estructura según los archivos reales del repositorio.

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con tu cambio: `git checkout -b feature/mi-cambio`
3. Realiza tus cambios y haz commit.
4. Envía un pull request describiendo los cambios realizados.

## Licencia

Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (c) 2026 Blangel-code

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 

## Contacto

Para dudas o sugerencias, abre un issue en el repositorio o contactatame.
