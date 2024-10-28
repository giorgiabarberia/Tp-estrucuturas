from collections import deque
from datetime import datetime
from class_central import Central
import validaciones 
from exportador import ExportadorLlamada

## Clase Telefono
class Telefono:
    def __init__(self, id_celular, central: Central):
        self.celular = central.obtener_celu_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central
        self.llamadas_entrantes = deque()  # Cola de llamadas entrantes
        self.llamada_activa_con = None
        self.hora_inicio_llamada = None
        self.hora_fin_llamada = None

    def realizar_llamada(self):   
        num_destino = input('\nIngrese el número al que desea llamar: ')
        if self.central.llamar(self.num_remitente, num_destino):
            self.celular.en_llamada = True
            print(f'Llamando a {num_destino}...')
        #### else: error....
        
    def ver_llamadas_entrantes(self):
        if not self.llamadas_entrantes:
            return
        print('\nLlamadas entrantes:')
        for i, celu in enumerate(self.llamadas_entrantes, start=1):
            print(f'{i}. 📲 {celu.numero}')
            
    def contestar_llamada(self):
        if not self.llamadas_entrantes:
            print('No hay llamadas entrantes para contestar.')
            return
        # Atender siempre la primera llamada en la cola
        self.celular.en_llamada = True
        celu_remitente = self.llamadas_entrantes.popleft()  # Eliminar y obtener la primera llamada
        self.llamada_activa_con = celu_remitente
        celu_remitente.telefono.llamada_activa_con = self.celular
        print(f'Llamada en curso con {celu_remitente.numero}...')
        self.hora_inicio_llamada = datetime.now()
        
            

    def colgar(self):
        if not self.celular.en_llamada:
            print('\nNo hay llamada en curso.')
            return
        celu_destino = self.llamada_activa_con
        if celu_destino:
            self.celular.en_llamada = False
            celu_destino.en_llamada = False
            self.llamada_activa_con = None
            celu_destino.telefono.llamada_activa_con = None
            print('\nLlamada finalizada.')

            self.hora_fin_llamada = datetime.now()
            duracion = self.hora_fin_llamada - self.hora_inicio_llamada
            self.central.registrar_llamada(self.num_remitente, celu_destino.numero, self.hora_inicio_llamada, self.hora_fin_llamada, duracion)
        else:
            self.celular.en_llamada = False
        
    def ejecutar_llamadas_entrantes(self):
        ver_llamadas = True
        while ver_llamadas:
            self.ver_llamadas_entrantes()
            if self.llamadas_entrantes:
                celu_remitente = self.llamadas_entrantes[0]  # Siempre toma la primera llamada en la cola
                print(f'\n📲Llamada de {celu_remitente.numero} está esperando.')
                        
                # Opciones para la primera llamada en la cola
                print('\n1. Atender\n2. Colgar sin atender\n3. Volver')
                subopcion = input('Seleccione una opción: ').strip()

                if subopcion == '1':
                    self.contestar_llamada()  # Atender la primera llamada
                elif subopcion == '2':
                    print(f'Llamada de {celu_remitente.numero} colgada sin atender.')
                    del self.llamadas_entrantes[0]  # Eliminar la primera llamada de la cola
                elif subopcion == '3':
                    ver_llamadas = False  # Volver sin hacer nada
                else:
                    print('Opción inválida. Intente nuevamente.')
            else:
                print('No hay llamadas entrantes en este momento.')
                ver_llamadas = False  # No hay llamadas entrantes

    def ver_historial_llamadas (self):
        if not self.central.registros_llamadas:
            return 'Historial de llamadas vacío.'
        print('\n--- Historial de Llamadas ---')
        for i, llamada in enumerate(self.central.registros_llamadas, start=1):
            print(f"{i}. {llamada['Tipo']} - De: {llamada['Remitente']} a: {llamada['Destinatario']} - Inicio: {llamada['Hora de inicio']} - Fin: {llamada['Hora de fin']} -  Duración: {llamada['Duración']}")

    def ejecutar_telefono(self):
        ejecutando = True
        while ejecutando:
            print('\n------TELÉFONO------')
            print('1. 📞 Realizar llamada\n2. ☎️  Finalizar llamada\n3. 📖  Ver historial de llamadas\n4. Salir')
            opcion = input('Seleccione una opción: ').strip()

            if opcion == '1':
                self.realizar_llamada()

            elif opcion == '2':
                self.colgar()
            elif opcion=='3':
                self.ver_historial_llamadas()
            elif opcion == '4':
                print('\nSaliendo de Teléfono...')
                exportador = ExportadorLlamada("registros_llamadas.csv")
                exportador.exportar(self.central.registros_llamadas)
                ejecutando = False

            else:
                print('Opción inválida. Intente nuevamente.')