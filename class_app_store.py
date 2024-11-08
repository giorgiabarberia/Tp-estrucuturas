from aplicaciones import Spotify, Goodreads, Calculadora, Reloj

class AppStore:
    def __init__(self):
        self.apps_descargadas = {
            'Spotify': (False, Spotify()),
            'Goodreads': (False, Goodreads()),
            'Calculadora': (False, Calculadora()),
            'Reloj': (False, Reloj())
            }
    
    # Descarga una aplicación si no está descargada. 
    def descargar_app(self, app):
        if app in self.apps_descargadas: # Validamos 2 veces por programacion defensiva, alguien puede usar la función en otro lugar más adelante y generaría error sino
            if not self.apps_descargadas[app][0]:
                self.apps_descargadas[app] = (True, self.apps_descargadas[app][1])
                print(f'{app} ha sido descargada.')
            else:
                print(f'{app} ya está descargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')
            
    # Elimina una aplicación que está descargada
    def eliminar_app(self, app):
        if app in self.apps_descargadas:
            if self.apps_descargadas[app][0]:
                self.apps_descargadas[app] = (False, self.apps_descargadas[app][1])
                print(f'{app} ha sido eliminada.')
            else:
                print(f'{app} no está descargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')
         
    
    # Muestra el estado de todas las aplicaciones disponibles
    def mostrar_apps(self):
        continuar = True
        app_seleccionada = ''
        while app_seleccionada not in self.apps_descargadas and continuar:
            print("\nAplicaciones disponibles:")
            for app, (descargada, _) in self.apps_descargadas.items():
                estado = "Descargada" if descargada else "No descargada"
                print(f"- {app}: {estado}")  

            app_seleccionada = input("Escriba el nombre de una aplicación (o escriba 'salir' para terminar): ").capitalize()
            if app_seleccionada.lower() == 'salir':
                print("Saliendo de la AppStore.")
                continuar = False
        self.seleccionar_app(app_seleccionada)

    # Selecciona una aplicación para descargar o ingresar
    def seleccionar_app(self, app):
        if app in self.apps_descargadas:
            if not self.apps_descargadas[app][0]:
                print(f"\n{app} no está descargada. Opciones:")
                print("1. Descargar")
                print("2. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    self.descargar_app(app)
                else:
                    print("Saliendo...")
            else:
                print(f"\n{app} ya está descargada. Opciones:")
                print("1. Ingresar")
                print("2. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    print(f"Ingresando a {app}...")
                    self.apps_descargadas[app][1].menu()
                else:
                    print("Saliendo...")
        else:
            print(f'{app} no se encuentra en AppStore.')