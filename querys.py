"""Archivo Donde Estarán Ubicadas Las Querys Para Poder Hacer Consultas En SQLite"""

import sqlite3
from pathlib import Path
from typing import TypedDict

PATH_DB =  Path(__file__).resolve().parent / "data" / "data.db"
"""Ruta De La Base De Datos SQLite"""
PATH_DB.parent.mkdir(parents=True,exist_ok=True)

QUERY_SEARCH_BOOKS = "SELECT bookID,isbn,title,autor,CASE WHEN stock_available = 0 THEN 'Inactivo' ELSE 'Activo' END AS status,category,publisher,year,pages,description,stock_total,stock_available FROM Books WHERE (status = ? OR ? IS NULL) AND (category = ? OR ? IS NULL) AND (title LIKE ? OR isbn LIKE ? OR autor LIKE ?)"
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
    "actual_return_date" DATE,
	PRIMARY KEY("orderID" AUTOINCREMENT),
    FOREIGN KEY("bookID") REFERENCES "Books"("bookID"),
	FOREIGN KEY("userID") REFERENCES "Users"("userID")
);
"""
"""Querys Para Crear Todas (4) Las Tablas De La Base De Datos. Crea la Tabla Books, Users, Orders y OrderDetails"""

QUERY_INSERT_BOOKS = "INSERT INTO Books (isbn,title,autor,description,category,year,pages,publisher,stock_total,stock_available) Values (?,?,?,?,?,?,?,?,?,?)"
"""Query Para Insertar Un Libro En La Base De Datos. El Orden De Los Datos Es: Isbn, Título, Autor, Descripción, Categoría, Año, Páginas, Editorial, Libros Totales, Libros Disponibles"""

QUERY_DELETE_BOOKS = "DELETE FROM Books b WHERE b.bookID = ? AND NOT EXISTS (SELECT 1 FROM Orders o WHERE o.bookID = b.bookID AND o.status = 'Activo')"
"""Query Para Eliminar Un Libro En La Base De Datos Mediante bookID"""
QUERY_UPDATE_BOOK = """UPDATE Books SET isbn = ?, title = ?, autor = ?, description = ?,
category = ?, year = ?, pages = ?, publisher = ?, stock_total = ?, stock_available = ?
WHERE bookID = ?"""
"""Actualiza la ficha y las cantidades de inventario de un libro."""

QUERY_SEARCH_FILTER_OF_BOOKS = "SELECT DISTINCT category FROM Books"
"""Query Para Buscar Las Categorías Distintas De Todos Los Libros"""

QUERY_INSERT_USERS = "INSERT INTO Users (name,email,phone,id_card) Values (?,?,?,?)"
"""Query Para Insertar Un Usuario En La Base De Datos. El Orden De Los Datos Es: Nombre, Correo Electrónico, Teléfono, Cédula De Identidad"""

QUERY_SEARCH_USERS = "SELECT userID,name,email,phone,id_card,state,registration_date FROM Users WHERE (name LIKE ? OR id_card LIKE ?) AND (state = ? OR ? IS NULL)"
"""Query Para Seleccionar la ID, Nombre, Email, Telefono, cedula, estado (Activo|Inactivo) Y Fecha De Registro De Todos Los Usuarios, Tiene La Capacidad De Filtrar Por Nombre De Usuario, Cedula Y Estado (Activo|Inactivo)"""

QUERY_DELETE_USERS = "DELETE FROM Users WHERE userID = ?"
"""Query Para Eliminar Un Usuario En La Base De Datos Mediante bookID"""
QUERY_UPDATE_USER = """UPDATE Users SET name = ?, email = ?, phone = ?, id_card = ? WHERE userID = ?"""
"""Actualiza los datos editables de un usuario."""

QUERY_SEARCH_ORDERS = """SELECT orderID, name, id_card, title, display_status,
date_lending, date_return, status
FROM (
    SELECT o.orderID, u.name, u.id_card, b.title,
        CASE
            WHEN (o.status = 'Activo' AND date(o.date_return) < date('now'))
              OR (o.status = 'Devuelto'
                  AND o.actual_return_date IS NOT NULL
                  AND date(o.actual_return_date) > date(o.date_return))
            THEN 'Retrasado'
            ELSE o.status
        END AS display_status,
        o.date_lending, o.date_return, o.status
    FROM Orders o
    JOIN Users u ON o.userID = u.userID
    JOIN Books b ON o.bookID = b.bookID
)
WHERE (name LIKE ? OR title LIKE ?)
  AND (display_status = ? OR ? IS NULL)
