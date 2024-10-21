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
        num_destino = input('\nIngrese el número al que desea llamar: ') 
        if self.central.llamar(self.num_remitente,num_destino):
            self.celular.en_llamada = True
        
    def ver_llamadas_entrantes(self):
        print('\nLlamadas entrantes:')
        if len(self.llamadas_entrantes)==0:
            return None
        for i, celu in enumerate(self.llamadas_entrantes,start=1):
            print(f'{i}. 📲 {celu.numero}')

    def contestar_llamada(self):
        llamada = int(input('Contestar: '))
        if 1<=llamada<=len(self.llamadas_entrantes):
            self.celular.en_llamada = True
            celu_remitente = self.llamadas_entrantes[llamada-1]
            self.llamada_activa_con = celu_remitente
            celu_remitente.telefono.llamada_activa_con = self.celular
            del self.llamadas_entrantes[llamada-1]
            print(f'Llamada en curso con {celu_remitente.numero}...')
        else:
            print('Selección inválida.')

    def colgar(self):
        if not self.celular.en_llamada:
            print('\nNo hay llamada en curso.')
            return False
        celu_destino = self.llamada_activa_con
        if celu_destino:
            self.celular.en_llamada = False
            celu_destino.en_llamada = False
            self.llamada_activa_con = None
            celu_destino.telefono.llamada_activa_con = None
            print('\nLlamada finalizada.')
        else:
            self.celular.en_llamada = False
        
    def ejecutar_telefono(self):
        while True:
            print('\n-----TELÉFONO------')
            print('1. 📞 Realizar llamada\n2. ☎️  Finalizar llamada\n3. 📲 Ver llamadas entrantes\n4. Salir')
            opcion = input('Seleccione una opción: ').strip()

            if opcion == '1':
                self.realizar_llamada()

            elif opcion == '2':
                self.colgar()

            elif opcion == '3':
                while True:
                    self.ver_llamadas_entrantes()
                    print('\n1. Contestar llamada\n2. Volver')
                    subopcion = input('Seleccione una opción: ').strip()
                    if subopcion == '1':
                        try:
                            self.contestar_llamada()
                        except ValueError:
                            print('\nOpción inválida. Ingresa el número de llamada.')
                    elif subopcion == '2':
                        break
                    else:
                        print('\nOpción inválida. Intente nuevamente.')

            elif opcion == '4':
                print('\nSaliendo de Teléfono...')
                break

            else:
                print('\nOpción inválida. Intente nuevamente.')