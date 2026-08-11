import pandas as pd
import datetime
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
archivo_leido_libros = pd.read_csv(ruta_base+"\\Data\\libros.csv")
archivo_leido_usuarios = pd.read_csv(ruta_base+"\\Data\\usuarios.csv")

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
    def __init__(self,nombre,id_usuario,edad,libros_prestados,fecha_del_libro_prestado):
        self.nombre = nombre
        self.id_usuario = str(id_usuario)
        self.edad = edad
        self.libros_prestados = libros_prestados
        self.fecha_del_libro_prestado = fecha_del_libro_prestado
        
class MayorDeEdad(Usuario):
    def __init__(self, nombre, id_usuario, edad, libros_prestados, fecha_del_libro_prestado):
        super().__init__(nombre, id_usuario, edad, libros_prestados, fecha_del_libro_prestado)
        self.maximo_de_libros = 6
            
class MenorDeEdad(Usuario):
    def __init__(self, nombre, id_usuario, edad, libros_prestados, fecha_del_libro_prestado):
        super().__init__(nombre, id_usuario, edad, libros_prestados, fecha_del_libro_prestado)
        self.maximo_de_libros = 4
        
class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        
    def encontrar_usuario(self,usuario_o_id):
        usuario_encontrado_list = []
        if usuario_o_id.isnumeric():
            usuario_o_id = str(int(usuario_o_id))
            for usuario in self.usuarios:
                if usuario.id_usuario == usuario_o_id:
                    usuario_encontrado_list.append(usuario)
                    break
        else:
            for usuario in self.usuarios:
                if usuario.nombre.lower() == usuario_o_id.lower():
                    usuario_encontrado_list.append(usuario)
        if len(usuario_encontrado_list) > 1:
            x = 1
            print("\nSelecciona un Usuario:  ")
            for usuario_encontrado in usuario_encontrado_list:
                print(f"{x}) {usuario_encontrado.nombre}, {usuario_encontrado.id_usuario}")
                x += 1
            while True:
                numero_usuario = pedir_input("\nIngrese el numero: ")
                if not numero_usuario.isnumeric():
                    print("\nError: Opcion no encontrada")
                    continue
                numero_usuario = int(numero_usuario)
                if numero_usuario <= len(usuario_encontrado_list):
                    usuario_encontrado_list = usuario_encontrado_list[numero_usuario-1]
                    break
                print("\nError: Opcion no encontrada")
        else:
            if usuario_encontrado_list:
                usuario_encontrado_list = usuario_encontrado_list[0]
        return usuario_encontrado_list

    def encontrar_libro(self,isbn_o_titulo):
        libro_encontrado_list = []
        if isbn_o_titulo.count("-") == 1:
            for libro in self.libros:
                if libro.isbn == isbn_o_titulo:
                    libro_encontrado_list.append(libro)
        else:
            for libro in self.libros:
                if libro.titulo == isbn_o_titulo:
                    libro_encontrado_list.append(libro)
        if len(libro_encontrado_list) > 1:
            x = 1
            print("\nSelecciona un Libro:  ")
            for libro_encontrado in libro_encontrado_list:
                print(f"{x}) {libro_encontrado.titulo}, {libro_encontrado.autor}")
                x += 1
            while True:
                numero_libro = pedir_input("\nIngrese el numero: ")
                if not numero_libro.isnumeric():
                    print("\nError: Opcion no encontrada")
                    continue
                numero_libro = int(numero_libro)
                if numero_libro <= len(libro_encontrado_list):
                    libro_encontrado_list = libro_encontrado_list[numero_libro-1]
                    break
                print("\nError: Opcion no encontrada")
        else:
            if libro_encontrado_list:
                libro_encontrado_list = libro_encontrado_list[0]
        return libro_encontrado_list
    
    def eliminar_libro(self):
        global archivo_leido_libros
        while True:
            isbn = pedir_input("\nIngresa el ISBN o Nombre del libro: ")
            libro_encontrado = self.encontrar_libro(isbn)
            if not libro_encontrado:
                print("\nError: No existe un libro con ese ISBN")
                continue
            break
        print(f"\nLibro seleccionado: {libro_encontrado.titulo}")
        if libro_encontrado.libros_disponibles != libro_encontrado.libros_existentes:
            print("\nError: No se puede eliminar si hay al menos un libro prestado")
            return
        while True: 
            confirmacion = pedir_input("\n¿Estás seguro de eliminar este libro? (y/n): ").lower()
            if confirmacion == "y":
                archivo_leido_libros = archivo_leido_libros[archivo_leido_libros['isbn'] != libro_encontrado.isbn].reset_index(drop=True)
                archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                print(f"\nEl libro {libro_encontrado.titulo} fue eliminado con exito")
                self.libros.remove(libro_encontrado)
            elif confirmacion == "n":
                print("\nLibro no eliminado")
            else:
                print("\nError: No se ha seleccionado una opcion valida")
                continue
            break
                            
    def registrar_libro(self,libro):
        self.libros.append(libro)
        
    def agregar_usuarios_del_csv(self):
        cantidad_de_filas,x = archivo_leido_usuarios.shape
        for i in range(cantidad_de_filas):
            usuario_archivo = archivo_leido_usuarios.loc[i,:]
            if pd.isna(usuario_archivo.libros_prestados):
                libros_prestados = []
            else:
                libros_prestados = usuario_archivo.libros_prestados.split(",")
            if pd.isna(usuario_archivo.fecha_del_libro_prestado):
                fecha_del_libro_prestado = []
            else:
                fecha_del_libro_prestado = usuario_archivo.fecha_del_libro_prestado.split(",")
                
            if usuario_archivo.edad > 18:
                usuario = MayorDeEdad(usuario_archivo.nombre,usuario_archivo.id_usuario,usuario_archivo.edad,libros_prestados,fecha_del_libro_prestado)
            else:
                usuario = MenorDeEdad(usuario_archivo.nombre,usuario_archivo.id_usuario,usuario_archivo.edad,libros_prestados,fecha_del_libro_prestado)
            biblioteca.registrar_usuario(usuario)
    
    def peparar_usuario(self):
        global archivo_leido_usuarios
        while True:
            nombre = pedir_input("\nNombre y Apellido: ")
            if not nombre.replace(" ","",1).isalpha() or not len(nombre.split()) == 2:
                print("\nError: El nombre entregado no es valido (nombre y apellido)")
                continue
            break
        while True:
            id_usuario = pedir_input("ID de usuario: ")
            if not id_usuario.isnumeric():
                print("\nError: La ID de usuario entregado no es valida (solo numeros)\n")
                continue
            usuario_encontrado = self.encontrar_usuario(id_usuario)
            if usuario_encontrado:
                print("\nError: Ya existe un usuario con el mismo ID\n")
                continue
            break
        while True:
            edad = pedir_input("Edad del usuario: ")
            if not edad.isnumeric():
                print("\nError: La edad entregada no es valida (solo numeros)\n")
                continue
            id_usuario = int(id_usuario)
            edad = int(edad)
            libros_prestados = []
            fecha_del_libro_prestado = []
            if edad <= 10 or edad > 99:
                print("\nError: El usuario tiene una edad no realista\n")
                continue
            elif edad >= 18:
                usuario = MayorDeEdad(nombre.title(),id_usuario,edad,libros_prestados,fecha_del_libro_prestado)
            elif edad <= 17:
                usuario = MenorDeEdad(nombre.title(),id_usuario,edad,libros_prestados,fecha_del_libro_prestado)
            break
        while True:
            confirmacion = input("\n¿Estás seguro de añadir este usuario? (y/n): ").lower()
            if confirmacion == "y":
                biblioteca.registrar_usuario(usuario)
                biblioteca.usuarios.sort(key=lambda x : int(x.id_usuario))
                print("\nUsuario añadido con exito")
                usuario = {
                    'nombre' : nombre.title(),                
                    'id_usuario' : id_usuario,
                    'edad' : edad,
                    'libros_prestados' : None
                }
                usuario = pd.DataFrame([usuario])
                archivo_leido_usuarios = pd.concat([archivo_leido_usuarios, usuario])
                archivo_leido_usuarios = archivo_leido_usuarios.sort_values(by='id_usuario')
                archivo_leido_usuarios.to_csv("Data/usuarios.csv", index = False)
                return str(id_usuario)
            elif confirmacion == "n":
                print("\nUsuario no añadido")
            else:
                print("\nError: No se ha seleccionado una opcion valida")
                continue
            break
    
    def registrar_usuario(self,usuario):
        self.usuarios.append(usuario)

    def prestar_libro(self,id_usuario):
        global archivo_leido_usuarios
        global archivo_leido_libros
        while True:
            if not id_usuario:
                usuario_id_o_nombre = pedir_input("\nIngresa el ID o Nombre del usuario: ")
            usuario_encontrado = biblioteca.encontrar_usuario(usuario_id_o_nombre)
            if not usuario_encontrado:
                id_usuario = None
                print("\nError: Usuario no encontrado")
                continue
            print(f"\nUsuario seleccionado: {usuario_encontrado.nombre}, {usuario_encontrado.id_usuario}")
            if isinstance(usuario_encontrado,MenorDeEdad) and len(usuario_encontrado.libros_prestados) >= usuario_encontrado.maximo_de_libros or isinstance(usuario_encontrado,MayorDeEdad) and len(usuario_encontrado.libros_prestados) >= usuario_encontrado.maximo_de_libros:
                print("\nError: Cantidad de prestamos maximos")
                id_usuario = None
                continue
            break
        while True:
            isbn = pedir_input("\nIngresa el ISBN o Nombre del libro: ")
            libro_encontrado = self.encontrar_libro(isbn)
            if libro_encontrado == None:
                print("\nError: No existe libro con ese ISBN o Nombre")
                continue
            if not libro_encontrado.libros_disponibles:
                print(f"\nError: No existen mas copias existentes del libro {libro_encontrado.titulo}")
                continue
            
            now = datetime.datetime.now()
            fecha_de_libro_prestado = now.strftime("%d/%m %H:%M")
            
            archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_encontrado.isbn, 'libros_disponibles'] = int(libro_encontrado.libros_disponibles) - 1
            libro_encontrado.libros_disponibles = libro_encontrado.libros_disponibles - 1
            archivo_leido_libros.to_csv("Data/libros.csv",index = False)
            usuario_encontrado.libros_prestados.append(libro_encontrado.isbn)
            
            print(f"\nEl libro {libro_encontrado.titulo} fue obtenido")
            
            archivo_leido_usuarios['libros_prestados'] = archivo_leido_usuarios["libros_prestados"].astype(str)
            libros_actuales = archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'libros_prestados']
            if libros_actuales.empty or pd.isna(libros_actuales.values[0]) or libros_actuales.values[0] == "nan":
                libros_actuales = []
            else:
                libros_actuales = libros_actuales.values[0].split(',')
            libros_actuales.append(str(libro_encontrado.isbn))
            archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'libros_prestados']  =  ",".join(libros_actuales)
            
            archivo_leido_usuarios['fecha_del_libro_prestado'] = archivo_leido_usuarios["fecha_del_libro_prestado"].astype(str)
            fecha_de_los_libros_actuales = archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'fecha_del_libro_prestado']
            if fecha_de_los_libros_actuales.empty or pd.isna(fecha_de_los_libros_actuales.values[0]) or fecha_de_los_libros_actuales.values[0] == "nan":
                fecha_de_los_libros_actuales = []
            else:
                fecha_de_los_libros_actuales = fecha_de_los_libros_actuales.values[0].split(',')
            fecha_de_los_libros_actuales.append(fecha_de_libro_prestado)
            usuario_encontrado.fecha_del_libro_prestado.append(str(fecha_de_libro_prestado))
            archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'fecha_del_libro_prestado']  =  ",".join(fecha_de_los_libros_actuales)
            archivo_leido_usuarios.to_csv("Data/usuarios.csv",index = False)
            break
        
    def devolver_libro(self):
        while True:
            usuario_id_o_nombre = pedir_input("\nIngresa tu ID o Nombre de usuario: ")
            usuario_encontrado = biblioteca.encontrar_usuario(usuario_id_o_nombre)
            if not usuario_encontrado:
                print("\nError: Usuario no encontrado")
                continue
            elif not usuario_encontrado.libros_prestados:
                print(f"\nUsuario seleccionado: {usuario_encontrado.nombre}, {usuario_encontrado.id_usuario}")
                print("\nError: No se le ha prestado ningun libro a este usuario")
                continue
            print(f"\nUsuario seleccionado: {usuario_encontrado.nombre}, {usuario_encontrado.id_usuario}")
            break
        while True:
            isbn = pedir_input("\nIngresa el ISBN o Nombre del libro: ")
            libro_encontrado = biblioteca.encontrar_libro(isbn)
            if not libro_encontrado:
                print("\nError: No existe ningun libro con el ISBN o Nombre ingresado")
                continue
            if not usuario_encontrado.libros_prestados:
                print("\nError: No se le ha prestado ningun libro al usuario")
                continue
            print(f"\nLibro seleccionado: {libro_encontrado.titulo}")
            num = 0
            for i in usuario_encontrado.libros_prestados:
                if i == libro_encontrado.isbn:
                    archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_encontrado.isbn, 'libros_disponibles'] = libro_encontrado.libros_disponibles + 1
                    libro_encontrado.libros_disponibles += 1
                    usuario_encontrado.libros_prestados.remove(libro_encontrado.isbn)
                    archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                    
                    print(f'\nEl libro "{libro_encontrado.titulo}" fue devuelto con exito')
                    
                    libros_actuales = archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'libros_prestados']
                    libros_actuales = libros_actuales.values[0].split(',')
                    libros_actuales.remove(str(libro_encontrado.isbn))
                    archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'libros_prestados'] = ",".join(libros_actuales)
                    
                    fechas_actuales = archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'fecha_del_libro_prestado']
                    fechas_actuales = fechas_actuales.values[0].split(',')
                    fechas_actuales.remove(fechas_actuales[num])
                    usuario_encontrado.fecha_del_libro_prestado = fechas_actuales
                    archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_encontrado.id_usuario), 'fecha_del_libro_prestado'] = ",".join(fechas_actuales)
                    archivo_leido_usuarios.to_csv("Data/usuarios.csv",index = False)
                    raise SalirAlMenu
                num += 1
            print("\nError: No se le ha prestado este libro")
        
            
