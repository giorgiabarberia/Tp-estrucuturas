import validaciones
from class_central import Central
from class_app_store import AppStore
## 1er menu que se muestra, opciones generales
def mostrar_menu():
    print("\n-----MENÚ PRINCIPAL-----")
    print("1. Operadora")
    print("2. Celular")
    print("3. Salir")

## Menu de la operadora, para crear o eliminar un celular
def mostrar_submenu_operadora():
    print("\n-----Submenú Operadora-----")
    print("1. Crear Celular")
    print("2. Eliminar Celular")
    print("3. Volver al Menú Principal")

## Función para encontrar el numero de celular al que quiere acceder el usuario
def preguntar_numero_celular():
    numero = input('\nIngrese el número del celular al que quiere acceder: ')
    continuar = True
    while continuar and numero not in Central.celulares_registrados:
        print('Error, número no registrado')
        continuar = validaciones.desea_continuar()
        if continuar:
            numero = input('Ingrese nuevamente el número del celular al que quiere acceder: ')
    return numero

def mostrar_submenu_celular(celular):
    print("\n-----Menú-----")
    print("1. 📖 Contactos")
    print("2. 💬 Mensajería SMS")
    print("3. 📧 e-mail")
    print("4. 📞 Teléfono")
    print("5. 📱 App Store")
    print("6. ⚙️  Configuración")
    if celular.apps.apps_descargadas:  
        print("7. Eliminar app")
    if celular.apps.apps_descargadas["Spotify"][0]:
        print("8. 🎧 Abrir Spotify")
    if celular.apps.apps_descargadas["Tetris"][0]:
        print("9. 🧩 Abrir Tetris")
    if celular.apps.apps_descargadas["Salud"][0]:
        print("10. ❤️‍🩹 Abrir Salud")
    if celular.apps.apps_descargadas["Twitter"][0]:
        print("11. 🐤 Abrir Twitter")
    print("0. Salir y dejar el celular prendido (puede recibir llamados)")
    print("00. Salir y apagar el celular")


# Permite al usuario eliminar aplicaciones descargadas en el celular
def menu_eliminar_app(celular):
    while True:
        print("\nAplicaciones disponibles para eliminar:")
        apps_descargadas = [app for app, (descargada, _) in celular.apps.apps_descargadas.items() if descargada]

        if not apps_descargadas:
            print("No hay aplicaciones descargadas disponibles para eliminar.")
            return  

        for idx, app in enumerate(apps_descargadas, start=1):
            print(f"{idx}. {app}")

        eleccion = input("\nIngrese el número de la aplicación que desea eliminar (o 'salir' para terminar): ").lower()

        if eleccion == 'salir':
            print("Saliendo del menú de eliminación de aplicaciones.")
            return  

        if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(apps_descargadas)):
            print("Elección inválida. Por favor, intente de nuevo.")
            continue  # Continúa al inicio del while

        indice = int(eleccion) - 1
        app_seleccionada = apps_descargadas[indice]
        celular.apps.eliminar_app(app_seleccionada)
        