import validaciones
from class_central import Central
from class_app_store import AppStore
## 1er menu que se muestra, opciones generales
def mostrar_menu():
    print("Menú Principal")
    print("1. Operadora")
    print("2. Celular")
    print("3. Salir")

## Menu de la operadora, para crear o eliminar un celular
def mostrar_submenu_operadora():
    print("Submenú Operadora")
    print("1. Crear Celular")
    print("2. Eliminar Celular")
    print("3. Volver al Menú Principal")

## Función para encontrar el numero de celular al que quiere acceder el usuario
def preguntar_numero_celular():
    numero = input('Ingrese el número del celular al que quiere acceder: ')
    continuar = True
    while continuar and numero not in Central.celulares_registrados:
        continuar = validaciones.desea_continuar()
        if continuar:
            numero = input('Ingrese nuevamente el número del celular al que quiere acceder: ')
    return numero

def mostrar_submenu_celular():
    print("\nMenú:")
    print("1. Contactos")
    print("2. Mensajería SMS")
    print("3. e-mail")
    print("4. Teléfono")
    print("5. App Store")
    print("6. Configuración")
    if AppStore.apps_descargadas.get('Spotify', True):
        print("7. Abrir Spotify")
    if AppStore.apps_descargadas.get('Tetris', True):
        print("8. Abrir Tetris")
    if AppStore.apps_descargadas.get('Salud', True):
        print("9. Abrir Salud")
    if AppStore.apps_descargadas.get('Instagram', True):
        print("10. Abrir Instagram")
    print("0. Salir")