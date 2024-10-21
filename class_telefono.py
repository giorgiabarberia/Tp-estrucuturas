from collections import deque
from datetime import datetime
from class_central import Central
from validaciones import validar_telefono

##Clase Telefono
class Telefono():
    def __init__(self, id_celular, central:Central):
        self.celular = central.obtener_celu_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central
        self.llamadas_entrantes = deque()
        self.llamada_activa_con = None

    def realizar_llamada(self):   
        num_destino = input('Ingrese el número al que desea llamar: ') 
        if self.central.llamar(self.num_remitente,num_destino):
            self.celular.en_llamada = True
        
    def ver_llamadas_entrantes(self):
        if not self.llamadas_entrantes:
            print('No hay llamadas entrantes.')
            return None
        print('\nLlamadas entrantes:')
        for i, celu in enumerate(self.llamadas_entrantes,start=1):
            print(f'{i}. {celu.numero}')

    def contestar_llamada(self):
        llamada = int(input('Contestar: '))
        if 1<=llamada<=len(self.llamadas_entrantes):
            self.celular.en_llamada = True
            celu_remitente = self.llamadas_entrantes.pop(llamada-1)
            self.llamada_activa_con = celu_remitente
            celu_remitente.telefono.llamada_activa_con = self.celular


    def colgar(self):
        if self.celular.en_llamada:
            self.celular.en_llamada = False
        else:
            print('No hay llamada en curso.')
            return False
        
    def ejecutar_telefono(self):
        while True:
            print('-----TELÉFONO------')
            print('1. Realizar llamada\n2. Finalizar llamada\n3. Ver llamadas entrantes\n4. Salir')
            opcion = input('Seleccione una opción: ').strip()

            if opcion == '1':
                self.realizar_llamada()

            elif opcion == '2':
                if self.celular.en_llamada:
                    self.colgar()
                else:
                    print('Error: No hay llamada en curso para finalizar.')

            elif opcion == '3':
                while True:
                    if self.ver_llamadas_entrantes():
                        print('\n1. Contestar llamada\n2. Volver')
                        subopcion = input('Seleccione una opción: ').strip()
                        if subopcion == '1':
                            self.contestar_llamada()
                        elif subopcion == '2':
                            break
                        else:
                            print('Opción inválida. Intente nuevamente.')

            elif opcion == '4':
                print('Saliendo de Teléfono...')
                break

            else:
                print('Opción inválida. Intente nuevamente.')