"""
"""Query Para Buscar Las Ordenes Existentes En La Tabla 'Orders' En La Base De Datos. Devuelve Los Valores Necesarios Para Mostrar De Manera Visual Mediante 2 Left Joins. Uno Que Une a Tabla Users Y El Otro Une A La Tabla Books.
Returns:
Devuelve Los Valores: OrderID, Nombre, Cedula, Titulo, Estado, Fecha De Prestamo, Fecha De Devolucion"""

QUERY_SELECT_USERS_FOR_LOANS = "SELECT userID, name, id_card, state FROM Users"
"""Query Para Seleccionar Los Usuarios Disponibles Para Registrar Prestamos"""

QUERY_SELECT_BOOKS_FOR_LOANS = "SELECT bookID, title, isbn, stock_available FROM Books"
"""Query Para Seleccionar Los Libros Y Su Disponibilidad Para Registrar Prestamos"""

QUERY_INSERT_LOAN = "INSERT INTO Orders (userID, bookID, date_return) SELECT ?, ?, ? WHERE EXISTS (SELECT 1 FROM Users WHERE userID = ? AND state = 'Activo')"
QUERY_DISCOUNT_BOOK = "UPDATE Books SET stock_available = stock_available - 1 WHERE bookID = ? AND stock_available > 0"
QUERY_ACOUNT_BOOK = "UPDATE Books SET stock_available = stock_available + 1 WHERE bookID = ?"

QUERY_LOANS_CHANGE_STATE = """UPDATE Orders
SET status = 'Devuelto', actual_return_date = date('now')
WHERE orderID = ? AND status != 'Devuelto'"""
QUERY_RETURN_BOOK = """UPDATE Books 
SET stock_available = stock_available + 1 
WHERE bookID = (
    SELECT bookID 
    FROM Orders 
    WHERE orderID = ? AND status != 'Devuelto'
)
"""
"""Incrementa el inventario al devolver un libro."""

QUERY_REPORT_ACTIVE_LOANS = "SELECT COUNT(*) FROM Orders WHERE status = 'Activo'"
QUERY_REPORT_OVERDUE_LOANS = "SELECT COUNT(*) FROM Orders WHERE status = 'Activo' AND date(date_return) < date('now')"
QUERY_REPORT_INVENTORY_BOOKS = "SELECT COALESCE(SUM(stock_total), 0) FROM Books"
QUERY_REPORT_REGISTERED_USERS = "SELECT COUNT(*) FROM Users WHERE state = 'Activo'"
QUERY_REPORT_TOP_BOOKS = """SELECT b.title, COUNT(*) AS loans
FROM Orders o
JOIN Books b ON b.bookID = o.bookID
GROUP BY b.bookID, b.title
ORDER BY loans DESC, b.title
LIMIT ?"""
QUERY_REPORT_CATEGORIES = """SELECT b.category, COUNT(*) AS loans
FROM Orders o
JOIN Books b ON b.bookID = o.bookID
GROUP BY b.category
ORDER BY loans DESC, b.category
LIMIT ?"""
QUERY_REPORT_BOOKS_WITHOUT_ACTIVITY = """SELECT b.title, b.category
FROM Books b
LEFT JOIN Orders o ON o.bookID = b.bookID
WHERE o.orderID IS NULL
ORDER BY b.title"""
QUERY_REPORT_MONTHLY_HISTORY = """WITH RECURSIVE months(month_start) AS (
    SELECT date('now', 'start of month', '-2 months')
    UNION ALL
    SELECT date(month_start, '+1 month')
    FROM months
    WHERE month_start < date('now', 'start of month')
)
SELECT
    CASE strftime('%m', month_start)
        WHEN '01' THEN 'Ene' WHEN '02' THEN 'Feb' WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Abr' WHEN '05' THEN 'May' WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul' WHEN '08' THEN 'Ago' WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct' WHEN '11' THEN 'Nov' ELSE 'Dic'
    END AS month_name,
    (SELECT COUNT(*) FROM Orders WHERE date(date_lending) >= month_start
        AND date(date_lending) < date(month_start, '+1 month')) AS lent,
    (SELECT COUNT(*) FROM Orders WHERE status = 'Devuelto'
        AND date(actual_return_date) >= month_start
        AND date(actual_return_date) < date(month_start, '+1 month')) AS returned
