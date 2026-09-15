"""Archivo Donde Estarán Ubicadas Las Querys Para Poder Hacer Consultas En SQLite"""

import sqlite3
from pathlib import Path

PATH_DB =  Path(__file__).resolve().parent / "data" / "data.db"
"""Ruta De La Base De Datos SQLite"""
PATH_DB.parent.mkdir(parents=True,exist_ok=True)

QUERY_SEARCH_BOOKS = "SELECT bookID,isbn,title,autor,CASE WHEN stock_available = 0 THEN 'Inactivo' ELSE 'Activo' END AS status,category,publisher,year,pages,description FROM Books"
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
	"state"	TEXT NOT NULL DEFAULT 'Activo',
	"fecha_registro"	DATE DEFAULT CURRENT_DATE,
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
            
def search_books():
    return make_cursor(QUERY_SEARCH_BOOKS,fetch=True)

def add_book(data_book: dict[str, str]):
    return make_cursor(QUERY_INSERT_BOOKS,tuple(data_book.values())+(data_book["disponibles"],))

def eliminate_book(delete_book:int):
    return make_cursor(QUERY_DELETE_BOOKS,(delete_book,))