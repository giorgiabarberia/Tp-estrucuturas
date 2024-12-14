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
                        'CelularNuevo',
                        dispositivo.id,
                        dispositivo.configuracion.nombre,
                        dispositivo.modelo,
                        dispositivo.sist_op,
                        dispositivo.version,
                        dispositivo.ram,
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
                        dispositivo.sist_ope,
                        dispositivo.version,
                        dispositivo.ram,
                        dispositivo.almacenamiento,
                        dispositivo.direcc_email
                    ]
                if isinstance(dispositivo,CelularAntiguo):
                    lista = [
                        'CelularAntiguo',
                        dispositivo.id,
                        dispositivo.configuracion.nombre,
                        dispositivo.modelo,
                        dispositivo.sist_op,
                        dispositivo.version,
                        dispositivo.ram,
                        dispositivo.almacenamiento,
                        dispositivo.numero
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
        modelo = input('Ingrese el modelo del celular: ')
        modelo = validaciones.ingreso_no_vacio(modelo)
        sistema_operativo = input('Ingrese el sistema operativo de su dispositivo: ')
        sistema_operativo = validaciones.ingreso_no_vacio(sistema_operativo)
        version = input('Ingrese la versión de su celular: ')
        version = validaciones.ingreso_no_vacio(version)
        cap_memoria_ram = input('Ingrese la capacidad de la memoria RAM de su celular: ')
        cap_memoria_ram = validaciones.ingreso_no_vacio(cap_memoria_ram)
        cap_almacenamiento = input('Ingrese la capacidad de almacenamiento de su celular: ')
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
            dispositivo = CelularNuevo(id,nombre,marca, modelo,sistema_operativo,version,cap_memoria_ram,cap_almacenamiento, numero,mail)
        elif tipo == "Celular Antiguo":
            dispositivo = CelularAntiguo(self, nombre, marca, modelo, sistema_operativo, version, cap_memoria_ram, cap_almacenamiento, id, numero)
        elif tipo == "Tablet":
            dispositivo = Tablet(nombre, marca, modelo, sistema_operativo, version, cap_memoria_ram, cap_almacenamiento,id)
        if tipo != "Tablet":
            Operadora.guardar_dispositivo(dispositivo)
            Operadora.central.ids_registrados[dispositivo.id] = dispositivo
            Operadora.central.celulares_registrados[dispositivo.numero] = dispositivo
            dispositivo.asignar_sms_telefono(Operadora.central)
            print(f'Celular registrado con éxito.\nSu número es: {dispositivo.numero}')
        else:
            print(f"Tablet registrada con éxito.\nIngese a ella con su email: {dispositivo.email}")


    def borrar_de_csv(id): 
        """Elimina un registro del archivo celulares.csv basado en el número de celular."""
        try:
            # Leer todos los registros excepto el que queremos eliminar
            dispositivos_actualizados = []
            with open('dispositivos.csv', "r", newline='') as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector)  # Leer el encabezado
                for fila in lector:
                    # Comparar `id` en el archivo con el `id` a eliminar
                    if fila[2] != id:  # Suponiendo que `id` está en la columna 8 (índice 7)
                        dispositivos_actualizados.append(fila)

            # Sobreescribir el archivo con los registros actualizados
            with open('celulares.csv', "w", newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(encabezado)  # Escribir encabezado
                escritor.writerows(dispositivos_actualizados)  # Escribir datos sin el celular eliminado

        except FileNotFoundError:
            print("Error: No se encontró el archivo 'dispositivos.csv'.")
        except IOError:
            print("Error al modificar el archivo 'dispositvos.csv'.")

    def eliminar_dispositivo(self,id):
        if id in Operadora.central.ids_registrados:
            dispositivo = Operadora.central.ids_registrados[id]
            if isinstance(dispositivo,CelularNuevo):
                mail = dispositivo.direcc_email 
                del Operadora.central.celulares_registrados[dispositivo.numero]
                Dispositivo.eliminar_mail(mail)
            if isinstance(dispositivo,CelularAntiguo):
                del Operadora.central.celulares_registrados[dispositivo.numero]
            if isinstance(dispositivo,Tablet):
                mail = dispositivo.direcc_email 
                Dispositivo.eliminar_mail(mail)
                
            print(f'Dispositivo {id} eliminado con éxito.')
        else:
            print(f'Error: No se encontró el dispositivo {id}, no estaba registrado en la operadora,\nEs posible que ya haya sido eliminado')
        self.borrar_de_csv(id)