biblioteca = Biblioteca()

cantidad_de_filas,x = archivo_leido_libros.shape
for i in range(cantidad_de_filas):
    libro = archivo_leido_libros.loc[i,:]
    biblioteca.registrar_libro(Libro(libro.titulo,libro.autor,libro.isbn,libro.libros_disponibles,libro.libros_existentes))

biblioteca.agregar_usuarios_del_csv()

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
                    while True:
                        titulo = pedir_input("\nTítulo del libro: ")
                        if titulo:
                            break
                        print("\nError: El titulo debe contener al menos un caracter")
                    while True:
                        autor = pedir_input("Autor: ")
                        if autor:
                            break
                        print("\nError: El autor debe contener al menos un caracter\n")
                    while True:
                        isbn = pedir_input("Ingresa el ISBN del libro: ")
                        if not isbn.replace("-", "", 1).isnumeric() or not isbn.count("-") == 1:
                            print('\nError: El ISBN ingresado no es valido ("numeros-numeros")\n')
                            continue
                        libro_encontrado = biblioteca.encontrar_libro(isbn)
                        if libro_encontrado:
                            print("\nYa existe un libro con esta ISBN\n")
                            continue
                        break
                    while True:
                        libros_existentes = pedir_input("Copias existentes del libro: ")
                        if not libros_existentes.isnumeric():
                            print("\nError: El valor ingresado no es valido (solo numeros)\n")
                            continue
                        break
                    while True:
                        confirmacion = pedir_input("\n¿Estás seguro de añadir este libro? (y/n): ").lower()
                        if confirmacion == "y":
                            libro = Libro(titulo,autor,isbn,int(libros_existentes),int(libros_existentes))
                            biblioteca.registrar_libro(libro)
                            biblioteca.libros.sort(key=lambda x : x.titulo)
                            libro = {
                                'titulo' : titulo,                
                                'autor' : autor,
                                'isbn' : isbn,
                                'libros_disponibles' : libros_existentes,
                                'libros_existentes' : libros_existentes
                            }
                            libro = pd.DataFrame([libro])
                            archivo_leido_libros = pd.concat([archivo_leido_libros, libro])
                            archivo_leido_libros.sort_values(by='titulo')
                            archivo_leido_libros.to_csv("Data/libros.csv", index = False)
                            print(f"\nEl libro {titulo} fue añadido con exito")
                        elif confirmacion == "n":
                            print("\nLibro no ha añadido")
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                        break
                    
                #Lista de los libros
                elif entrada == "2":
                    for cantidad_de_libros in biblioteca.libros:
                        print('\nLibro: '+cantidad_de_libros.titulo)
                        print('Autor: '+cantidad_de_libros.autor)
                        print(f'Cantidad disponible: "{cantidad_de_libros.libros_disponibles}" de "{cantidad_de_libros.libros_existentes}"')
                        print(f"ISBN: {cantidad_de_libros.isbn}")
                    break
                
                #Editar un libro
                elif entrada == "3":
                    print()
                    while True:
                        isbn = pedir_input("Ingresa el ISBN o Nombre del libro: ")
                        libro_a_editar = biblioteca.encontrar_libro(isbn)
                        if not libro_a_editar:
                            print("\nError: No existe libro con ese ISBN o Nombre\n")
                            continue
                        break
                    print(f"\nLibro seleccionado: {libro_a_editar.titulo}")
                    while True:
                        print("\n1)Titulo")
                        print("2)Autor")
                        print("3)ISBN")
                        print("4)libros disponibles")
                        seleccion_a_editar = pedir_input("Selecciona que parte del libro quieres editar: ").lower()
                        
                        #Editar el titulo
                        if seleccion_a_editar == "1":
                            while True:
                                titulo_a_editar_encontrado = None
                                titulo_nuevo = pedir_input("\nTitulo nuevo: ")
                                if not titulo_nuevo:
                                    print("\nError: El titulo debe contener al menos un caracter")
                                    continue
                                for libro in biblioteca.libros:
                                    if libro.titulo == titulo_nuevo:
                                        titulo_a_editar = titulo_nuevo
                                        print("\nError: Ya existe un libro con el mismo titulo")
                                        break
                                if titulo_a_editar_encontrado:
                                    continue
                                break
                            archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'titulo'] = titulo_nuevo
                            archivo_leido_libros = archivo_leido_libros.sort_values(by='titulo')
                            archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                            libro_a_editar.titulo = titulo_nuevo
                            print("\nTitulo del libro editado con exito")
                            biblioteca.libros.sort(key=lambda x : x.titulo)
                            
                        #Editar el autor
                        elif seleccion_a_editar == "2":
                            while True:
                                autor_nuevo = pedir_input("\nAutor nuevo: ")
                                if not autor_nuevo:
                                    print("\nError: El nuevo autor debe contener al menos un caracter")
                                    continue
                                if autor_nuevo == libro_a_editar.autor:
                                    print("\nError: El nuevo autor no puede ser igual que el anterior\n")
                                    continue
                                break
                            archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'autor'] = autor_nuevo
                            archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                            libro_a_editar.autor = autor_nuevo
                            print("\nAutor del libro editado con exito")
                            
                        #Editar el ISBN
                        elif seleccion_a_editar == "3":
                            if libro_a_editar.libros_disponibles != libro_a_editar.libros_existentes:
                                print("\nError: No se puede cambiar el ISBN si hay algun libro prestado")
                                continue
                            while True:
                                nuevo_isbn = pedir_input("\nIngrese el nuevo ISBN: ")
                                if nuevo_isbn == libro_a_editar.isbn:
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
                            archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'isbn'] = nuevo_isbn
                            archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                            libro_a_editar.isbn = nuevo_isbn
                            print("\nISBN del libro editado con exito")
                            
                        #Editar la cantidad de libros disponibles
                        elif seleccion_a_editar == "4":
                            cantidad_de_libros_cambiada = False
                            while not cantidad_de_libros_cambiada:
                                print(f"\nCantidad actual: {libro_a_editar.libros_disponibles}")
                                nuevo_libros_disponibles = pedir_input("\nCantidad a sumar o restar: ")
                                if not nuevo_libros_disponibles.isnumeric():
                                    print("\nError: La cantidad ingresada no es valida")
                                    continue
                                nuevo_libros_disponibles = int(nuevo_libros_disponibles)
                                while True:
                                    print("\n1)Sumar")
                                    print("2)Restar")
                                    print("3)Cambiar cantidad colocada")
                                    sumar_o_restar = pedir_input("Selecciona si quieres sumar o restar la cantidad: ")
                                    if sumar_o_restar == "1":
                                        archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'libros_disponibles'] = int(libro_a_editar.libros_disponibles) + nuevo_libros_disponibles
                                        archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'libros_existentes'] = int(libro_a_editar.libros_existentes) + nuevo_libros_disponibles
                                        archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                                        libro_a_editar.libros_disponibles = int(libro_a_editar.libros_disponibles) + nuevo_libros_disponibles
                                        libro_a_editar.libros_existentes = int(libro_a_editar.libros_existentes) + nuevo_libros_disponibles
                                    elif sumar_o_restar == "2":
                                        if int(libro_a_editar.libros_disponibles) - int(nuevo_libros_disponibles) < 0:
                                            print("\nError: Se ha eliminado mas libros de los que existian")
                                            break
                                        archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'libros_disponibles'] = int(libro_a_editar.libros_disponibles) - nuevo_libros_disponibles
                                        archivo_leido_libros.loc[archivo_leido_libros['isbn'] == libro_a_editar.isbn, 'libros_existentes'] = int(libro_a_editar.libros_existentes) - nuevo_libros_disponibles
                                        archivo_leido_libros.to_csv("Data/libros.csv",index = False)
                                        libro_a_editar.libros_disponibles = int(libro_a_editar.libros_disponibles) - nuevo_libros_disponibles
                                        libro_a_editar.libros_existentes = int(libro_a_editar.libros_existentes) - nuevo_libros_disponibles
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
                    id_usuario = biblioteca.peparar_usuario()
                    if id_usuario:
                        while True:
                            continuacion = input("\nDeseas pedir prestado un libro con este usuario? (y/n): ").lower()
                            if continuacion == "y":
                                biblioteca.prestar_libro(id_usuario)
                                break
                            elif continuacion == "n":
                                break
                            else:
                                print("\nError: No se ha seleccionado una opcion valida")
                            
                #Lista de los usuarios
                elif entrada == "2":
                    for cantidad_de_usuarios in biblioteca.usuarios:
                        print(f"\n{cantidad_de_usuarios.nombre}\nSu ID es: {cantidad_de_usuarios.id_usuario}\nTiene {cantidad_de_usuarios.edad} años de edad")
                        if cantidad_de_usuarios.libros_prestados:
                            titulos_y_indices = {}
                            for idx, isbn in enumerate(cantidad_de_usuarios.libros_prestados):
                                for libro in biblioteca.libros:
                                    if isbn == libro.isbn:
                                        if libro.titulo not in titulos_y_indices:
                                            titulos_y_indices[libro.titulo] = []
                                        titulos_y_indices[libro.titulo].append(idx)
                            for titulo, indices in titulos_y_indices.items():
                                fechas_a_mostrar = [cantidad_de_usuarios.fecha_del_libro_prestado[i] for i in indices]
                                print(f"Libro prestado: {titulo}, '{len(indices)}', {fechas_a_mostrar}")
                                    
                #Editar usuarios
                elif entrada == "3":
                    while True:
                        usuario_id_o_nombre = pedir_input("\nEscribe el ID o Nombre del usuario al cual desea editar: ")
                        usuario_a_editar = biblioteca.encontrar_usuario(usuario_id_o_nombre)
                        if not usuario_a_editar:
                            print("\nError: Usuario no encontrado")
                            continue
                        break
                    print(f"\nUsuario seleccionado: {usuario_a_editar.nombre},{usuario_a_editar.id_usuario}")
                    
                    while True:
                        print("\n1)Editar nombre de usuario")
                        print("2)Editar ID de usuario")
                        print("3)Editar edad de usuario")
                        entrada = pedir_input("Selecciona que parte del usuario quieres editar: ")
                    
                        #Editar el nombre del usuario
                        if entrada == "1":
                            while True:
                                nuevo_nombre = pedir_input("\nNuevo nombre y apellido del usuario: ")
                                if nuevo_nombre == usuario_a_editar.nombre:
                                    print("\nError: El nuevo nombre del usuario no puede ser igual al actual")
                                    continue
                                if not nuevo_nombre.replace(" ","",1).isalpha() or not len(nuevo_nombre.split()) == 2:
                                    print("\nError: El nombre no es valido (nombre y apellido)")
                                    continue
                                break
                            archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_a_editar.id_usuario),'nombre'] = nuevo_nombre.title()
                            archivo_leido_usuarios.to_csv("Data/usuarios.csv",index=False)
                            usuario_a_editar.nombre = nuevo_nombre.title()
                            print("\nNombre cambiado con exito")
                            
                        #Editar el ID del usuario
                        elif entrada == "2":
                            while True:
                                nuevo_id_usuario = pedir_input("\nNuevo numero ID de usuario: ")
                                if not nuevo_id_usuario.isnumeric():
                                    print("\nError: La ID de usuario entregado no es valida (solo numeros)")
                                    continue
                                if str(int(nuevo_id_usuario)) == usuario_a_editar.id_usuario:
                                    print("\nError: El nuevo ID del usuario no puede ser igual al actual")
                                    continue
                                usuario_encontrado = biblioteca.encontrar_usuario(nuevo_id_usuario)
                                if usuario_encontrado:
                                    print("\nError: Ya existe un usuario con la misma ID")
                                    continue
                                break
                            archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_a_editar.id_usuario),'id_usuario'] = int(nuevo_id_usuario)
                            archivo_leido_usuarios = archivo_leido_usuarios.sort_values(by='id_usuario')
                            archivo_leido_usuarios.to_csv("Data/usuarios.csv",index=False)
                            usuario_a_editar.id_usuario = str(int(nuevo_id_usuario))
                            biblioteca.usuarios.sort(key=lambda x : int(x.id_usuario))
                            print("\nID del usuario cambiada con exito")
                        
                        #Editar la edad del usuario
                        elif entrada == "3":
                            while True:
                                nueva_edad = pedir_input("\nNueva edad del usuario: ")
                                if not nueva_edad.isnumeric():
                                    print("\nError: La edad ingresada no es valida (solo numeros)")
                                    continue
                                nueva_edad = int(nueva_edad)
                                if nueva_edad <= 10 or nueva_edad > 99:
                                    print("\nError: El usuario debe tener mas edad")
                                    continue
                                elif nueva_edad >= 18:
                                    usuario_a_editar_edad_cambiada = MayorDeEdad(usuario_a_editar.nombre,usuario_a_editar.id_usuario,nueva_edad,usuario_a_editar.libros_prestados,usuario_a_editar.fecha_del_libro_prestado)
                                elif nueva_edad <= 17:
                                    if len(usuario_a_editar.libros_prestados) >= 4:
                                        print("\nError: El usuario sobrepasa el limite de libros para menores de edad")
                                        continue
                                    usuario_a_editar_edad_cambiada = MenorDeEdad(usuario_a_editar.nombre,usuario_a_editar.id_usuario,nueva_edad,usuario_a_editar.libros_prestados,usuario_a_editar.fecha_del_libro_prestado)
                                break
                            archivo_leido_usuarios.loc[archivo_leido_usuarios['id_usuario'] == int(usuario_a_editar.id_usuario),'edad'] = nueva_edad
                            archivo_leido_usuarios.to_csv("Data/usuarios.csv",index=False)
                            biblioteca.usuarios.remove(usuario_a_editar)
                            biblioteca.usuarios.append(usuario_a_editar_edad_cambiada)
                            biblioteca.usuarios.sort(key=lambda x : int(x.id_usuario))
                            usuario_a_editar = usuario_a_editar_edad_cambiada
                            print("\nEdad editada con exito")
                        else:
                            print("\nError: No se ha seleccionado una opcion valida")
                            continue
                
                #Eliminar un usuario
                elif entrada == "4":
                    while True:
                        id_o_nombre_usuario_a_eliminar = pedir_input("\nID del usuario a eliminar: ")
                        usuario_a_eliminar = biblioteca.encontrar_usuario(id_o_nombre_usuario_a_eliminar)
                        if not usuario_a_eliminar:
                            print("\nError: Usuario no encontrado")
                            continue
                        print(f"\nEl usuario seleccionado es: {usuario_a_eliminar.nombre}")
                        if usuario_a_eliminar.libros_prestados:
                            print("\nError: No se puede eliminar que tenga algun libro prestado")
                            break
                        while True: 
                            confirmacion = input("\n¿Estás seguro de eliminar este usuario? (y/n): ").lower()
                            if confirmacion == "y":
                                archivo_leido_usuarios = archivo_leido_usuarios[archivo_leido_usuarios['id_usuario'] != int(usuario_a_eliminar.id_usuario)].reset_index(drop=True)
                                archivo_leido_usuarios.to_csv("Data/usuarios.csv",index=False)
                                biblioteca.usuarios.remove(usuario_a_eliminar)
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