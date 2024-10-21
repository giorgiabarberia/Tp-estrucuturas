from class_operadora import Operadora
from class_central import Central
from class_celular import Celular
from class_app_store import AppStore
from aplicaciones import Spotify,Tetris,Salud,Twitter
from class_contactos import Contactos
import validaciones
import funciones_menu

operadora = Operadora('Personal')

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
                            funciones_menu.mostrar_submenu_celular(celular)
                            eleccion = input("Seleccione una opción: ")

                            if eleccion == '1':
                                print("Has seleccionado Contactos.")
                                celular.contactos.menu_contactos()
                            elif eleccion == '2':
                                print("Has seleccionado Mensajería SMS.")
                                # Agrega aquí el código para manejar Mensajería SMS
                                celular.abrir_app_sms()
                            elif eleccion == '3':
                                print("Has seleccionado e-mail.")
                                celular.abrir_app_email()
                            elif eleccion == '4':
                                print("Has seleccionado Teléfono.")
                                celular.abrir_app_telefono()
                            elif eleccion == '5':
                                print("Has seleccionado App Store.")
                                celular.apps.mostrar_apps()
                            elif eleccion == '6':
                                print("Has seleccionado Configuración.")
                                celular.configuacion.configuacion()
                            elif celular.apps.apps_descargadas and eleccion == '7':
                                print("Has seleccionado Eliminar App.")
                                funciones_menu.menu_eliminar_app(celular)
                            elif celular.apps.apps_descargadas.get('Spotify', False) and eleccion == '8':
                                print("Has seleccionado Abrir Spotify.")
                                Spotify.ejecutar()
                            elif celular.apps.apps_descargadas.get('Tetris', True) and eleccion == '9':
                                print("Has seleccionado Abrir Tetris.")
                                Tetris.menu_tetris()
                            elif celular.apps.apps_descargadas.get('Salud', True) and eleccion == '10':
                                print("Has seleccionado Abrir Salud.")
                                Salud.menu_salud()
                            elif celular.apps.apps_descargadas.get('Instagram', True) and eleccion == '11':
                                print("Has seleccionado Abrir Twitter.")
                                Twitter.menu_twitter()
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

menu_principal()