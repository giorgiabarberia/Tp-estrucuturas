from class_operadora import Operadora
from class_central import Central
from class_celular import Celular
from class_app_store import AppStore
import validaciones
import funciones_menu

operadora = Operadora()

## Acá deberíamos bajar desde csv todas las listas para usar ahora y tener datos viejos. 

def menu_principal():
    while True:
        funciones_menu.mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            while True:
                funciones_menu.mostrar_submenu_operadora()
                sub_opcion = input("Seleccione una opción: ")
                
                if sub_opcion == '1':
                    operadora.registrar_celular()
                elif sub_opcion == '2':
                    numero = input('Ingrese el número del celular al que quiere eliminar: ')
                    operadora.eliminar_celular(numero) ## No valido que el numero exista acá poruqe lo hice en la funcion, pero nose si mejor hacerlo acá
                elif sub_opcion == '3':
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
        

        elif opcion == '2':
            if Central.celulares_registrados:
                numero = funciones_menu.preguntar_numero_celular()
                ## Prendo y desbloqueo (o no) el celular
                if numero in Central.celulares_registrados:
                    celular = Central.celulares_registrados[numero]
                    celular.prender_celular()
                    if celular.bloqueo:
                        celular.apagar_celular()
                    else:
                        ## El celular está desbloqueado, acá van sus funciones (apps)
                        while True:
                            funciones_menu.mostrar_submenu_celular()
                            eleccion = input("Seleccione una opción: ")

                            if eleccion == '1':
                                print("Has seleccionado Contactos.")
                                # Agrega aquí el código para manejar Contactos
                            elif eleccion == '2':
                                print("Has seleccionado Mensajería SMS.")
                                # Agrega aquí el código para manejar Mensajería SMS
                                celular.abrir_app_sms()
                            elif eleccion == '3':
                                print("Has seleccionado e-mail.")
                                # Agrega aquí el código para manejar e-mail
                                celular.abrir_app_email()
                            elif eleccion == '4':
                                print("Has seleccionado Teléfono.")
                                # Agrega aquí el código para manejar Teléfono
                            elif eleccion == '5':
                                print("Has seleccionado App Store.")
                                # Agrega aquí el código para manejar App Store
                            elif eleccion == '6':
                                print("Has seleccionado Configuración.")
                                # Agrega aquí el código para manejar Configuración
                            elif AppStore.apps_descargadas.get('Spotify', False) and eleccion == '7':
                                print("Has seleccionado Abrir Spotify.")
                                # Agrega aquí el código para manejar Spotify
                            elif AppStore.apps_descargadas.get('Tetris', True) and eleccion == '8':
                                print("Has seleccionado Abrir Tetris.")
                                # Agrega aquí el código para manejar Tetris
                            elif AppStore.apps_descargadas.get('Salud', True) and eleccion == '9':
                                print("Has seleccionado Abrir Salud.")
                                # Agrega aquí el código para manejar Salud
                            elif AppStore.apps_descargadas.get('Instagram', True) and eleccion == '10':
                                print("Has seleccionado Abrir Instagram.")
                                # Agrega aquí el código para manejar Instagram
                            elif eleccion == '0':
                                print("Saliendo del menú.")
                                break
                            else:
                                print("Opción no válida. Por favor, seleccione una opción válida.")


            else:
                print('Aún no hay ningún celular registrado en la central al que pueda acceder.')
            # Aquí puedes agregar más funciones relacionadas con el celular

        elif opcion == '3':
            print("Saliendo del programa.")
            ## Acá tendríamos que subir al csv todas las listas q actualizamos en esta corrida.
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")