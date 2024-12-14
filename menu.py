from operadora import Operadora
from central import Central
from dispositivo import Dispositivo,Tablet,Celular,CelularAntiguo,CelularNuevo
from app_store import AppStore
from aplicaciones import Spotify, Goodreads, Calculadora, Reloj
from contactos import Contactos
import funciones_menu


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
                print('Aún no hay ningún dispositivo registrado al que pueda acceder.')
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
        dispositivos_validos = ['tablet','celular']
        sub_opcion = input("Seleccione una opción: ")
        
        if sub_opcion == '1':
            tipo_dispositivo = input('Ingrese el tipo de dispositivo que desea crear: ').strip().lower()
            while tipo_dispositivo not in dispositivos_validos:
                tipo_dispositivo = input('Dispositivo incorrecto. Ingrese nuevamente el tipo de dispositivo que desea crear: ').strip().lower() 
            if tipo_dispositivo == 'tablet':
                operadora.registrar_dispositivo('Tablet')
            if tipo_dispositivo == 'celular':
                while True:  
                    año = input('Ingrese el año de fabricación del celular: ')
                    try:
                        año = int(año) 
                        break  
                    except ValueError:
                        print("Entrada no válida. Debe ingresar un número.")
                if año >= 2000:
                    operadora.registrar_dispositivo('Celular Nuevo')
                else:
                    operadora.registrar_dispositivo('Celular Antiguo')

        elif sub_opcion == '2':
            id = input('Ingrese el id del dispositivo que desea eliminar: ')
            operadora.eliminar_dispositivo(id)
            
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

def celular_menu(dispositivo,operadora):
    continuar = True
    while continuar:
        if not isinstance(dispositivo,Tablet):
            # Apenas entras, se fija si tenes llamadas entrantes, y no te deja usar el celular hasta que decidas que hacer con ellas
            while dispositivo.telefono.llamadas_entrantes:
                dispositivo.telefono.ejecutar_llamadas_entrantes()
        funciones_menu.mostrar_submenu_celular(dispositivo)
        eleccion = input("Seleccione una opción: ")
        ## Acá poner lo de las llamadas entrantes. Que solo aparezca el menú
        if eleccion == '1':
            print("Has seleccionado Contactos.")
            dispositivo.contactos.menu_contactos()
        elif eleccion == '2' and not isinstance(dispositivo,Tablet):
            print("Has seleccionado Mensajería SMS.")
            dispositivo.abrir_app_sms()
        elif eleccion == '3' and not isinstance(dispositivo,CelularAntiguo):
            print("Has seleccionado e-mail.")
            dispositivo.abrir_app_email(operadora)
        elif eleccion == '4' and not isinstance(dispositivo,Tablet):
            print("Has seleccionado Teléfono.")
            dispositivo.abrir_app_telefono()
        elif eleccion == '5' and not isinstance(dispositivo,CelularAntiguo):
            print("Has seleccionado App Store.")
            dispositivo.apps.mostrar_apps()
        elif eleccion == '6':
            print("Has seleccionado Configuración.")
            dispositivo.configuracion.configuracion()
        elif not isinstance(dispositivo,CelularAntiguo) and True in [valor[0] for valor in dispositivo.apps.apps_descargadas.values()] and eleccion == '7':
            print("Has seleccionado Eliminar App.")
            funciones_menu.menu_eliminar_app(dispositivo)
        elif not isinstance(dispositivo,CelularAntiguo) and dispositivo.apps.apps_descargadas["Spotify"][0] and eleccion == '8':
            print("Has seleccionado Abrir Spotify.")
            dispositivo.apps.apps_descargadas["Spotify"][1].ejecutar_menu()
        elif not isinstance(dispositivo,CelularAntiguo) and dispositivo.apps.apps_descargadas["Goodreads"][0] and eleccion == '9':
            print("Has seleccionado Abrir Goodreads.")
            dispositivo.apps.apps_descargadas["Goodreads"][1].ejecutar_menu()
        elif not isinstance(dispositivo,CelularAntiguo) and dispositivo.apps.apps_descargadas["Calculadora"][0] and eleccion == '10':
            print("Has seleccionado Abrir Calculadora.")
            dispositivo.apps.apps_descargadas["Calculadora"][1].ejecutar_menu()
        elif not isinstance(dispositivo,CelularAntiguo) and dispositivo.apps.apps_descargadas["Reloj"][0] and eleccion == '11':
            print("Has seleccionado Abrir Reloj.")
            dispositivo.apps.apps_descargadas["Reloj"][1].ejecutar_menu()
        elif not isinstance(dispositivo,CelularAntiguo) and dispositivo.apps.apps_descargadas["Notas"][0] and eleccion == '12':
            print("Has seleccionado Abrir Notas.")
            dispositivo.apps.apps_descargadas["Notas"][1].ejecutar_menu()
        elif eleccion == '0':
            print("Saliendo del menú.")
            continuar = False 
        elif eleccion == "00":
            print("Apagando el celular y saliendo del menú")
            dispositivo.prendido = False
            dispositivo.bloqueo = True
            dispositivo.configuracion.desactivar_red_movil()
            continuar = False 
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")



# Función principal
def main():
    funciones_menu.cargar_dispositivos()
    operadora = Operadora('Personal')
    menu_principal(operadora)

# Ejecución del código
if __name__ == "__main__":
    main()