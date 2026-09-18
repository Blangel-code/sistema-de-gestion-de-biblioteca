"""Archivo Donde Estarán Ubicadas Las Querys Para Poder Hacer Consultas En SQLite"""

import sqlite3
from pathlib import Path

PATH_DB =  Path(__file__).resolve().parent / "data" / "data.db"
"""Ruta De La Base De Datos SQLite"""
PATH_DB.parent.mkdir(parents=True,exist_ok=True)

QUERY_SEARCH_BOOKS = "SELECT bookID,isbn,title,autor,CASE WHEN stock_available = 0 THEN 'Inactivo' ELSE 'Activo' END AS status,category,publisher,year,pages,description FROM Books WHERE (status = ? OR ? IS NULL) AND (category = ? OR ? IS NULL) AND (title LIKE ? OR isbn LIKE ?)"
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
	"fecha_prestamo"	DATE DEFAULT CURRENT_DATE,
	"fecha_limite"	DATE NOT NULL,
	PRIMARY KEY("orderID" AUTOINCREMENT),
	FOREIGN KEY("userID") REFERENCES "Users"("userID")
);
CREATE TABLE IF NOT EXISTS "OrderDetails" (
	"detailID"	INTEGER,
	"orderID"	INTEGER NOT NULL,
	"book_id"	INTEGER NOT NULL,
	"fecha_devolucion"	DATE,
	PRIMARY KEY("detailID" AUTOINCREMENT),
	FOREIGN KEY("book_id") REFERENCES "Books"("bookID"),
	FOREIGN KEY("orderID") REFERENCES "Orders"("orderID")
);
"""
"""Querys Para Crear Todas (4) Las Tablas De La Base De Datos. Crea la Tabla Books, Users, Orders y OrderDetails"""

QUERY_INSERT_BOOKS = "INSERT INTO Books (isbn,title,autor,description,category,year,pages,publisher,stock_total,stock_available) Values (?,?,?,?,?,?,?,?,?,?)"
"""Query Para Insertar Un Libro En La Base De Datos. El Orden De Los Datos Es: Isbn, Título, Autor, Descripción, Categoría, Año, Páginas, Editorial, Libros Totales, Libros Disponibles"""

QUERY_DELETE_BOOKS = "DELETE FROM Books WHERE bookID = ?"
"""Query Para Eliminar Un Libro Mediante bookID"""

QUERY_SEARCH_FILTER_OF_BOOKS = "SELECT DISTINCT category FROM Books"
"""Query Para Buscar Las Categorías Distintas De Todos Los Libros"""

QUERY_INSERT_USERS = "INSERT INTO Users (name,email,phone,id_card) Values (?,?,?,?)"
"""Query Para Insertar Un Usuario En La Base De Datos. El Orden De Los Datos Es: Nombre, Correo Electrónico, Teléfono, Cédula De Identidad"""

QUERY_SEARCH_USERS = "SELECT userID,name,email,phone,id_card,state,registration_date FROM Users"
"""Query Para Seleccionar la ID, Isbn, Título, Autor, Estado (Activo|Inactivo), Categoría, Editorial, Anio y Paginas De Todos Los Libros"""

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
            
def search_books(status:str|None, category:str|None, title_or_isbn:str) -> list:
    """Ejecuta Una Query Para Buscar Información De Los Libros Necesarias Para La Vista En Tabla y Detalles. Devuelve Una Lista Con Tuplas"""
    status = None if status == "Todos" else status
    category = None if category == "Todas" else category
    return make_cursor(QUERY_SEARCH_BOOKS,(status,status,category,category,f"%{title_or_isbn}%",f"%{title_or_isbn}%"),True)

def add_book(data_book: dict[str, str]) -> bool:
    """Ejecuta Una Query Para Añadir Un Libro A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_BOOKS,tuple(data_book.values())+(data_book["disponibles"],))

def eliminate_book(delete_book:int) -> bool:
    """Ejecuta Una Query Para Eliminar Un Libro De La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_DELETE_BOOKS,(delete_book,))

def search_filter_of_books() -> tuple:
    """Ejecúta Una Query Para Buscar Los Filtros Existentes En La Base De Datos De La Tabla Books. Devuelve Una Filtra Con Los Filtros Distintos Existentes"""
    return tuple(item[0] for item in make_cursor(QUERY_SEARCH_FILTER_OF_BOOKS,fetch=True))

def add_user(data_user: dict[str, str]) -> bool:
    """Ejecuta Una Query Para Añadir Un Usuario A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_USERS,tuple(data_user.values()))
            
def search_users() -> list:
    """Ejecuta Una Query Para Buscar Información De Los Usuarios Necesarios Para La Vista En Tabla y Detalles. Devuelve Una Lista"""
    return make_cursor(QUERY_SEARCH_USERS,fetch=True)