FROM months
ORDER BY month_start"""
QUERY_REPORT_RETURNS = """SELECT
    COALESCE(ROUND(100.0 * SUM(CASE WHEN date(actual_return_date) <= date(date_return) THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)), 0),
    COALESCE(ROUND(100.0 * SUM(CASE WHEN date(actual_return_date) > date(date_return) THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)), 0)
FROM Orders
WHERE status = 'Devuelto' AND actual_return_date IS NOT NULL"""
QUERY_REPORT_TOP_READERS = """SELECT u.name, COUNT(*) AS loans
FROM Orders o
JOIN Users u ON u.userID = o.userID
GROUP BY u.userID, u.name
ORDER BY loans DESC, u.name
LIMIT ?"""
QUERY_REPORT_REPEAT_OVERDUE_USERS = """WITH overdue AS (
    SELECT userID, MAX(COALESCE(actual_return_date, date_return)) AS last_overdue_date
    FROM Orders
    WHERE (status = 'Activo' AND date(date_return) < date('now'))
       OR (status = 'Devuelto' AND date(actual_return_date) > date(date_return))
    GROUP BY userID
    HAVING COUNT(*) > 1
)
SELECT u.name, COUNT(o.orderID) AS overdue_count,
       'Hace ' || CAST(MAX(julianday('now') - julianday(overdue.last_overdue_date)) AS INTEGER) || ' días'
FROM overdue
JOIN Users u ON u.userID = overdue.userID
JOIN Orders o ON o.userID = overdue.userID
WHERE (o.status = 'Activo' AND date(o.date_return) < date('now'))
   OR (o.status = 'Devuelto' AND date(o.actual_return_date) > date(o.date_return))
GROUP BY u.userID, u.name, overdue.last_overdue_date
ORDER BY overdue_count DESC, u.name
LIMIT ?"""

QUERY_EXPORT_BOOKS = """SELECT bookID, isbn, title, autor, category, publisher, year,
pages, description, stock_total, stock_available
FROM Books
ORDER BY bookID"""
QUERY_EXPORT_USERS = """SELECT userID, name, email, phone, id_card, state, registration_date
FROM Users
WHERE date(registration_date) BETWEEN date(?) AND date(?)
ORDER BY userID"""
QUERY_EXPORT_ORDERS = """SELECT orderID, userID, bookID, status, date_lending,
date_return, actual_return_date
FROM Orders
WHERE date(date_lending) BETWEEN date(?) AND date(?)
ORDER BY orderID"""

QUERY_DASHBOARD_SUMMARY = """SELECT
    (SELECT COALESCE(SUM(stock_total), 0) FROM Books),
    (SELECT COUNT(*) FROM Users WHERE state = 'Activo'),
    (SELECT COUNT(*) FROM Orders WHERE status = 'Activo'),
    (SELECT COUNT(*) FROM Orders
     WHERE status = 'Activo' AND date(date_return) < date('now'))"""
QUERY_DASHBOARD_ACTIVITY = """SELECT b.title, u.name, o.date_lending,
    CASE
        WHEN o.status = 'Activo' AND date(o.date_return) < date('now') THEN 'Retrasado'
        WHEN o.status = 'Activo' THEN 'Activo'
        ELSE 'Devuelto'
    END AS display_status
