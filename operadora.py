from central import Central
from dispositivo import Dispositivo,Tablet,Celular,CelularNuevo,CelularAntiguo
import validaciones
import random
import string
import csv
from io import FileIO

class Operadora:
    central = Celular.central
    
    def __init__(self,nombre):
        self.nombre = nombre 

    # Función para generar un número de celular válido, que no esté ya en la central
    @staticmethod
    def crear_numero_aleatorio() -> str:
        numero = "11" + ''.join(random.choices("0123456789", k=8))
        while numero in Operadora.central.celulares_registrados:
            numero = "11" + ''.join(random.choices("0123456789", k=8))
        return numero

    # Función para generar un ID para los celulares que sea único. 
    @staticmethod
    def generar_id_unico(longitud=25) -> str:
        caracteres = string.ascii_letters + string.digits
        id = ''.join(random.choice(caracteres) for _ in range(longitud))
        while True:
            if id not in Operadora.central.ids_registrados:
                return id
    
    @staticmethod            
    def guardar_dispositivo(dispositivo):
        try:
            with open('dispositivos.csv', "a", newline='') as archivo:  
                escritor = csv.writer(archivo)
                if isinstance(dispositivo,CelularNuevo):
                    lista = [
                        'Celular_Nuevo',
                        dispositivo.id,
                        dispositivo.configuracion.nombre,
                        dispositivo.modelo,
                        dispositivo.marca,
                        dispositivo.sistema_operativo,
                        dispositivo.version,
                        dispositivo.memoria_ram,
                        dispositivo.almacenamiento,
                        dispositivo.numero,
                        dispositivo.direcc_email
                    ]
                if isinstance(dispositivo,Tablet):
                    lista = [
                        'Tabelt',
                        dispositivo.id,
                        dispositivo.configuracion.nombre,
                        dispositivo.modelo,
                        dispositivo.marca,
                        dispositivo.sistema_operativo,
                        dispositivo.version,
                        dispositivo.memoria_ram,
                        dispositivo.almacenamiento,'',
                        dispositivo.direcc_email
                        ]
                if isinstance(dispositivo,CelularAntiguo):
                    lista = [
                        'Celular_Antiguo',
                        dispositivo.id,
                        dispositivo.configuracion.nombre,
                        dispositivo.modelo,
                        dispositivo.marca,
                        dispositivo.sistema_operativo,
                        dispositivo.version,
                        dispositivo.memoria_ram,
                        dispositivo.almacenamiento,
                        dispositivo.numero,
                        ""
                    ]
                escritor.writerow(lista)  
        except IOError:
            print("Error al exportar archivo")
            raise IOError('Error al exportar el archivo')
        
    def registrar_dispositivo(self,tipo):
        id = self.generar_id_unico()
        nombre = input('Ingrese su nombre: ')
        nombre = validaciones.ingreso_no_vacio(nombre)
        marca = input('Ingrese la marca de su dispositivo: ')
        marca = validaciones.ingreso_no_vacio(marca)
        modelo = input('Ingrese el modelo del dispositivo: ')
        modelo = validaciones.ingreso_no_vacio(modelo)
        sistema_operativo = input('Ingrese el sistema operativo de su dispositivo: ')
        sistema_operativo = validaciones.ingreso_no_vacio(sistema_operativo)
        version = input('Ingrese la versión de su dispositivo: ')
        version = validaciones.ingreso_no_vacio(version)
        cap_memoria_ram = input('Ingrese la capacidad de la memoria RAM de su dispositivo: ')
        cap_memoria_ram = validaciones.ingreso_no_vacio(cap_memoria_ram)
        cap_almacenamiento = input('Ingrese la capacidad de almacenamiento de su dispositivo: ')
        cap_almacenamiento = validaciones.ingreso_no_vacio(cap_almacenamiento)
        if tipo != "Tablet":
            numero = self.crear_numero_aleatorio()
        if tipo != "Celular Antiguo":
            mail = input('Ingrese su mail: ')
            while not validaciones.validar_email(mail) or mail in Dispositivo.mails_usados:
                if not validaciones.validar_email(mail):
                    mail = input('Ingrese un mail válido, el formato del ingresado no es válido: ')
                else: 
                    mail = input('Ingrese un mail válido, el ingresado ya está en uso por otro dispositivo: ')
        if tipo == "Celular Nuevo":
            dispositivo = CelularNuevo(nombre, marca, modelo, sistema_operativo, version, cap_memoria_ram, cap_almacenamiento, id, numero, mail)
        elif tipo == "Celular Antiguo":
            dispositivo = CelularAntiguo(nombre, marca, modelo, sistema_operativo, version, cap_memoria_ram, cap_almacenamiento, id, numero)
        elif tipo == "Tablet":
            dispositivo = Tablet(nombre, marca, modelo, sistema_operativo, version, cap_memoria_ram, cap_almacenamiento,id,mail)
        Operadora.guardar_dispositivo(dispositivo)
        Operadora.central.ids_registrados[dispositivo.id] = dispositivo
        if tipo != "Tablet":
            Operadora.central.celulares_registrados[dispositivo.numero] = dispositivo
            dispositivo.asignar_sms_telefono(Operadora.central)
            print(f'Celular registrado con éxito.\nSu número es: {dispositivo.numero}')
        else:
            print(f"Tablet registrada con éxito.\nIngese a ella con su email: {mail}")


    def borrar_de_csv(self, id): 
        ## Elimina un registro del archivo dispositivos.csv basado en el id del dispositivo.
        try:
            # Leer todos los registros excepto el que queremos eliminar
            dispositivos_actualizados = []
            with open('dispositivos.csv', "r", newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector)  # Leer el encabezado
                for fila in lector:
                    # Validar que la fila tenga suficiente longitud antes de comparar
                    if len(fila) > 2 and fila[1] != id:  # `id` asumido en columna 2 (índice 1)
                        dispositivos_actualizados.append(fila)

            # Sobreescribir el archivo con los registros actualizados
            with open('dispositivos.csv', "w", newline='', encoding='utf-8') as archivo:  # Corregido a 'dispositivos.csv'
                escritor = csv.writer(archivo)
                escritor.writerow(encabezado)  # Escribir encabezado
                escritor.writerows(dispositivos_actualizados)  # Escribir datos actualizados

        except FileNotFoundError:
            print("Error: No se encontró el archivo 'dispositivos.csv'.")
        except IOError:
            print("Error al modificar el archivo 'dispositivos.csv'.")
        except Exception as e:
            print(f"Error inesperado: {e}")
            

    def eliminar_dispositivo(self,identificador):
        ok = True
        dispositivo = False
        # Caso 1: El identificador es un número
        if identificador in Operadora.central.celulares_registrados:
            dispositivo = Operadora.central.celulares_registrados[identificador]
            if isinstance(dispositivo, CelularNuevo):
                mail = dispositivo.direcc_email
                Dispositivo.eliminar_mail(mail)  # Eliminamos el correo
            del Operadora.central.celulares_registrados[dispositivo.numero]  # Eliminamos por número
            print(f'Dispositivo {identificador} eliminado con éxito.')
            
        # Caso 2: El identificador está en correos registrados
        elif identificador in Dispositivo.mails_usados:
            for elemento in Operadora.central.ids_registrados.values():
                if not isinstance(elemento, CelularAntiguo): 
                    if elemento.direcc_email == identificador:
                        dispositivo = elemento
                        break
            if dispositivo:  # Validamos que el dispositivo se haya encontrado
                if isinstance(dispositivo, CelularNuevo):
                    del Operadora.central.celulares_registrados[dispositivo.numero]
                mail = dispositivo.direcc_email
                Dispositivo.eliminar_mail(mail)  # Eliminamos el correo
                print(f'Dispositivo {identificador} eliminado con éxito.')
            else:
                print(f"Error: No se encontró el dispositivo con email {identificador}.")
                ok = False
        # Caso 3: El identificador no está registrado
        else:
            print(f"Error: No se encontró el dispositivo {identificador}. Es posible que ya haya sido eliminado.")
            ok = False
        # Si se eliminó correctamente, borramos del CSV
        if ok and dispositivo:
            self.borrar_de_csv(dispositivo.id)