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
        self.llamada_activa = None

    def realizar_llamada(self):   
        num_destino = input('Ingrese el número al que desea llamar: ') 
        self.central.llamar(self.num_remitente,num_destino)
       
        
    def recibir_llamada(self,num_remitente):
        print(f'Llamada entrante del numero {num_remitente}')
        contestar = input('¿Desea contestar? (si/no): ').strip().lower()
        while contestar not in ['si','no']:
            contestar = input('¿Desea contestar? (si/no): ').strip().lower()
        if contestar == 'si':
            return True
        else:
            return False

    def colgar(self,celu_destino):
        if self.celular.en_llamada and celu_destino.en_llamada:
            colgar = input('¿Desea colgar? (si/no): ').strip().lower()
            if colgar=='si':
                print('Llamada finalizada.')
                return True
            else:
                return False
        else:
            print('No hay llamada en curso.')
            return False
        
    def ejecutar_telefono(self):
        while True:
            print('-----TELÉFONO------')
            print('1. Realizar llamada\n2. Finalizar llamada\n3. Salir')
            opcion = input('Seleccione una opción: ').strip()

            if opcion == '1':
                self.realizar_llamada()

            elif opcion == '2':
                if self.celular.en_llamada and self.llamada_activa:
                    celu_destino = self.central.celulares_registrados[self.llamada_activa]
                    self.colgar(celu_destino)
                else:
                    print('Error: No hay llamada en curso para finalizar.')
            elif opcion == '3':
                print('Saliendo de Teléfono...')
                break
            else:
                print('Opción inválida. Intente nuevamente.')
                
                    

                        


       
        

