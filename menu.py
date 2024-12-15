from operadora import Operadora
from central import Central
from dispositivo import Dispositivo,Tablet,Celular,CelularAntiguo,CelularNuevo
from app_store import AppStore
from aplicaciones import Spotify, Goodreads, Calculadora, Reloj
from contactos import Contactos
import funciones_menu


# Función principal del menú
def menu_principal(operadora, central):
    continuar = True
    while continuar:
        funciones_menu.mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            submenu_operadora(operadora)
        elif opcion == '2':
            if central.ids_registrados:
                manejar_dispositivo(central)  
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
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '1':
            crear_dispositivo(operadora)

        elif sub_opcion == '2':
            identificador = input('Ingrese el número o email del dispositivo que desea eliminar: ')
            operadora.eliminar_dispositivo(identificador)
            
        elif sub_opcion == '3':
            continuar = False  # Cambiar la condición para salir del bucle
        
        else:
            print("Opción no válida. Intente de nuevo.")
            
# Menú crear dispositivo
def crear_dispositivo(operadora):
    dispositivos_validos = ['tablet','celular']
    tipo_dispositivo = input('Ingrese el tipo de dispositivo que desea crear: ').strip().lower()
    while tipo_dispositivo not in dispositivos_validos:
        tipo_dispositivo = input('Dispositivo incorrecto. Ingrese nuevamente el tipo de dispositivo que desea crear (Tablet o Celular): ').strip().lower() 
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

def manejar_dispositivo(central):
    print("\n¿Desea ingresar con un celular o una tablet?")
    tipo = input("Escriba 'celular' o 'tablet': ").strip().lower()

    if tipo == 'celular':
        numero = input("Ingrese el número del celular: ").strip()
        if numero in central.celulares_registrados:
            dispositivo = central.celulares_registrados[numero]
            if isinstance(dispositivo, Celular):
                ok = dispositivo.prender_celular()
                if ok:
                    dispositivo_menu(dispositivo, central)
        else:
            print("Número de celular no registrado.")

    elif tipo == 'tablet':
        mail = input("Ingrese el email de la tablet: ").strip()
        if mail in Dispositivo.mails_usados:
            for elemento in Operadora.central.ids_registrados.values():
                if not isinstance(elemento, CelularAntiguo): 
                    if elemento.direcc_email == mail:
                        dispositivo = elemento
                        break
        if dispositivo and isinstance(dispositivo, Tablet):
            dispositivo_menu(dispositivo, central)
        else:
            print("Mail de tablet no registrado o el dispositivo no es una tablet.")

    else:
        print("Tipo de dispositivo no válido. Por favor, intente nuevamente.")

def dispositivo_menu(dispositivo, central):
    continuar = True
    while continuar:
        if not isinstance(dispositivo, Tablet):
            while dispositivo.telefono.llamadas_entrantes:
                dispositivo.telefono.ejecutar_llamadas_entrantes()
        funciones_menu.mostrar_submenu_dispositivo(dispositivo)
        eleccion = input("Seleccione una opción: ")

        if not isinstance(dispositivo, Tablet) and eleccion == '1':
            print("Has seleccionado Contactos.")
            dispositivo.contactos.menu_contactos()
        elif not isinstance(dispositivo, Tablet) and eleccion == '2':
            print("Has seleccionado Mensajería SMS.")
            dispositivo.abrir_app_sms()
        elif not isinstance(dispositivo, CelularAntiguo) and eleccion == '3':
            print("Has seleccionado e-mail.")
            dispositivo.abrir_app_email(central)  
        elif not isinstance(dispositivo, Tablet) and eleccion == '4':
            print("Has seleccionado Teléfono.")
            dispositivo.abrir_app_telefono()
        elif eleccion == '5' and not isinstance(dispositivo, CelularAntiguo):
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
    central = Central()
    operadora.central = central
    menu_principal(operadora,central)

# Ejecución del código
if __name__ == "__main__":
    main()