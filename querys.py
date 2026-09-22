"""Archivo Donde Estarán Ubicadas Las Querys Para Poder Hacer Consultas En SQLite"""

import sqlite3
from pathlib import Path
from typing import TypedDict

PATH_DB =  Path(__file__).resolve().parent / "data" / "data.db"
"""Ruta De La Base De Datos SQLite"""
PATH_DB.parent.mkdir(parents=True,exist_ok=True)

QUERY_SEARCH_BOOKS = "SELECT bookID,isbn,title,autor,CASE WHEN stock_available = 0 THEN 'Inactivo' ELSE 'Activo' END AS status,category,publisher,year,pages,description FROM Books WHERE (status = ? OR ? IS NULL) AND (category = ? OR ? IS NULL) AND (title LIKE ? OR isbn LIKE ? OR autor LIKE ?)"
"""Query Para Seleccionar la ID, Isbn, Título, Autor, Estado (Activo|Inactivo), Categoría, Editorial, Anio y Paginas De Todos Los Libros"""

QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS "Books" (
	"bookID"	INTEGER,
	"isbn"	TEXT NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	"autor"	TEXT NOT NULL,
	"category"	TEXT NOT NULL,
	"publisher"	TEXT NOT NULL,
	"year"	INTEGER NOT NULL,
	"pages"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL,
	"stock_total"	INTEGER DEFAULT 1,
	"stock_available"	INTEGER DEFAULT 1,
	PRIMARY KEY("bookID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Users" (
	"userID"	INTEGER,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"phone"	TEXT,
    "id_card"	INTEGER NOT NULL,
	"state"	TEXT NOT NULL DEFAULT 'Activo',
    "libros
	"registration_date"	DATE DEFAULT CURRENT_DATE,
	PRIMARY KEY("userID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Orders" (
	"orderID"	INTEGER,
	"userID"	INTEGER NOT NULL,
	"bookID"	INTEGER NOT NULL,
    "status"	TEXT NOT NULL DEFAULT 'Activo',
	"date_lending"	DATE DEFAULT CURRENT_DATE,
	"date_return"	DATE NOT NULL,
	PRIMARY KEY("orderID" AUTOINCREMENT),
    FOREIGN KEY("bookID") REFERENCES "Books"("bookID"),
	FOREIGN KEY("userID") REFERENCES "Users"("userID")
);
"""
"""Querys Para Crear Todas (4) Las Tablas De La Base De Datos. Crea la Tabla Books, Users, Orders y OrderDetails"""

QUERY_INSERT_BOOKS = "INSERT INTO Books (isbn,title,autor,description,category,year,pages,publisher,stock_total,stock_available) Values (?,?,?,?,?,?,?,?,?,?)"
"""Query Para Insertar Un Libro En La Base De Datos. El Orden De Los Datos Es: Isbn, Título, Autor, Descripción, Categoría, Año, Páginas, Editorial, Libros Totales, Libros Disponibles"""

QUERY_DELETE_BOOKS = "DELETE FROM Books WHERE bookID = ?"
"""Query Para Eliminar Un Libro En La Base De Datos Mediante bookID"""

QUERY_SEARCH_FILTER_OF_BOOKS = "SELECT DISTINCT category FROM Books"
"""Query Para Buscar Las Categorías Distintas De Todos Los Libros"""

QUERY_INSERT_USERS = "INSERT INTO Users (name,email,phone,id_card) Values (?,?,?,?)"
"""Query Para Insertar Un Usuario En La Base De Datos. El Orden De Los Datos Es: Nombre, Correo Electrónico, Teléfono, Cédula De Identidad"""

QUERY_SEARCH_USERS = "SELECT userID,name,email,phone,id_card,state,registration_date FROM Users WHERE (name LIKE ? OR id_card LIKE ?) AND (state = ? OR ? IS NULL)"
"""Query Para Seleccionar la ID, Nombre, Email, Telefono, cedula, estado (Activo|Inactivo) Y Fecha De Registro De Todos Los Usuarios, Tiene La Capacidad De Filtrar Por Nombre De Usuario, Cedula Y Estado (Activo|Inactivo)"""

QUERY_DELETE_USERS = "DELETE FROM Users WHERE userID = ?"
"""Query Para Eliminar Un Usuario En La Base De Datos Mediante bookID"""

QUERY_SEARCH_ORDERS = """SELECT o.orderID, u.name, u.id_card, b.title, o.status, o.date_lending, o.date_return FROM Orders o
JOIN Users u ON o.userID = u.userID
JOIN Books b ON o.bookID = b.bookID
WHERE (u.name LIKE ? OR b.title LIKE ? OR o.orderID LIKE ?) AND (o.status = ? OR ? IS NULL)
"""
"""Query Para Buscar Las Ordenes Existentes En La Tabla 'Orders' En La Base De Datos. Devuelve Los Valores Necesarios Para Mostrar De Manera Visual Mediante 2 Left Joins. Uno Que Une a Tabla Users Y El Otro Une A La Tabla Books.
Returns:
Devuelve Los Valores: OrderID, Nombre, Cedula, Titulo, Estado, Fecha De Prestamo, Fecha De Devolucion"""

QUERY_LOANS_CHANGE_STATE = "UPDATE Orders SET status = 'Devuelto' WHERE orderID = ?"

def make_cursor(query:str,parameters:tuple = None,fetch:bool=False) -> bool|list:


        """Ejecuta una consulta parametrizada en una conexión independiente.

        Args:
            query: Sentencia SQL a ejecutar.
            parameters: Valores para los marcadores de la sentencia.
            fetch: Si es ``True``, devuelve todas las filas obtenidas.

        Returns:
            Lista de filas, ``True`` si la escritura fue correcta o ``False``
            cuando SQLite informa de un error.
        """
        conn = sqlite3.connect(PATH_DB)
        try:
            cursor = conn.cursor()
            cursor.execute(query,parameters) if parameters else cursor.execute(query)
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return True
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                print("\nBase De Datos Bloqueada")
                return False
            else:
                print("\nError Inesperado: "+type(e).__name__)
                return False
        except Exception as e:
            print(f"\nHa Ocurrido Un Error Inesperado {str(e)}")
            return False
        finally:
            conn.close()
            
def search_books(status:str, category:str|None, title_or_isbn_or_author:str) -> list:
    """Ejecuta Una Query Para Buscar Información De Los Libros Necesarias Para La Vista En Tabla y Detalles. Devuelve Una Lista"""
    status = None if status == "Todos" else status
    category = None if category == "Todas" else category
    value_for_search = f"%{title_or_isbn_or_author}%"
    return make_cursor(QUERY_SEARCH_BOOKS,(status,status,category,category,value_for_search,value_for_search,value_for_search),True)

def add_book(data_book: dict[str, str]) -> bool:
    """Ejecuta Una Query Para Añadir Un Libro A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_BOOKS,tuple(data_book.values())+(data_book["disponibles"],))

def eliminate_book(delete_book:int) -> bool:
    """Ejecuta Una Query Para Eliminar Un Libro De La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_DELETE_BOOKS,(delete_book,))

def search_filter_of_books() -> tuple:
    """Ejecúta Una Query Para Buscar Los Filtros Existentes En La Base De Datos De La Tabla Books. Devuelve Una Tupla Con Los Filtros Distintos Existentes"""
    return tuple(item[0] for item in make_cursor(QUERY_SEARCH_FILTER_OF_BOOKS,fetch=True))

def add_user(data_user: dict[str, str]) -> bool:
    """Ejecuta Una Query Para Añadir Un Usuario A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_USERS,tuple(data_user.values()))
            
def search_users(name_or_id_card:str, status:str) -> list:
    """Ejecuta Una Query Para Buscar Información De Los Usuarios Necesarios Para La Vista En Tabla y Detalles. Devuelve Una Lista"""
    status = None if status == "Todos" else status
    return make_cursor(QUERY_SEARCH_USERS,(f"%{name_or_id_card}%",f"%{name_or_id_card}%",status,status),True)

def eliminate_user(delete_user:int) -> bool:
    """Ejecuta Una Query Para Eliminar Un Libro De La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_DELETE_USERS,(delete_user,))
            
def search_loans(name_or_title_or_id:str,status:str) -> list:
    """Ejecuta Una Query Para Buscar Las Ordenes Existentes. Devuelve Los Valores Necesarios Para Mostrar De Manera Visual
Returns:
Devuelve Los Valores: OrderID, Nombre, Cedula, Titulo, Estado, Fecha De Prestamo, Fecha De Devolucion"""
    value_for_search = f"%{name_or_title_or_id}%"
    status = None if status == "Todos" else status
    print(value_for_search)
    return make_cursor(QUERY_SEARCH_ORDERS,(value_for_search,value_for_search,value_for_search,status,status),fetch=True)

def change_status_loan(loan_id:int) -> None:
    return make_cursor(QUERY_LOANS_CHANGE_STATE,(loan_id,))


class ReportData(TypedDict):
    """Contrato de datos que consume la vista de reportes."""

    active_loans: int
    overdue_loans: int
    inventory_books: int
    registered_users: int
    top_books: list[tuple[str, int]]
    categories: list[tuple[str, int]]
    books_without_activity: list[tuple[str, str]]
    monthly_history: list[tuple[str, int, int]]
    returns_on_time: int
    returns_late: int
    top_readers: list[tuple[str, int]]
    repeat_overdue_users: list[tuple[str, int, str]]


def get_reports_data() -> ReportData:
    """Devuelve datos de ejemplo para construir el módulo de reportes.

    La función mantiene el contrato que después puede sustituirse por consultas
    sobre Books, Users y Orders sin modificar la vista.
    """
    return {
        "active_loans": 84,
        "overdue_loans": 12,
        "inventory_books": 1248,
        "registered_users": 356,
        "top_books": [
            ("El principito", 38),
            ("Cien años de soledad", 32),
            ("Hábitos atómicos", 27),
            ("Sapiens", 24),
            ("Clean Code", 19),
        ],
        "categories": [
            ("Novela", 42),
            ("Tecnología", 24),
            ("Historia", 18),
            ("Desarrollo personal", 16),
        ],
        "books_without_activity": [
            ("Introducción a la astronomía", "Ciencia"),
            ("Atlas del mundo", "Geografía"),
            ("Teoría del color", "Arte"),
            ("Poesía reunida", "Poesía"),
        ],
        "monthly_history": [
            ("Abr", 58, 44),
            ("May", 66, 51),
            ("Jun", 72, 60),
            ("Jul", 81, 68),
            ("Ago", 76, 70),
            ("Sep", 92, 78),
        ],
        "returns_on_time": 86,
        "returns_late": 14,
        "top_readers": [
            ("María González", 18),
            ("Carlos Rodríguez", 15),
            ("Ana Martínez", 12),
            ("Luis Pérez", 10),
        ],
        "repeat_overdue_users": [
            ("Jorge Ramírez", 4, "Hace 2 días"),
            ("Sofía Torres", 3, "Hace 5 días"),
            ("Diego Herrera", 2, "Hace 8 días"),
        ],
    }