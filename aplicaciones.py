import time
import datetime

class Aplicacion:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def mostrar_menu(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    def ejecutar_menu(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")


class Spotify(Aplicacion):
    def __init__(self):
        self.nombre = 'Spotify'
        self.canciones = {}
        self.playlists = {}
        self.cancion_actual = None

    # Agregar nueva canción a tu biblioteca
    def agregar_cancion(self, id_cancion, nombre_cancion, artista):
        if id_cancion not in self.canciones:
            self.canciones[id_cancion] = {'nombre': nombre_cancion, 'artista': artista}
            print(f'Canción "{nombre_cancion}" de {artista} agregada.')
        else:
            print('El ID de la canción ya existe.')

    # Eliminar canción de tu biblioteca
    def eliminar_cancion(self, id_cancion):
        if id_cancion in self.canciones:
            cancion = self.canciones.pop(id_cancion)
            print(f'Canción "{cancion["nombre"]}" de {cancion["artista"]} eliminada.')
        else:
            print('ID de canción no encontrado.')

    # Crear una playlist
    def crear_playlist(self, nombre_playlist):
        if nombre_playlist not in self.playlists:
            self.playlists[nombre_playlist] = []
            print(f'Playlist "{nombre_playlist}" creada.')
        else:
            print(f'Error: ya existe una playlist con el nombre "{nombre_playlist}".')

    # Agregar canción a una playlist
    def agregar_cancion_a_playlist(self, nombre_playlist, id_cancion):
        if nombre_playlist not in self.playlists:
            print(f'Error: la playlist "{nombre_playlist}" no existe.')
            return
        if id_cancion not in self.canciones:
            print(f'Error: la canción con ID {id_cancion} no existe.')
            return
        # Verifica si la canción ya está en la playlist
        if self.canciones[id_cancion] not in self.playlists[nombre_playlist]:
            self.playlists[nombre_playlist].append(self.canciones[id_cancion])
            print(f'Canción "{self.canciones[id_cancion]["nombre"]}" agregada a la playlist "{nombre_playlist}".')
        else:
            print(f'La canción ya está en la playlist "{nombre_playlist}".')

    # Eliminar canción de una playlist
    def eliminar_cancion_de_playlist(self, nombre_playlist, id_cancion):
        if nombre_playlist not in self.playlists:
            print(f'Error: la playlist "{nombre_playlist}" no existe.')
            return
        if id_cancion not in self.canciones:
            print(f'Error: la canción con ID {id_cancion} no existe.')
            return

        if self.canciones[id_cancion] in self.playlists[nombre_playlist]:
            self.playlists[nombre_playlist].remove(self.canciones[id_cancion])
            print(f'Canción "{self.canciones[id_cancion]["nombre"]}" eliminada de la playlist "{nombre_playlist}".')
        else:
            print(f'La canción no está en la playlist "{nombre_playlist}".')

    # Reproducir canción
    def reproducir_cancion(self, id_cancion):
        if id_cancion in self.canciones:
            self.cancion_actual = self.canciones[id_cancion]
            print(f'Reproduciendo "{self.cancion_actual["nombre"]}" de {self.cancion_actual["artista"]}.')
        else:
            print('ID de canción no encontrado.')

    # Pausa la canción actual
    def pausar_cancion(self):
        if self.cancion_actual:
            print(f'Canción "{self.cancion_actual["nombre"]}" de {self.cancion_actual["artista"]} pausada.')
            self.cancion_actual = None
        else:
            print('No hay ninguna canción en reproducción.')

    # Nombra todas las canciones de la biblioteca
    def listar_canciones(self):
        if self.canciones:
            for id_cancion, detalles in self.canciones.items():
                print(f'ID: {id_cancion}, Nombre: "{detalles["nombre"]}", Artista: {detalles["artista"]}')
        else:
            print("No tienes canciones en tu biblioteca.")

    # Enumera todas las playlists
    def listar_playlists(self):
        if self.playlists:
            for nombre_lista, canciones in self.playlists.items():
                canciones_nombres = [cancion["nombre"] for cancion in canciones]
                print(f'Playlist: {nombre_lista}, Canciones: {", ".join(canciones_nombres)}')
        else:
            print("No tienes playlists.")

    @staticmethod
    def mostrar_menu():
        print("\nMenú de Spotify")
        print("1. Agregar canción")
        print("2. Eliminar canción")
        print("3. Crear Playlist")
        print("4. Agregar canción a Playlist")
        print("5. Eliminar canción de Playlist")
        print("6. Reproducir canción")
        print("7. Pausar canción")
        print("8. Listar canciones")
        print("9. Listar Playlists")
        print("10. Salir")

    def ejecutar_menu(self):
        while True:
            try:
                self.mostrar_menu()
                opcion = int(input("Elija una opción: "))
                if opcion == 1:
                    id_cancion = int(input("ID de la canción: "))
                    nombre_cancion = input("Nombre de la canción: ").strip()
                    artista = input("Artista: ").strip()
                    if nombre_cancion and artista:
                        self.agregar_cancion(id_cancion, nombre_cancion, artista)
                    else:
                        print("El nombre de la canción y el artista no pueden estar vacíos.")
                elif opcion == 2:
                    id_cancion = int(input("ID de la canción a eliminar: "))
                    self.eliminar_cancion(id_cancion)
                elif opcion == 3:
                    nombre_lista = input("Nombre de la lista de reproducción: ").strip()
                    if nombre_lista:
                        self.crear_playlist(nombre_lista)
                    else:
                        print("El nombre de la lista de reproducción no puede estar vacío.")
                elif opcion == 4:
                    nombre_lista = input("Nombre de la lista de reproducción: ").strip()
                    id_cancion = int(input("ID de la canción: "))
                    self.agregar_cancion_a_playlist(nombre_lista, id_cancion)
                elif opcion == 5:
                    nombre_lista = input("Nombre de la lista de reproducción: ").strip()
                    id_cancion = int(input("ID de la canción: "))
                    self.eliminar_cancion_de_playlist(nombre_lista, id_cancion)
                elif opcion == 6:
                    id_cancion = int(input("ID de la canción a reproducir: "))
                    self.reproducir_cancion(id_cancion)
                elif opcion == 7:
                    self.pausar_cancion()
                elif opcion == 8:
                    self.listar_canciones()
                elif opcion == 9:
                    self.listar_playlists()
                elif opcion == 10:
                    print("Saliendo del programa...")
                    break  # Salir del bucle  
                else:
                    print("Opción no válida, por favor intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")


# App de libros
class Goodreads(Aplicacion):
    def __init__(self):
        self.nombre = 'Goodreads'
        self.libros = []

    def agregar_libro(self, titulo, autor, año, genero):
        libro = {
            'titulo': titulo,
            'autor': autor,
            'año': año,
            'genero': genero,
            'calificacion': None,
            'resena': None
        }
        self.libros.append(libro)
        print(f'Libro "{titulo}" de {autor} agregado.')

    def calificar_libro(self, titulo, calificacion):
        if not (1 <= calificacion <= 5):  # Validación de la calificación
            print("La calificación debe estar entre 1 y 5 estrellas.")
            return
        for libro in self.libros:
            if libro['titulo'] == titulo:
                libro['calificacion'] = calificacion
                print(f'Libro "{titulo}" calificado con {calificacion} estrellas.')
                return
        print(f'Libro "{titulo}" no encontrado.')

    def agregar_resena(self, titulo, resena):
        for libro in self.libros:
            if libro['titulo'] == titulo:
                libro['resena'] = resena
                print(f'Reseña agregada al libro "{titulo}".')
                return
        print(f'Libro "{titulo}" no encontrado.')

    def listar_libros(self):
        if not self.libros:
            print('No hay libros registrados.')
            return
        for libro in self.libros:
            print(f'Título: {libro["titulo"]}, Autor: {libro["autor"]}, Año: {libro["año"]}, Género: {libro["genero"]}')
            if libro['calificacion'] is not None:
                print(f'  Calificación: {libro["calificacion"]} estrellas')
            if libro['resena']:
                print(f'  Reseña: {libro["resena"]}')
            print('---')

    @staticmethod
    def mostrar_menu():
        print("\nMenú de Goodreads")
        print("1. Agregar libro")
        print("2. Calificar libro")
        print("3. Agregar reseña")
        print("4. Listar libros")
        print("5. Salir")

    def ejecutar_menu(self):
        opcion = 0
        while opcion != 5:
            self.mostrar_menu()
            try:
                opcion = int(input("Elija una opción: "))

                if opcion == 1:
                    titulo = input("Título del libro: ")
                    while not titulo.strip():  # Validar que no esté vacío
                        print("El título no puede estar vacío.")
                        titulo = input("Título del libro: ")

                    autor = input("Autor del libro: ")
                    while not autor.strip():  # Validar que no esté vacío
                        print("El autor no puede estar vacío.")
                        autor = input("Autor del libro: ")

                    while True:  # Validación del año de publicación
                        try:
                            año = int(input("Año de publicación: "))
                            if año < 0 or año > datetime.datetime.now().year:  
                                print("Por favor ingrese un año razonable.")
                            else:
                                break
                        except ValueError:
                            print("Por favor ingrese un año válido (número).")
                    
                    genero = input("Género del libro: ")
                    while not genero.strip():  
                        print("El género no puede estar vacío.")
                        genero = input("Género del libro: ")

                    self.agregar_libro(titulo, autor, año, genero)

                elif opcion == 2:
                    titulo = input("Título del libro a calificar: ")
                    while not titulo.strip(): 
                        print("El título no puede estar vacío.")
                        titulo = input("Título del libro a calificar: ")

                    while True:
                        try:
                            calificacion = float(input("Calificación (de 1 a 5 estrellas): "))
                            if 1 <= calificacion <= 5:
                                break
                            else:
                                print("La calificación debe estar entre 1 y 5.")
                        except ValueError:
                            print("Por favor ingrese una calificación válida (número).")
                    self.calificar_libro(titulo, calificacion)

                elif opcion == 3:
                    titulo = input("Título del libro para agregar reseña: ")
                    while not titulo.strip(): 
                        print("El título no puede estar vacío.")
                        titulo = input("Título del libro para agregar reseña: ")

                    resena = input("Escribe tu reseña: ")
                    while not resena.strip():  
                        print("La reseña no puede estar vacía.")
                        resena = input("Escribe tu reseña: ")

                    self.agregar_resena(titulo, resena)

                elif opcion == 4:
                    self.listar_libros()

                elif opcion == 5:
                    print("Saliendo del programa...")

                else:
                    print("Opción no válida, por favor intente de nuevo.")

            except ValueError:
                print("Por favor ingrese un número válido para la opción del menú.")


class Calculadora(Aplicacion):
    def __init__(self):
        self.nombre='Calculadora'
        
    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Error: División por cero"
        
    @staticmethod
    def mostrar_menu():
        print("\n--- Calculadora Menu ---")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Salir")
        
    def ingresar_numero(self, mensaje):
        while True:
            try:
                numero = float(input(mensaje))
                return numero
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
    def ejecutar_menu(self):
        continuar = True
        while continuar:
            self.mostrar_menu()
            choice = input("Elige una opción: ")

            if choice == '1':
                a = self.ingresar_numero("Primer número: ")
                b = self.ingresar_numero("Segundo número: ")
                print(f"Resultado: {self.sumar(a, b)}")
            elif choice == '2':
                a = self.ingresar_numero("Primer número: ")
                b = self.ingresar_numero("Segundo número: ")
                print(f"Resultado: {self.restar(a, b)}")
            elif choice == '3':
                a = self.ingresar_numero("Primer número: ")
                b = self.ingresar_numero("Segundo número: ")
                print(f"Resultado: {self.multiplicar(a, b)}")
            elif choice == '4':
                a = self.ingresar_numero("Primer número: ")
                b = self.ingresar_numero("Segundo número: ")
                print(f"Resultado: {self.dividir(a, b)}")
            elif choice == '5':
                print("Saliendo de Calculadora")
                continuar = False
            else:
                print("Opción inválida, intente nuevamente.")


class Reloj(Aplicacion):
    def __init__(self):
        self.nombre = 'Reloj'
        self.timer_iniciado = False
        self.inicio_timer = None

    # Muestra la hora actual en formato de 24Hs o 12Hs
    def mostrar_hora(self, formato_24h=True):
        ahora = datetime.datetime.now()
        if formato_24h:
            hora_actual = ahora.strftime("%H:%M:%S")
        else:
            hora_actual = ahora.strftime("%I:%M:%S %p")  # 12h
        print(f"Hora actual: {hora_actual}")
    
    def iniciar_timer(self):
        if self.timer_iniciado:
            print("El timer ya está en marcha, debe pararlo antes de empezar uno nuevo.")
        else:
            self.inicio_timer = time.time()
            self.timer_iniciado = True
            print("Timer iniciado.")

    # Para el timer y muestra el tiempo contado
    def parar_timer(self):
        if not self.timer_iniciado:
            print("El temporizador no ha sido iniciado.")
        else:
            tiempo_transcurrido = time.time() - self.inicio_timer
            self.timer_iniciado = False
            print(f"Temporizador detenido. Tiempo transcurrido: {self.formatear_tiempo(tiempo_transcurrido)}")

    # Convierte el tiempo en segundos a formato minutos y segundos
    def formatear_tiempo(self, tiempo_segundos):
        minutos = int(tiempo_segundos // 60)
        segundos = int(tiempo_segundos % 60)
        return f"{minutos} min {segundos} seg"

    def mostrar_menu(self):
        print("\n--- Menú del Reloj ---")
        print("1. Mostrar hora actual")
        print("2. Iniciar Timer")
        print("3. Detener Timer")
        print("4. Salir")
    
    def ingresar_opcion(self):
        while True:
            try:
                opcion = int(input("Elija una opción: "))
                if opcion in [1, 2, 3, 4]:
                    return opcion
                else:
                    print("Opción no válida. Debe ser 1, 2, 3 o 4.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
    def ejecutar_menu(self):
        opcion = 0
        while opcion != 4:
            self.mostrar_menu()
            opcion = self.ingresar_opcion()

            if opcion == 1:
                formato = input("¿Mostrar hora en formato 24h o 12h? (24/12): ").strip()
                if formato == '12':
                    self.mostrar_hora(formato_24h=False)
                elif formato == '24':
                    self.mostrar_hora(formato_24h=True)
                else:
                    print("Formato no válido. Mostrando en formato 24h por defecto.")
                    self.mostrar_hora(formato_24h=True)
            elif opcion == 2:
                self.iniciar_timer()
            elif opcion == 3:
                self.parar_timer()
            elif opcion == 4:
                print("Saliendo del programa...")
            else:
                print("Opción no válida, por favor intente de nuevo.")