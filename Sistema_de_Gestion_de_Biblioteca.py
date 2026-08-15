import sqlite3
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_final = os.path.join(ruta_base,"datos.db")

#Query Para Agregar Libros
QUERY_AGREGAR_LIBROS = "INSERT INTO Books VALUES (?,?,?,?,?)"
#Query Para Buscar Un Libro
QUERY_BUSCAR_LIBRO = "SELECT * FROM Books WHERE BookID = ? OR Title = ?"
#Query Para Mostrar TODOS Los Libros
QUERY_MOSTRAR_LIBROS = "SELECT * FROM Books"
#Querys Para Actualizar Libro
QUERYS_ACTUALIZAR_LIBRO = {
    "Title" : "UPDATE Books SET Title = ? WHERE BookID = ?",
    "BookID" : "UPDATE Books SET BookID = ? WHERE BookID = ?",
    "Autor" : "UPDATE Books SET Autor = ? WHERE BookID = ?",
    "SumExistingBooks" : "UPDATE Books SET BooksAvaibles = BooksAvaibles + ?, ExistingBooks = ExistingBooks + ? WHERE BookID = ?",
    "MinusExistingBooks" : "UPDATE Books SET BooksAvaibles = BooksAvaibles - ?, ExistingBooks = ExistingBooks - ? WHERE BookID = ?",
    }
#Query Para Eliminar Un Libro
QUERY_ELIMINAR_LIBRO = "DELETE FROM Books WHERE BookID = ?"
#Query Para Agregar Usuarios
QUERY_AGREGAR_USUARIO = "INSERT INTO Users VALUES (?,?,?,?)"
#Query Para Buscar TODOS Los Usuarios ()
QUERY_MOSTRAR_USUARIOS = """SELECT u.UserID, Name, Age, TotalBooks, GROUP_CONCAT(OrderDate, ', ') AS Dates, b.BookID, b.Title, b.Autor FROM Users u
    LEFT JOIN Orders o ON o.UserID = u.UserID
    LEFT JOIN Books b ON o.BookID = b.BookID
    GROUP BY u.UserID, o.BookID
    ORDER BY u.UserID
"""
#Query Para Buscar Un Usuario
QUERY_BUSCAR_USUARIO = "SELECT * FROM Users WHERE UserID = ? OR Name = ?"
#Query Para Eliminar Un Usuario
QUERY_ELIMINAR_USUARIO = "DELETE FROM Users WHERE UserID = ?"
#Querys Para Actualizar Usuario
QUERYS_ACTUALIZAR_USUARIO = {
    "Name" : "UPDATE Users SET Name = ? WHERE UserID = ?",
    "UserID" : "UPDATE Users SET UserID = ? WHERE UserID = ?",
    "Age" : "UPDATE Users SET Age = ?, TotalBooks = ? WHERE UserID = ?",
    }
#Query Para Crear Una Orden
QUERYS_CREAR_ORDEN = {
    "actualizar_Books" : "UPDATE Books SET BooksAvaibles = BooksAvaibles - 1 WHERE BookID = ?",
    "actualizar_Users" : "UPDATE Users SET TotalBooks = TotalBooks - 1 WHERE UserID = ?",
    "crear_orden" : "INSERT INTO Orders (BookID,UserID,OrderDate) VALUES (?,?,datetime('now', 'localtime'))",
}
#Query Para Eliminar Una Orden
QUERYS_ELIMINAR_ORDEN = {
    "actualizar_Books" : "UPDATE Books SET BooksAvaibles = BooksAvaibles + 1 WHERE BookID = ?",
    "actualizar_Users" : "UPDATE Users SET TotalBooks = TotalBooks + 1 WHERE UserID = ?",
    "encontrar_orden" : "SELECT OrderID FROM Orders WHERE UserID = ? AND BookID = ? ORDER BY OrderID LIMIT 1",
    "eliminar_orden" : "DELETE FROM Orders WHERE OrderID = ?",
}
#QueryS Para Crear Las Tablas
QUERYS_CREAR_TABLAS = {
    "crear_Books" : """CREATE TABLE "Books" (
	"BookID"	TEXT UNIQUE,
	"Title"	TEXT,
	"Autor"	TEXT,
	"BooksAvaibles"	INTEGER,
	"ExistingBooks"	INTEGER,
	PRIMARY KEY("BookID")
)""",
    "crear_Orders" : """CREATE TABLE "Orders" (
	"OrderID"	INTEGER,
	"BookID"	TEXT,
	"UserID"	INTEGER,
	"OrderDate"	TEXT,
	PRIMARY KEY("OrderID" AUTOINCREMENT)
)""",
    "crear_Users" : """CREATE TABLE "Users" (
	"UserID"	INTEGER UNIQUE,
	"Name"	TEXT,
	"Age"	INTEGER,
	"TotalBooks"	INTEGER,
	PRIMARY KEY("UserID")
)"""
}

