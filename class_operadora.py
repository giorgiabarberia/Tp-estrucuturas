
from class_celular import Celular
from class_central import Central
import validaciones
import random
import string

class Operadora:
    def __init__(self,nombre):
        self.nombre = nombre
        self.central = Central()

    # Función para generar un número de celular válido, que no esté ya en la central
    @staticmethod
    def crear_numero_aleatorio() -> str:
        numero = "11" + ''.join(random.choices("0123456789", k=8))
        while numero in Central.celulares_registrados:
            numero = "11" + ''.join(random.choices("0123456789", k=8))
        return numero

    # Función para generar un ID para los celulares que sea único. 
    @staticmethod
    def generar_id_unico(longitud=25) -> str:
        caracteres = string.ascii_letters + string.digits
        id = ''.join(random.choice(caracteres) for _ in range(longitud))
        while True:
            if id not in Central.ids_registrados:
                return id

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
        Central.ids_registrados[celular.id] = celular
        Central.celulares_registrados[celular.numero] = celular
        celular.asignar_sms_telefono(self.central)
        print(f'Celular registrado con éxito.\nSu número es: {celular.numero}')

    def eliminar_celular(self,numero):
        if numero in Central.celulares_registrados:
            cel = Central.celulares_registrados[numero]
            mail = cel.direcc_email 
            del Central.celulares_registrados[numero]
            Celular.eliminar_mail_celular(mail)
            print(f'Celular {numero} eliminado con éxito.')
        else:
            print(f'Error: No se encontró el celular {numero}, no estaba registrado en la central,\nEs posible que ya haya sido eliminado')

