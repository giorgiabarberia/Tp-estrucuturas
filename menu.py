from class_operadora import Operadora
from class_central import Central
from class_celular import Celular
from class_app_store import AppStore
from aplicaciones import Spotify, Goodreads, Calculadora, Reloj
from class_contactos import Contactos
import funciones_menu
import csv


# Función principal del menú
def menu_principal(operadora):
    continuar = True
    while continuar:
        funciones_menu.mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            submenu_operadora(operadora)
        elif opcion == '2':
            if Central.celulares_registrados:
                manejar_celular()
            else:
                print('Aún no hay ningún celular registrado en la central al que pueda acceder.')
        elif opcion == '3':
            print("Saliendo del programa.")
            continuar = False 
        else:
            print("Opción no válida. Intente de nuevo.")

# Menú de la operadora
def submenu_operadora(operadora):
    continuar = True
    while continuar:
        funciones_menu.mostrar_submenu_operadora()
        sub_opcion = input("Seleccione una opción: ")
        
        if sub_opcion == '1':
            operadora.registrar_celular()
        elif sub_opcion == '2':
            numero = input('Ingrese el número del celular al que quiere eliminar: ')
            operadora.eliminar_celular(numero)
        elif sub_opcion == '3':
            continuar = False  # Cambiar la condición para salir del bucle
        else:
            print("Opción no válida. Intente de nuevo.")

def manejar_celular():
    numero = funciones_menu.preguntar_numero_celular()
    if numero in Central.celulares_registrados:
        celular = Central.celulares_registrados[numero]
        ok = celular.prender_celular()
        if ok:
            celular_menu(celular)
    else:
        print("Número de celular no registrado.")

def celular_menu(celular):
    continuar = True
    while continuar:
        # Apenas entras, se fija si tenes llamadas entrantes, y no te deja usar el celular hasta que decidas que hacer con ellas
        while celular.telefono.llamadas_entrantes:
            celular.telefono.ejecutar_llamadas_entrantes()
        funciones_menu.mostrar_submenu_celular(celular)
        eleccion = input("Seleccione una opción: ")
        ## Acá poner lo de las llamadas entrantes. Que solo aparezca el menú
        if eleccion == '1':
            print("Has seleccionado Contactos.")
            celular.contactos.menu_contactos()
        elif eleccion == '2':
            print("Has seleccionado Mensajería SMS.")
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
            celular.configuracion.configuracion()
        elif True in [valor[0] for valor in celular.apps.apps_descargadas.values()] and eleccion == '7':
            print("Has seleccionado Eliminar App.")
            funciones_menu.menu_eliminar_app(celular)
        elif celular.apps.apps_descargadas["Spotify"][0] and eleccion == '8':
            print("Has seleccionado Abrir Spotify.")
            celular.apps.apps_descargadas["Spotify"][1].ejecutar_menu()
        elif celular.apps.apps_descargadas["Goodreads"][0] and eleccion == '9':
            print("Has seleccionado Abrir Goodreads.")
            celular.apps.apps_descargadas["Goodreads"][1].ejecutar_menu()
        elif celular.apps.apps_descargadas["Calculadora"][0] and eleccion == '10':
            print("Has seleccionado Abrir Calculadora.")
            celular.apps.apps_descargadas["Calculadora"][1].ejecutar_menu()
        elif celular.apps.apps_descargadas["Reloj"][0] and eleccion == '11':
            print("Has seleccionado Abrir Reloj.")
            celular.apps.apps_descargadas["Reloj"][1].ejecutar_menu()
        elif eleccion == '0':
            print("Saliendo del menú.")
            continuar = False 
        elif eleccion == "00":
            print("Apagando el celular y saliendo del menú")
            celular.prendido = False
            celular.bloqueo = True
            celular.configuracion.desactivar_red_movil()
            continuar = False 
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")



# Función principal
def main():
    funciones_menu.cargar_celulares()
    operadora = Operadora('Personal')
    menu_principal(operadora)

# Ejecución del código
if __name__ == "__main__":
    main()