with sqlite3.connect(ruta_final) as conn:
    try:
      conn.cursor().execute("SELECT Name FROM Users LIMIT 1")
    except Exception as e:
      if str(e) == "no such table: Users":
        conn.cursor().execute(QUERYS_CREAR_TABLAS["crear_Books"])
        conn.cursor().execute(QUERYS_CREAR_TABLAS["crear_Orders"])
        conn.cursor().execute(QUERYS_CREAR_TABLAS["crear_Users"])
        conn.commit()
      else:
        print(f"Ocurrió Un Error Inesperado Al Intentar Crear La Tabla ({e})")


class SalirAlMenu(Exception):
    pass

def pedir_input(mensaje):
    entrada = input(mensaje)
    if entrada.lower() == "salir" or entrada.lower() == "0":
        print("\nSaliendo hacia al menu principal...")
        raise SalirAlMenu()
    return entrada

class Libro:
    def __init__(self,titulo,autor,isbn,libros_disponibles,libros_existentes):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.libros_disponibles = libros_disponibles
        self.libros_existentes = libros_existentes

class Usuario:
    def __init__(self,nombre,id_usuario,edad,limite_de_libros):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.edad = edad
        self.limite_de_libros = limite_de_libros
        
class Biblioteca:
    def encontrar_usuario(self,usuario_o_id):
        with sqlite3.connect(ruta_final) as conn:
            usuario_encontrado = conn.cursor().execute(QUERY_BUSCAR_USUARIO,(usuario_o_id,usuario_o_id)).fetchall()
        if len(usuario_encontrado) > 1:
            x = 1
            print("\nSelecciona un Usuario:  ")
            for usuarios in usuario_encontrado:
                print(f"{x}) {usuarios[1]} | {usuarios[0]}")
                x += 1
            while True:
                numero_usuario = pedir_input("\nIngrese el numero: ")
                if not numero_usuario.isnumeric():
                    print("\nError: Opcion no encontrada")
                    continue
                numero_usuario = int(numero_usuario)
                if numero_usuario <= len(usuario_encontrado):
                    usuario_encontrado = usuario_encontrado[numero_usuario-1]
                    break
                print("\nError: Opcion no encontrada")
        else:
            if usuario_encontrado:
                usuario_encontrado = usuario_encontrado[0]
        return usuario_encontrado

    def encontrar_libro(self,isbn_o_titulo):
        with sqlite3.connect(ruta_final) as conn:
            libro_encontrado = conn.cursor().execute(QUERY_BUSCAR_LIBRO,(isbn_o_titulo,isbn_o_titulo)).fetchall()
        if len(libro_encontrado) > 1:
            x = 1
            print("\nSelecciona un Libro:  ")
            for libro in libro_encontrado:
                print(f"{x}) {libro[1]}, {libro[2]}")
                x += 1
            while True:
                numero_libro = pedir_input("\nIngrese el numero: ")
                if not numero_libro.isnumeric():
                    print("\nError: Opcion no encontrada")
                    continue
                numero_libro = int(numero_libro)
                if numero_libro <= len(libro_encontrado):
                    libro_encontrado = libro_encontrado[numero_libro-1]
                    break
                print("\nError: Opcion no encontrada")
        else:
            if libro_encontrado:
                libro_encontrado = libro_encontrado[0]
        return libro_encontrado
    
    def eliminar_libro(self):
        while True:
            isbn_o_titulo = pedir_input("\nIngresa el ISBN o Nombre del libro: ").strip()
            libro_encontrado = self.encontrar_libro(isbn_o_titulo)
            if not libro_encontrado:
                print("\nError: No existe un libro con ese ISBN")
                continue
            break
        print(f"\nLibro seleccionado: {libro_encontrado[1]}")
        if libro_encontrado[3] != libro_encontrado[4]:
            print("\nError: No se puede eliminar si hay al menos un libro prestado")
            return
        while True: 
            confirmacion = pedir_input("\n¿Estás seguro de eliminar este libro? (y/n): ").lower()
            if confirmacion == "y":
                with sqlite3.connect(ruta_final) as conn:
                    conn.cursor().execute(QUERY_ELIMINAR_LIBRO,(libro_encontrado[0],))
                    conn.commit()
                print(f"\nEl libro {libro_encontrado[1]} fue eliminado con exito")
            elif confirmacion == "n":
                print("\nLibro no eliminado")
            else:
                print("\nError: No se ha seleccionado una opcion valida")
                continue
            break
    
    def registrar_libro(self):
        while True:
            titulo = pedir_input("\nTítulo del libro: ").strip()
            if titulo:
                break
            print("\nError: El titulo debe contener al menos un caracter")
        while True:
            autor = pedir_input("Autor: ").strip()
            if autor:
                break
            print("\nError: El autor debe contener al menos un caracter\n")
        while True:
            isbn = pedir_input("Ingresa el ISBN del libro: ").strip()
            if not isbn.replace("-", "", 1).isnumeric() or not isbn.count("-") == 1:
                print('\nError: El ISBN ingresado no es valido ("numeros-numeros")\n')
                continue
            libro_encontrado = biblioteca.encontrar_libro(isbn)
            if libro_encontrado:
                print("\nYa existe un libro con esta ISBN\n")
                continue
            break
        while True:
            libros_existentes = pedir_input("Copias existentes del libro: ").strip()
            if not libros_existentes.isnumeric():
                print("\nError: El valor ingresado no es valido (solo numeros)\n")
                continue
            break
        libro = Libro(titulo,autor,isbn,int(libros_existentes),int(libros_existentes))
        return libro
    
    def registrar_usuario(self):
        while True:
            nombre = pedir_input("\nNombre y Apellido: ").strip().title()
            if not nombre.replace(" ","",1).isalpha() or not len(nombre.split()) == 2:
                print("\nError: El nombre entregado no es valido (nombre y apellido)")
                continue
            break
        while True:
            id_usuario = pedir_input("ID de usuario: ").strip()
            if not id_usuario.isnumeric():
                print("\nError: La ID de usuario entregado no es valida (solo numeros)\n")
                continue
            id_usuario = int(id_usuario)
            usuario_encontrado = self.encontrar_usuario(id_usuario)
            if usuario_encontrado:
                print("\nError: Ya existe un usuario con el mismo ID\n")
                continue
            break
        while True:
            edad = pedir_input("Edad del usuario: ").strip()
            if not edad.isnumeric():
                print("\nError: La edad entregada no es valida (solo numeros)\n")
                continue
            edad = int(edad)
            if edad <= 6 or edad > 99:
                print("\nError: El usuario tiene una edad no realista\n")
                continue
            elif edad >= 18:
                usuario = Usuario(nombre,id_usuario,edad,6)
            elif edad <= 17:
                usuario = Usuario(nombre,id_usuario,edad,3)
            break
        return usuario

    def prestar_libro(self,id_usuario):
        while True:
            if not id_usuario:
                usuario_id_o_nombre = pedir_input("\nIngresa el ID o Nombre del usuario: ").strip().title()
            usuario_encontrado = biblioteca.encontrar_usuario(usuario_id_o_nombre)
            if not usuario_encontrado:
                id_usuario = None
                print("\nError: Usuario no encontrado")
                continue
            print(f"\nUsuario seleccionado: {usuario_encontrado[1]} | {usuario_encontrado[0]}")
            if usuario_encontrado[3] == 0:
                print("\nError: Cantidad de prestamos maximos")
                id_usuario = None
                continue
            break
        while True:
            isbn = pedir_input("\nIngresa el ISBN o Nombre del libro: ")
            libro_encontrado = self.encontrar_libro(isbn)
            if not libro_encontrado:
                print("\nError: No existe libro con ese ISBN o Nombre")
                continue
            if not libro_encontrado[3]:
                print(f"\nError: No existen mas copias existentes del libro {libro_encontrado[1]}")
                continue
            with sqlite3.connect(ruta_final) as conn:
                cursor = conn.cursor()
                cursor.execute(QUERYS_CREAR_ORDEN["actualizar_Books"],(libro_encontrado[0],))
                cursor.execute(QUERYS_CREAR_ORDEN["actualizar_Users"],(usuario_encontrado[0],))
                cursor.execute(QUERYS_CREAR_ORDEN["crear_orden"],(libro_encontrado[0],usuario_encontrado[0]))
                conn.commit()
            print(f"\nEl libro {libro_encontrado[1]} fue obtenido")
            break
        
    def devolver_libro(self):
        while True:
            usuario_id_o_nombre = pedir_input("\nIngresa tu ID o Nombre de usuario: ").strip().title()
            usuario_encontrado = biblioteca.encontrar_usuario(usuario_id_o_nombre)
            if not usuario_encontrado:
                print("\nError: Usuario no encontrado")
                continue
            print(f"\nUsuario seleccionado: {usuario_encontrado[1]} | {usuario_encontrado[0]}")
            break
        while True:
            isbn_o_titulo = pedir_input("\nIngresa el ISBN o Nombre del libro: ").strip()
            libro_encontrado = biblioteca.encontrar_libro(isbn_o_titulo)
            if not libro_encontrado:
                print("\nError: No existe ningun libro con el ISBN o Nombre ingresado")
                continue
            print(f"\nLibro seleccionado: {libro_encontrado[1]}")
            with sqlite3.connect(ruta_final) as conn:
                orden_encontrada = conn.cursor().execute(QUERYS_ELIMINAR_ORDEN["encontrar_orden"],(usuario_encontrado[0],libro_encontrado[0])).fetchall()
                if not orden_encontrada:
                    print("\nError: No se le ha prestado este libro")
                    continue
                orden_encontrada = orden_encontrada[0]
                cursor = conn.cursor()
                cursor.execute(QUERYS_ELIMINAR_ORDEN["actualizar_Books"],(libro_encontrado[0],))
                cursor.execute(QUERYS_ELIMINAR_ORDEN["actualizar_Users"],(usuario_encontrado[0],))
                cursor.execute(QUERYS_ELIMINAR_ORDEN["eliminar_orden"],orden_encontrada)
                conn.commit()
                print(f'\nEl libro "{libro_encontrado[1]}" fue devuelto con exito')
                break
            
