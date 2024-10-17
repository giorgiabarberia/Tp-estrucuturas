from class_celular import Celular
from class_central import Central

class Operadora:
    def __init__(self,nombre):
        self.nombre = nombre
        
    def registrar_celular(self,celular:Celular):
        if celular.numero in Central.celulares_registrados:
            print(f'Error: El número {celular.numero} ya está registrado.')
        else:
            Central.celulares_registrados[celular.numero] = celular
            print(f'Celular {celular.numero} registrado con éxito.')
    
    def eliminar_celular(self,numero):
        if numero in Central.celulares_registrados:
            del Central.celulares_registrados[numero]
            print(f'Celular {numero} eliminado con éxito.')
        else:
            print(f'Error: No se encontró el celular {numero}')