FROM Orders o
JOIN Books b ON b.bookID = o.bookID
JOIN Users u ON u.userID = o.userID
ORDER BY datetime(o.date_lending) DESC, o.orderID DESC
LIMIT ?"""

def make_cursor(query:str,parameters:tuple = (),fetch:bool=False, message:str|None = None, comprobate_delete:bool=False) -> tuple[bool, str]|list:


        """Ejecuta una consulta parametrizada en una conexión independiente.

        Args:
            query: Sentencia SQL a ejecutar.
            parameters: Valores para los marcadores de la sentencia.
            fetch: Si es ``True``, devuelve todas las filas obtenidas.

        Returns:
            Lista de filas, ``True`` si la escritura fue correcta o ``False``
            cuando SQLite informa de un error.
        """
        
        try:
            with sqlite3.connect(PATH_DB) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(query,parameters)
                
                if fetch:
                    return cursor.fetchall()
                if comprobate_delete and cursor.rowcount == 0:
                    return False, "No Se Ha Eliminado De La Base De Datos"
            return True, message
        
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                return False, "Base De Datos Bloqueada"
            else:
                return False, f"Error Operacional Inesperado: {type(e).__name__}"
        except Exception as e:
            return False, f"Ha Ocurrido Un Error Inesperado {str(e)}"
        finally:
            conn.close()
            
def search_books(status:str, category:str|None, title_or_isbn_or_author:str) -> list:
    """Ejecuta Una Query Para Buscar Información De Los Libros Necesarias Para La Vista En Tabla y Detalles. Devuelve Una Lista"""
    status = None if status == "Todos" else status
    category = None if category == "Todas" else category
    value_for_search = f"%{title_or_isbn_or_author}%"
    return make_cursor(QUERY_SEARCH_BOOKS,(status,status,category,category,value_for_search,value_for_search,value_for_search),True)

def add_book(data_book: dict[str, str]) -> tuple[bool, str]:
    """Ejecuta Una Query Para Añadir Un Libro A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_BOOKS,tuple(data_book.values())+(data_book["disponibles"],))

def eliminate_book(delete_book: int) -> tuple[bool, str]:
    """Elimina un libro solo cuando no tiene préstamos activos."""
    return make_cursor(QUERY_DELETE_BOOKS,(delete_book,),message="Libro Eliminado Con Éxito",comprobate_delete=True)

def search_filter_of_books() -> list:
    """Ejecúta Una Query Para Buscar Los Filtros Existentes En La Base De Datos De La Tabla Books. Devuelve Una Tupla Con Los Filtros Distintos Existentes"""
    return tuple(item[0] for item in make_cursor(QUERY_SEARCH_FILTER_OF_BOOKS,fetch=True))

def add_user(data_user: dict[str, str]) -> tuple[bool, str]:
    """Ejecuta Una Query Para Añadir Un Usuario A La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_INSERT_USERS,tuple(data_user.values()),comprobate_delete=True,message="Usuario Añadido Con Éxito")
            
def search_users(name_or_id_card:str, status:str) -> list:
    """Ejecuta Una Query Para Buscar Información De Los Usuarios Necesarios Para La Vista En Tabla y Detalles. Devuelve Una Lista"""
    status = None if status == "Todos" else status
    return make_cursor(QUERY_SEARCH_USERS,(f"%{name_or_id_card}%",f"%{name_or_id_card}%",status,status),True)

def eliminate_user(delete_user:int) ->  tuple[bool, str]:
    """Ejecuta Una Query Para Eliminar Un Libro De La Base De Datos. Devuelve False Si Ocurrió Un Error o True Si Se Ejecutó Correctamente"""
    return make_cursor(QUERY_DELETE_USERS,(delete_user,),comprobate_delete=True,message="El Usuario Se Ha Eliminado Con Éxito")
            
def search_loans(name_or_title:str,status:str) -> list:
    """Ejecuta Una Query Para Buscar Las Ordenes Existentes. Devuelve Los Valores Necesarios Para Mostrar De Manera Visual
