from collections import deque
from datetime import datetime
from class_central import Central
from validaciones import validar_telefono

##Clase Telefono
class Telefono():
    def init(self, id_celular, central:Central):
        self.celular = central.obtener_celu_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central

    def realizar_llamada(self):   
        self.celular.en_llamada=True
        numero = input('Ingrese el numero al que desea llamar: ')
        while not validar_telefono(numero):
            numero = input('Nro incorrecto, intente nuevamente: ')
        if numero.en_llamada:
            return f'El numero {numero} se encuentra ocupado'
        numero.en_llamada = True
        print(f'Llamando a {numero}...')
        return numero

    def recibir_llamada(self,num_remitente):
        print(f'Llamada entrante del numero {num_remitente}')
        contestar = input('¿Desea contestar?(si/no)').strip().lower()
        return contestar

    def colgar(self,nro):
        if self.celular.en_llamada and nro.en_llamada:
            self.celular.en_llamada = False
            nro.en_llamada = False

