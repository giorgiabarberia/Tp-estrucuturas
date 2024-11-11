from celular import Celular
from central import Central
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
    def guardar_celular(celular):
        try:
            with open('celulares.csv', "a", newline='') as archivo:  
                escritor = csv.writer(archivo)
                
                lista = [
                    celular.id,
                    celular.configuracion.nombre,
                    celular.modelo,
                    celular.sist_op,
                    celular.version,
                    celular.ram,
                    celular.almacenamiento,
                    celular.numero,
                    celular.direcc_email
                ]
                escritor.writerow(lista)  
        except IOError:
            print("Error al exportar archivo")
            raise IOError('Error al exportar el archivo')
        
    def registrar_celular(self):
        id = self.generar_id_unico()
        nombre = input('Ingrese su nombre: ')
        nombre = validaciones.ingreso_no_vacio(nombre)
        modelo = input('Ingrese el modelo del celular: ')
        modelo = validaciones.ingreso_no_vacio(modelo)
        sistema_operativo = input('Ingrese el sistema operativo de su celular: ')
        sistema_operativo = validaciones.ingreso_no_vacio(sistema_operativo)
        version = input('Ingrese la versión de su celular: ')
        version = validaciones.ingreso_no_vacio(version)
        cap_memoria_ram = input('Ingrese la capacidad de la memoria RAM de su celular: ')
        cap_memoria_ram = validaciones.ingreso_no_vacio(cap_memoria_ram)
        cap_almacenamiento = input('Ingrese la capacidad de almacenamiento de su celular: ')
        cap_almacenamiento = validaciones.ingreso_no_vacio(cap_almacenamiento)
        numero = self.crear_numero_aleatorio()
        mail = input('Ingrese su mail: ')
        while not validaciones.validar_email(mail) or mail in Celular.mails_usados:
            if not validaciones.validar_email(mail):
                mail = input('Ingrese un mail válido, el formato del ingresado no es válido: ')
            else: 
                mail = input('Ingrese un mail válido, el ingresado ya está en uso por otro celular: ')
        celular = Celular(id,nombre,modelo,sistema_operativo,version,cap_memoria_ram,cap_almacenamiento, numero,mail)
        Operadora.guardar_celular(celular)
        Operadora.central.ids_registrados[celular.id] = celular
        Operadora.central.celulares_registrados[celular.numero] = celular
        celular.asignar_sms_telefono(Operadora.central)
        print(f'Celular registrado con éxito.\nSu número es: {celular.numero}')

    def borrar_de_csv(numero):
        """Elimina un registro del archivo celulares.csv basado en el número de celular."""
        try:
            # Leer todos los registros excepto el que queremos eliminar
            celulares_actualizados = []
            with open('celulares.csv', "r", newline='') as archivo:
                lector = csv.reader(archivo)
                encabezado = next(lector)  # Leer el encabezado
                for fila in lector:
                    # Comparar `numero` en el archivo con el `numero` a eliminar
                    if fila[7] != numero:  # Suponiendo que `numero` está en la columna 8 (índice 7)
                        celulares_actualizados.append(fila)

            # Sobreescribir el archivo con los registros actualizados
            with open('celulares.csv', "w", newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(encabezado)  # Escribir encabezado
                escritor.writerows(celulares_actualizados)  # Escribir datos sin el celular eliminado

        except FileNotFoundError:
            print("Error: No se encontró el archivo 'celulares.csv'.")
        except IOError:
            print("Error al modificar el archivo 'celulares.csv'.")

    def eliminar_celular(self,numero):
        if numero in Operadora.central.celulares_registrados:
            cel = Operadora.central.celulares_registrados[numero]
            mail = cel.direcc_email 
            del Operadora.central.celulares_registrados[numero]
            Celular.eliminar_mail_celular(mail)
            print(f'Celular {numero} eliminado con éxito.')
        else:
            print(f'Error: No se encontró el celular {numero}, no estaba registrado en la central,\nEs posible que ya haya sido eliminado')
        self.borrar_de_csv(numero)