Returns:
Devuelve Los Valores: OrderID, Nombre, Cedula, Titulo, Estado, Fecha De Prestamo, Fecha De Devolucion"""
    value_for_search = f"%{name_or_title}%"
    status = None if status == "Todos" else status
    return make_cursor(QUERY_SEARCH_ORDERS,(value_for_search,value_for_search,status,status),fetch=True)

def change_status_loan(loan_id: int) -> tuple[bool, str]:
    """Marca una orden como devuelta y repone el ejemplar en una sola transacción."""
    success, msg = make_cursor(QUERY_RETURN_BOOK,(loan_id,),comprobate_delete=True)
    if not success:
        return success, "No Se Ha Devuelto El Libro Correctamente. "+msg
    return make_cursor(QUERY_LOANS_CHANGE_STATE,(loan_id,),message="Se Ha Devuelto El Libro Correctamente")

def create_loan(user_id: int, book_id: int, return_date: str) -> tuple[bool, str]:
    """Valida y crea un préstamo descontando inventario atómicamente."""
    success, msg = make_cursor(QUERY_DISCOUNT_BOOK, (book_id,),comprobate_delete=True,)
    if not success:
        return False, "El Libro No Existe O No Hay Stock Disponible. "+msg
    success, msg = make_cursor(QUERY_INSERT_LOAN, (user_id, book_id, return_date, user_id),comprobate_delete=True,message="Se Ha Creado El Prestamo Con Éxito")
    if not success:
        make_cursor(QUERY_ACOUNT_BOOK,(book_id,),comprobate_delete=True)
        return False, "El Usuario No Existe O No Está En Estado Activo. "+msg
    return True, msg

def update_user(user_id: int, data_user: dict[str, str]) -> tuple[bool, str]:
    """Actualiza un usuario mediante una consulta parametrizada."""
    return make_cursor(
        QUERY_UPDATE_USER,
        (
            data_user["nombre"],
            data_user["gmail"],
            data_user["telefono"],
            data_user["cedula"],
            user_id,
        ),
        comprobate_delete=True,message="El Usuario Se Ha Editado Con Éxito"
    )


def update_book(book_id: int, data_book: dict[str, str]) -> tuple[bool, str]:
    """Actualiza un libro aplicando la variación al stock disponible.

    La disponibilidad nueva se calcula como ``nuevo_total >= (total_actual
    - disponible_actual)``. Así, reducir el stock consume únicamente ejemplares
    disponibles y nunca modifica los ejemplares comprometidos por préstamos.
