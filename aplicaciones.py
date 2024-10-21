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
        for idx, cancion in enumerate(self.canciones, start=1):
            print(f"{idx}. {cancion}")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("\nIngrese el número de la opción que desea seleccionar: ")
            if opcion == '1':
                self.mostrar_canciones()
            elif opcion == '2':
                print("Saliendo de Spotify Simulado. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")


## HAY que probar si funciona bien
class Tetris:
    def __init__(self):
        self.grid = [[0] * 10 for _ in range(20)]  # Una cuadrícula de 20 filas por 10 columnas
        self.current_piece = self.generate_piece()

    def generate_piece(self):
        # Generar una pieza simplificada (por ejemplo, una pieza cuadrada 2x2)
        return [[1, 1], [1, 1]]

    def display_grid(self):
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def place_piece(self):
        # Colocar la pieza en la parte superior de la cuadrícula
        piece = self.current_piece
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                self.grid[r][c + 4] = piece[r][c]  # Colocar la pieza en la columna central

    def menu_tetris(self):
        while True:
            print("\nMenu Tetris:")
            print("1. Jugar")
            print("2. Salir del juego")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                print("\nJugando Tetris...")
                self.place_piece()
                self.display_grid()
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
        self.noticias = ["Publicación 1: ¡Hola Mundo!", "Publicación 2: Disfrutando de un día soleado", "Publicación 3: Nueva receta de cocina"]

    def mostrar_noticias(self):
        print("Noticias de Instagram:")
        for noticia in self.noticias:
            print(f"- {noticia}")

    def menu_twitter(self):
        while True:
            print("\nMenu Instagram:")
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