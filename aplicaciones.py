
class Spotify:
    def __init__(self):
        self.canciones = [
            "Canción 1 - Artista A",
            "Canción 2 - Artista B",
            "Canción 3 - Artista C",
            "Canción 4 - Artista D"
        ]

    def mostrar_menu(self):
        print("\nSPOTIFY ♫♬♪♩𝄞")
        print("1. Ver lista de canciones")
        print("2. Salir")

    def mostrar_canciones(self):
        print("\nLista de canciones disponibles ♫♬♪♩𝄞:")
        for cancion in self.canciones:
            print(cancion)

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("\nIngrese el número de la opción que desea seleccionar: ")
            if opcion == '1':
                self.mostrar_canciones()
            elif opcion == '2':
                print("Saliendo de Spotify. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

## HAY que probar si funciona bien
class Tetris:
    def entrada_tetris():
        print("*************************************")
        print("*       ¡Bienvenido a Tetris!       *")
        print("*************************************")
        print("\nControles:")
        print(" - Izquierda: 'a'")
        print(" - Derecha: 'd'")
        print(" - Rotar: 'w'")
        print(" - Bajar rápido: 's'")
        print(" - Pausar: 'p'\n")
        print("Tablero de Tetris:")
        for _ in range(20):  # 20 filas
            print("|          |")  # 10 columnas vacías
        print("------------")  # Base del tablero

    def menu_tetris(self):
        while True:
            print("\nMenu Tetris:")
            print("1. Jugar")
            print("2. Salir del juego")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.entrada_tetris
            elif opcion == '2':
                print("Saliendo del juego...")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

class Salud:
    def __init__(self):
        self.informacion = "Información básica de salud:\n- Mantenerse hidratado\n- Hacer ejercicio regularmente\n- Comer una dieta balanceada"

    def mostrar_informacion(self):
        print(self.informacion)

    def menu_salud(self):
        while True:
            print("\nMenu Salud:")
            print("1. Ver Información de Salud")
            print("2. Salir de la app")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                print("\nMostrando información de salud...")
                self.mostrar_informacion()
            elif opcion == '2':
                print("Saliendo de la app.")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")


class Twitter:
    def __init__(self):
        self.noticias = ["Publicación 1: Muerte de Liam Payne", "Publicación 2: Vamos Racing", "Publicación 3: Lean aprobanos"]

    def mostrar_noticias(self):
        print("Noticias de Twitter:")
        for noticia in self.noticias:
            print(f"- {noticia}")

    def menu_twitter(self):
        while True:
            print("\nMenu Twitter:")
            print("1. Ver Noticias")
            print("2. Salir de la app")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                print("\nMostrando noticias de Twitter...")
                self.mostrar_noticias()
            elif opcion == '2':
                print("Saliendo de la app.")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")