"""
    list_values_books = make_cursor("SELECT stock_total, stock_available FROM Books WHERE bookID = ?",(book_id,),fetch=True)[0]
    if not list_values_books:
        return False, "No Se Ha Podido Seleccionar El Libro"
    prestados = list_values_books[1]-list_values_books[0]
    if int(data_book["disponibles"]) < prestados:
        return False, f"No puedes reducir el stock a {data_book["totales"]} porque hay {prestados} libros prestados."
    success, msg = make_cursor(
        QUERY_UPDATE_BOOK,
        (
            data_book["isbn"], data_book["titulo"], data_book["autor"],
            data_book["descripcion"], data_book["categoria"],
            int(data_book["anio"]), int(data_book["paginas"]),
            data_book["editorial"], int(data_book["disponibles"]) - prestados, int(data_book["disponibles"]), book_id,
        ),
    comprobate_delete=True,
    message="Se Ha Editado El Libro Con Éxito"
    )
    if not success:
        return success, "No Se Ha Actualizado El Libro. "+msg
    return success, msg

def select_users_and_books_for_loans() -> list:
    
    """Ejecuta Una Query Para Buscar Informacion Basica Sobre Usuarios Y Libros
    Returns:
    Devuelve 2 Variables Distintas; La Primera Una Lista De Los Usuarios Y La Segunda Una Lista De Los Libros"""
    return make_cursor(QUERY_SELECT_USERS_FOR_LOANS,fetch=True), make_cursor(QUERY_SELECT_BOOKS_FOR_LOANS,fetch=True)


def get_export_data(start_date: str, end_date: str) -> dict[str, list[tuple]]:
    """Obtiene las tres tablas para exportarlas respetando el rango indicado."""
    data = {
        "Books": make_cursor(QUERY_EXPORT_BOOKS, fetch=True),
        "Users": make_cursor(QUERY_EXPORT_USERS, (start_date, end_date), fetch=True),
        "Orders": make_cursor(QUERY_EXPORT_ORDERS, (start_date, end_date), fetch=True),
    }
    if any(not isinstance(rows, list) for rows in data.values()):
        raise RuntimeError("No se pudieron obtener los datos para exportar")
    return data


def get_dashboard_data() -> dict[str, int | list[tuple[str, str, str, str]]]:
    """Obtiene los indicadores y movimientos recientes del panel principal."""
    summary = make_cursor(QUERY_DASHBOARD_SUMMARY, fetch=True)
    activity = make_cursor(QUERY_DASHBOARD_ACTIVITY, (5,), fetch=True)
    if (
        not isinstance(summary, list)
        or not summary
        or not isinstance(activity, list)
    ):
        raise RuntimeError("No se pudo obtener la información del dashboard")
    return {
        "inventory_books": int(summary[0][0]),
        "active_users": int(summary[0][1]),
        "active_loans": int(summary[0][2]),
        "overdue_loans": int(summary[0][3]),
        "activity": activity,
    }

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


def _report_value(query: str, parameters: tuple = ()) -> int:
    """Obtiene un único valor escalar de una consulta de reporte."""
    result = make_cursor(query, parameters, fetch=True)
    if not isinstance(result, list) or not result or not result[0]:
        raise RuntimeError("No se pudo obtener un valor del reporte")
    return int(result[0][0] or 0)


def get_report_data() -> ReportData:
    """Construye el reporte a partir de los datos actuales de SQLite."""
    top_books = make_cursor(QUERY_REPORT_TOP_BOOKS, (5,), fetch=True)
    categories = make_cursor(QUERY_REPORT_CATEGORIES, (4,), fetch=True)
    books_without_activity = make_cursor(QUERY_REPORT_BOOKS_WITHOUT_ACTIVITY, fetch=True)
    monthly_history = make_cursor(QUERY_REPORT_MONTHLY_HISTORY, fetch=True)
    returns = make_cursor(QUERY_REPORT_RETURNS, fetch=True)
    top_readers = make_cursor(QUERY_REPORT_TOP_READERS, (4,), fetch=True)
    repeat_overdue_users = make_cursor(QUERY_REPORT_REPEAT_OVERDUE_USERS, (4,), fetch=True)
    report_lists = (
        top_books,
        categories,
        books_without_activity,
        monthly_history,
        returns,
        top_readers,
        repeat_overdue_users,
    )
    if any(not isinstance(result, list) for result in report_lists):
        raise RuntimeError("No se pudo construir el reporte desde la base de datos")

    return {
        "active_loans": _report_value(QUERY_REPORT_ACTIVE_LOANS),
        "overdue_loans": _report_value(QUERY_REPORT_OVERDUE_LOANS),
        "inventory_books": _report_value(QUERY_REPORT_INVENTORY_BOOKS),
        "registered_users": _report_value(QUERY_REPORT_REGISTERED_USERS),
        "top_books": top_books,
        "categories": categories,
        "books_without_activity": books_without_activity,
        "monthly_history": monthly_history,
        "returns_on_time": int(returns[0][0]) if returns else 0,
        "returns_late": int(returns[0][1]) if returns else 0,
        "top_readers": top_readers,
        "repeat_overdue_users": repeat_overdue_users,
    }


def get_reports_data() -> ReportData:
    """Compatibilidad con las vistas que usan el nombre anterior."""
    return get_report_data()