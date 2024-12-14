import validaciones
from dispositivo import Dispositivo,Tablet, Celular,CelularAntiguo,CelularNuevo
from central import Central
from app_store import AppStore
from operadora import Operadora
import csv
## 1er menu que se muestra, opciones generales
def mostrar_menu():
    print("\n-----MENÚ PRINCIPAL-----")
    print("1. Operadora")
    print("2. Dispositivo")
    print("3. Salir")

## Menu de la operadora, para crear o eliminar un celular
def mostrar_submenu_operadora():
    print("\n-----Submenú Operadora-----")
    print("1. Crear Dispositivo")
    print("2. Eliminar Dispositivor")
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

# Submenú celular, hay opciones que solo se muestran si las apps correspondientes están descargadas. 
def mostrar_submenu_celular(dispositivo):
    print("\n-----Menú-----")
    print("1. 📖 Contactos")
    print("2. 💬 Mensajería SMS")
    print("3. 📧 e-mail")
    print("4. 📞 Teléfono")
    print("5. 📱 App Store")
    print("6. ⚙️  Configuración")
    if True in [valor[0] for valor in dispositivo.apps.apps_descargadas.values()] and not isinstance(dispositivo,CelularAntiguo):  
        print("7. 👺Eliminar app")
    if dispositivo.apps.apps_descargadas["Spotify"][0] and not isinstance(dispositivo,CelularAntiguo):
        print("8. 🎧 Abrir Spotify")
    if dispositivo.apps.apps_descargadas["Goodreads"][0] and not isinstance(dispositivo,CelularAntiguo):
        print("9. 📚 Abrir Goodreads")
    if dispositivo.apps.apps_descargadas["Calculadora"][0] and not isinstance(dispositivo,CelularAntiguo):
        print("10. 🧮 Abrir Calculadora")
    if dispositivo.apps.apps_descargadas["Reloj"][0] and not isinstance(dispositivo,CelularAntiguo):
        print("11. 🕑 Abrir Reloj")
    if dispositivo.apps.apps_descargadas["Notas"][0] and not isinstance(dispositivo,CelularAntiguo):
        print("12. 📝 Abrir Notas")
    if not isinstance(dispositivo,Tablet):
        print("0. Salir y dejar el celular prendido (puede recibir llamados)")
        print("00. Salir y apagar el dispositivo")
    else:
        print("0. Apagar Tablet")


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
            continue 

        indice = int(eleccion) - 1
        app_seleccionada = apps_descargadas[indice]
        celular.apps.eliminar_app(app_seleccionada)
        

def cargar_dispositivos():
    try:
        with open('dispositivos.csv', "r", newline='') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                tipo_dispositivo = fila.get('tipo')  # Columna tipo indica la clase a instanciar

                if tipo_dispositivo == 'Celular_Nuevo':
                    dispositivo = CelularNuevo(
                        id=fila.get('id'),
                        nombre=fila.get('nombre'),
                        modelo=fila.get('modelo'),
                        marca=fila.get('marca'),
                        sistema_operativo=fila.get('sistema_operativo'),
                        version=fila.get('version'),
                        memoria_ram=fila.get('ram'),
                        almacenamiento=fila.get('almacenamiento'),
                        numero=fila.get('numero'),
                        direcc_email=fila.get('email')
                    )

                elif tipo_dispositivo == 'Tabelt':
                    dispositivo = Tablet(
                        id=fila.get('id'),
                        nombre=fila.get('nombre'),
                        modelo=fila.get('modelo'),
                        marca=fila.get('marca'),
                        sistema_operativo=fila.get('sistema_operativo'),
                        version=fila.get('version'),
                        memoria_ram=fila.get('ram'),
                        almacenamiento=fila.get('almacenamiento'),
                        direcc_email=fila.get('email')
                    )

                elif tipo_dispositivo == 'Celular_Antiguo':
                    dispositivo = CelularAntiguo(
                        id=fila.get('id'),
                        nombre=fila.get('nombre'),
                        modelo=fila.get('modelo'),
                        marca=fila.get('marca'),
                        sistema_operativo=fila.get('sistema_operativo'),
                        version=fila.get('version'),
                        memoria_ram=fila.get('ram'),
                        almacenamiento=fila.get('almacenamiento'),
                        numero=fila.get('numero'),
                    )

                else:
                    print(f"Tipo de dispositivo desconocido: {fila['tipo']}")
                    continue

                # Se gurda en operadora
                Operadora.central.ids_registrados[dispositivo.id] = dispositivo
                if isinstance(dispositivo, Celular):  # Solo Celular y derivados tienen números
                    Operadora.central.celulares_registrados[dispositivo.numero] = dispositivo
                    dispositivo.asignar_sms_telefono(Operadora.central)
            

    except FileNotFoundError:
        print("Error: El archivo no existe.")
    except IOError:
        print("Error al leer el archivo.")