biblioteca = Biblioteca()

print("Bienvenido a la Biblioteca")
while True:        
    try:
        print("\n1)Libros")
        print("2)Usuarios")
        print("3)Pedir prestado un libro")
        print("4)Devolver un Libro prestado")

        entrada = input("Selecciona el numero de la opcion: ")
        #Libros
        if entrada == "1":
            while True:
                print("\n1)Registrar un Libro")
                print("2)Lista de todos los Libros")
                print("3)Editar un Libro")
                print("4)Eliminar un Libro")
                entrada = pedir_input("Selecciona el numero de la opcion: ")
                
                #Registrar un libro
                if entrada == "1":
                    libro = biblioteca.registrar_libro()
                    while True:
                        confirmacion = pedir_input("\n¿Estás seguro de añadir este libro? (y/n): ").lower()
                        if confirmacion == "y":
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERY_AGREGAR_LIBROS,(libro.isbn,libro.titulo,libro.autor,libro.libros_existentes,libro.libros_existentes))
                                conn.commit()
                            print(f"\nEl libro {libro.titulo} fue añadido con exito")
                        elif confirmacion == "n":
                            print("\nLibro no ha añadido")
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                        break
                    
                #Lista de los libros
                elif entrada == "2":
                    with sqlite3.connect(ruta_final) as conn:
                        cantidad_de_libros = conn.cursor().execute(QUERY_MOSTRAR_LIBROS).fetchall()
                    for libro in cantidad_de_libros:
                        print('\nLibro: '+libro[1])
                        print('Autor: '+libro[2])
                        print(f'Cantidad disponible: "{libro[3]}" de "{libro[4]}"')
                        print(f"ISBN: {libro[0]}")
                    break
                
                #Editar un libro
                elif entrada == "3":
                    print()
                    while True:
                        isbn_o_titulo = pedir_input("Ingresa el ISBN o Nombre del libro: ")
                        libro_a_editar = biblioteca.encontrar_libro(isbn_o_titulo)
                        if not libro_a_editar:
                            print("\nError: No existe libro con ese ISBN o Nombre\n")
                            continue
                        break
                    print(f"\nLibro seleccionado: {libro_a_editar[1]}")
                    while True:
                        print("\n1)Titulo")
                        print("2)Autor")
                        print("3)ISBN")
                        print("4)libros disponibles")
                        seleccion_a_editar = pedir_input("Selecciona que parte del libro quieres editar: ").lower()
                        
                        #Editar el titulo
                        if seleccion_a_editar == "1":
                            while True:
                                titulo_nuevo = pedir_input("\nTitulo nuevo: ")
                                if titulo_nuevo == libro_a_editar[1]:
                                    print("\nError: El titulo No Puede Ser Igual Que El Anterior")
                                    continue
                                if not titulo_nuevo:
                                    print("\nError: El titulo debe contener al menos un caracter")
                                    continue
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_LIBRO["Title"],(titulo_nuevo,libro_a_editar[0]))
                            print("\nTitulo del libro editado con exito")
                            
                        #Editar el autor
                        elif seleccion_a_editar == "2":
                            while True:
                                autor_nuevo = pedir_input("\nAutor nuevo: ")
                                if not autor_nuevo:
                                    print("\nError: El nuevo autor debe contener al menos un caracter")
                                    continue
                                if autor_nuevo == libro_a_editar[2]:
                                    print("\nError: El nuevo autor no puede ser igual que el anterior\n")
                                    continue
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_LIBRO["Autor"],(autor_nuevo,libro_a_editar[0]))
                            print("\nAutor del libro editado con exito")

                        #Editar el ISBN
                        elif seleccion_a_editar == "3":
                            if libro_a_editar[3] != libro_a_editar[4]:
                                print("\nError: No se puede cambiar el ISBN si hay algun libro prestado")
                                continue
                            while True:
                                nuevo_isbn = pedir_input("\nIngrese el nuevo ISBN: ")
                                if nuevo_isbn == libro_a_editar[0]:
                                    print("\nError: El nuevo ISBN no puede ser igual que el anterior")
                                    continue
                                if not nuevo_isbn.replace("-", "", 1).isnumeric() or not nuevo_isbn.count("-") == 1:
                                    print('\nError: El ISBN ingresado no es valido ("numeros-numeros")')
                                    continue
                                libro_encontrado = biblioteca.encontrar_libro(nuevo_isbn)
                                if libro_encontrado:
                                    print("\nYa existe un libro con esta ISBN")
                                    continue
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_LIBRO["BookID"],(nuevo_isbn,libro_a_editar[0]))
                            print("\nISBN del libro editado con exito")
                            
                        #Editar la cantidad de libros disponibles
                        elif seleccion_a_editar == "4":
                            cantidad_de_libros_cambiada = False
                            while not cantidad_de_libros_cambiada:
                                print(f"\nCantidad actual: {libro_a_editar[3]}")
                                nueva_cantidad = pedir_input("\nCantidad a sumar o restar: ").strip()
                                if not nueva_cantidad.isnumeric():
                                    print("\nError: La cantidad ingresada no es valida")
                                    continue
                                nueva_cantidad = int(nueva_cantidad)
                                while True:
                                    print("\n1)Sumar")
                                    print("2)Restar")
                                    print("3)Cambiar cantidad colocada")
                                    sumar_o_restar = pedir_input("Selecciona si quieres sumar o restar la cantidad: ")
                                    if sumar_o_restar == "1":
                                        with sqlite3.connect(ruta_final) as conn:
                                            conn.cursor().execute(QUERYS_ACTUALIZAR_LIBRO["SumExistingBooks"],(nueva_cantidad,nueva_cantidad,libro_a_editar[0]))
                                            conn.commit()
                                    elif sumar_o_restar == "2":
                                        if libro_a_editar[3] - nueva_cantidad < 0:
                                            print("\nError: Se ha eliminado mas libros de los que existian")
                                            break
                                        else:
                                            with sqlite3.connect(ruta_final) as conn:
                                                conn.cursor().execute(QUERYS_ACTUALIZAR_LIBRO["MinusExistingBooks"],(nueva_cantidad,nueva_cantidad,libro_a_editar[0]))
                                                conn.commit()
                                    elif sumar_o_restar == "3":
                                        break
                                    else:
                                        print("\nError: No se ha seleccionado una opcion valida")
                                        continue
                                    cantidad_de_libros_cambiada = True
                                    print("\nCantidad del libro editada con exito")
                                    break
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                        continue
                #Eliminar un libro
                elif entrada == "4":
                    biblioteca.eliminar_libro()
                
                else:
                    print("\nError: No se ha seleccionado una opcion valida")
                    continue
        #Usuarios
        elif entrada == "2":
            while True:
                print("\n1)Agregar un Usuario")
                print("2)Lista de los Usuario")
                print("3)Editar un Usuario")
                print("4)Eliminar un Usuario")
                entrada = pedir_input("Selecciona el numero de la opcion: ")
                
                #Agregar un usuario
                if entrada == "1":
                    usuario = biblioteca.registrar_usuario()
                    while True:
                        confirmacion = input("\n¿Estás seguro de añadir este usuario? (y/n): ").lower()
                        if confirmacion == "y":
                            try:
                                with sqlite3.connect(ruta_final) as conn:
                                    conn.cursor().execute(QUERY_AGREGAR_USUARIO,(usuario.id_usuario,usuario.nombre,usuario.edad,usuario.limite_de_libros))
                                    conn.commit()
                                print("\nUsuario añadido con exito")
                            except sqlite3.OperationalError as e:
                                if "locked" in str(e).lower():
                                    print("\nBase De Datos Bloqueada")
                        elif confirmacion == "n":
                            print("\nUsuario no añadido")
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                        break
                    if confirmacion == "y":
                        while True:
                            continuacion = input("\nDeseas pedir prestado un libro con este usuario? (y/n): ").lower()
                            if continuacion == "y":
                                biblioteca.prestar_libro(usuario.id_usuario)
                                break
                            elif continuacion == "n":
                                break
                            else:
                                print("\nError: No se ha seleccionado una opcion valida")
                            
                #Lista de los usuarios
                elif entrada == "2":
                    usuario_anterior = None
                    with sqlite3.connect(ruta_final) as conn:
                        lista_usuarios = conn.cursor().execute(QUERY_MOSTRAR_USUARIOS).fetchall()
                    for usuario in lista_usuarios:
                        if not usuario_anterior == usuario[0]:
                            print(f"\n{usuario[1]}\nSu ID es: {usuario[0]}\nTiene {usuario[2]} años de edad\nPuede pedir '{usuario[3]}' libros")
                        if usuario[4]:
                            print(f"Poseé el libro: {usuario[6]} '{usuario[4].count(",")+1}'\nHecho por: {usuario[7]} Pedido en la fecha: {usuario[4]}")
                        usuario_anterior = usuario[0]
                                    
                #Editar usuarios
                elif entrada == "3":
                    while True:
                        usuario_id_o_nombre = pedir_input("\nEscribe el ID o Nombre del usuario al cual desea editar: ").strip().title()
                        usuario_a_editar = biblioteca.encontrar_usuario(usuario_id_o_nombre)
                        if not usuario_a_editar:
                            print("\nError: Usuario no encontrado")
                            continue
                        break
                    print(f"\nUsuario seleccionado: {usuario_a_editar[1]} | {usuario_a_editar[0]}")
                    
                    while True:
                        print("\n1)Editar nombre de usuario")
                        print("2)Editar ID de usuario")
                        print("3)Editar edad de usuario")
                        entrada = pedir_input("Selecciona que parte del usuario quieres editar: ")
                    
                        #Editar el nombre del usuario
                        if entrada == "1":
                            while True:
                                nuevo_nombre = pedir_input("\nNuevo nombre y apellido del usuario: ").title()
                                if nuevo_nombre == usuario_a_editar[1]:
                                    print("\nError: El nuevo nombre del usuario no puede ser igual al actual")
                                    continue
                                if not nuevo_nombre.replace(" ","",1).isalpha() or not len(nuevo_nombre.split()) == 2:
                                    print("\nError: El nombre no es valido (nombre y apellido)")
                                    continue
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_USUARIO["Name"],(nuevo_nombre,usuario_a_editar[0],))
                                conn.commit()
                            print("\nNombre cambiado con exito")
                            
                        #Editar el ID del usuario
                        elif entrada == "2":
                            while True:
                                nuevo_id_usuario = pedir_input("\nNuevo numero ID de usuario: ").strip()
                                if not nuevo_id_usuario.isnumeric():
                                    print("\nError: La ID de usuario entregado no es valida (solo numeros)")
                                    continue
                                if nuevo_id_usuario == usuario_a_editar[0]:
                                    print("\nError: El nuevo ID del usuario no puede ser igual al actual")
                                    continue
                                usuario_encontrado = biblioteca.encontrar_usuario(nuevo_id_usuario)
                                if usuario_encontrado:
                                    print("\nError: Ya existe un usuario con la misma ID")
                                    continue
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_USUARIO["UserID"],(nuevo_id_usuario,usuario_a_editar[0],))
                                conn.commit()
                            print("\nID del usuario cambiada con exito")
                        
                        #Editar la edad del usuario
                        elif entrada == "3":
                            while True:
                                nueva_edad = pedir_input("\nNueva edad del usuario: ").strip()
                                if not nueva_edad.isnumeric():
                                    print("\nError: La edad ingresada no es valida (solo numeros)")
                                    continue
                                nueva_edad = int(nueva_edad)
                                if nueva_edad <= 6 or nueva_edad > 99:
                                    print("\nError: La Edad Del Usuario No Es Válida")
                                    continue
                                elif nueva_edad >= 18:
                                    nuevo_limite_de_libros = 6
                                elif nueva_edad <= 17:
                                    if usuario_a_editar[3] <= 3:
                                        print("\nError: El usuario sobrepasa el limite de libros para menores de edad")
                                        continue
                                    nuevo_limite_de_libros = 3
                                break
                            with sqlite3.connect(ruta_final) as conn:
                                conn.cursor().execute(QUERYS_ACTUALIZAR_USUARIO["Age"],(nueva_edad,nuevo_limite_de_libros,usuario_a_editar[0],))
                                conn.commit()
                            print("\nEdad editada con exito")
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                
                #Eliminar un usuario
                elif entrada == "4":
                    while True:
                        id_o_nombre_usuario_a_eliminar = pedir_input("\nID del usuario a eliminar: ").strip().title()
                        usuario_a_eliminar = biblioteca.encontrar_usuario(id_o_nombre_usuario_a_eliminar)
                        if not usuario_a_eliminar:
                            print("\nError: Usuario no encontrado")
                            continue
                        print(f"\nEl usuario seleccionado es: {usuario_a_eliminar[1]}")
                        if usuario_a_eliminar[3] == 0:
                            print("\nError: No se puede eliminar si tiene algun libro prestado")
                            break
                        while True:
                            confirmacion = input("\n¿Estás seguro de eliminar este usuario? (y/n): ").lower()
                            if confirmacion == "y":
                                with sqlite3.connect(ruta_final) as conn:
                                    conn.cursor().execute(QUERY_ELIMINAR_USUARIO,(usuario_a_eliminar[0],))
                                print("\nUsuario eliminado con exito")
                            elif confirmacion == "n":
                                print("\nUsuario no eliminado")
                            else:
                                print("\nError: No se ha seleccionado una opcion valida")
                                continue
                            break
                        break
                else:    
                    print("\nError: No se ha seleccionado una opcion valida")       
        elif entrada == "3":
                biblioteca.prestar_libro(None)
        elif entrada == "4":
                biblioteca.devolver_libro()
        elif entrada.lower() == "salir" or entrada.lower() == "0":
            break
        else:
            print("\nError: No se ha seleccionado una opcion valida")
    except SalirAlMenu:
        continue