## No se si hacer una class aplicación

class Aplicacion:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_menu(self):
        print(f"\nMenu {self.nombre}:")
        print("1. Ver contenido")
        print("2. Salir de la app")

    def mostrar_contenido(self):
        raise NotImplementedError("Debe implementar este método en la subclase")

    def menu(self):
        opcion = None
        while opcion != '2':
            self.mostrar_menu()
            opcion = input("\nSeleccione una opción: ")
            if opcion == '1':
                self.mostrar_contenido()
            elif opcion == '2':
                print(f"Saliendo de {self.nombre}. ¡Hasta luego!")
            else:
                print("Opción inválida. Por favor, intente de nuevo.")
      
class Spotify(Aplicacion):
    def __init__(self):
        super().__init__("Spotify")
        self.canciones = [
            "Canción 1 - Artista A",
            "Canción 2 - Artista B",
            "Canción 3 - Artista C",
            "Canción 4 - Artista D"
        ]

    def mostrar_contenido(self):
        print("\nLista de canciones disponibles ♫♬♪♩𝄞:")
        for cancion in self.canciones:
            print(cancion)
        print('▶︎ •၊၊||၊|။||||။‌‌‌‌‌၊|• 0:30')


class Tetris(Aplicacion):
    def __init__(self):
        super().__init__("Tetris")

    def mostrar_contenido(self):
        print("*************************************")
        print("*       ¡Bienvenido a Tetris!       *")
        print("*************************************")
        print("\nControles:")
        print(" - Izquierda: 'a'")
        print(" - Derecha: 'd'")
        print(" - Rotar: 'w'")
        print(" - Bajar rápido: 's'")
        print(" - Pausar: 'p'\n")


class Salud(Aplicacion):
    def __init__(self):
        super().__init__("Salud")
        self.informacion = (
            "Información básica de salud:\n- Mantenerse hidratado\n"
            "- Hacer ejercicio regularmente\n- Comer una dieta balanceada"
        )

    def mostrar_contenido(self):
        print(self.informacion)


class Twitter(Aplicacion):
    def __init__(self):
        super().__init__("Twitter")
        self.noticias = [
            "Publicación 1: Muerte de Liam Payne",
            "Publicación 2: Vamos Racing",
            "Publicación 3: Lean aprobanos"
        ]

    def mostrar_contenido(self):
        print("Noticias de Twitter:")
        for noticia in self.noticias:
            print(f"- {noticia}")