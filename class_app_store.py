import validaciones
from aplicaciones import Spotify,Salud,Twitter,Tetris

class AppStore:
    def __init__(self):
        self.apps_descargadas = {
            'Spotify': False,
            'Tetris': False,
            'Salud': False,
            'Twitter': False
        }
    
    def descargar_app(self, app):
        if app in self.apps_descargadas and not self.apps_descargadas[app]:
            self.apps_descargadas[app] = True
            print(f'{app} ha sido descargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')


    def eliminar_app(self, app):
        if app in self.apps_descargadas and self.apps_descargadas[app]:
            self.apps_descargadas[app] = False
            print(f'{app} ha sido eliminada.')
        elif app in self.apps_descargadas and not self.apps_descargadas[app]:
            print(f'{app} no está descargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')

    def mostrar_apps(self):
        print("\nAplicaciones disponibles:")
        for app, descargada in self.apps_descargadas.items():
            estado = "Descargada" if descargada else "No descargada"
            print(f"- {app}: {estado}")
        app_seleccionada = input("Seleccione una aplicación (o escriba 'salir' para terminar): ")
        if app_seleccionada.lower() == 'salir':
            print("Saliendo de la AppStore.")
            return
        self.seleccionar_app(app_seleccionada)

    def seleccionar_app(self, app):
        if app in self.apps_descargadas:
            if not self.apps_descargadas[app]:
                print(f"\n{app} no está descargada. Opciones:")
                print("1. Descargar")
                print("2. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    self.descargar_app(app)
                elif opcion == '2':
                    print("Saliendo...")
            else:
                print(f"\n{app} ya está descargada. Opciones:")
                print("1. Ingresar")
                print("2. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    print(f"Ingresando a {app}...")
                    app()
                elif opcion == '2':
                    print("Saliendo...")
        else:
            print(f'{app} no se encuentra en AppStore.')


