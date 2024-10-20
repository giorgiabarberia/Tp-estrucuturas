from datetime import datetime

# Clase Central
class Central:
    ids_registrados = {}
    celulares_registrados = {}  # Diccionario de celulares registrados por número
    registros = []  # log PREGUNTAR COMO SE USA (actividad, lista de registros de celualres)

    # Para verificar si un celular está disponible (encendido y con red móvil activa)
    def verif_disponibilidad(self, numero):
        celu = self.celulares_registrados.get(numero)
        if celu and celu.prendido and celu.red_movil:
            return True
        print(f'{numero} no se encuentra disponible.')
        return False
    
    # Para validar que el numero destinatario este registrado en la central
    def celular_registrado(self,numero):
        return numero in self.celulares_registrados
    
    # Si el remitente esta disponible pero el destinatario no se deberia almacenar en algun lado???
    # Para enviar un SMS de un remitente a un destinatario si ambos están disponibles
    def enviar_sms(self,num_remitente,num_destino,texto):
        if self.celular_registrado(num_destino):
            if self.verif_disponibilidad(num_remitente) and self.verif_disponibilidad(num_destino):
                
                remitente_celu = self.celulares_registrados[num_remitente]
                destino_celu = self.celulares_registrados[num_destino]

                remitente_celu.sms.enviar_sms(num_destino,texto)
                destino_celu.sms.recibir_sms(num_remitente,texto)

                self.registros.append({
                    'Tipo': 'SMS',
                    'Remitente': num_remitente,
                    'Destinatario': num_destino,
                    'Fecha': datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
                })
                return True
            else:
                print('Error: Verificar conexión a la red móvil.')
        else:
            print('Error: El número destinatario no está registrado.')
        return False
    
    def obtener_celu_por_id(self,id):
        celular = self.ids_registrados.get(id)
        if celular:
            return celular
        else:
            print('Error: celular no encontrado.')
            return None
        
    def obtener_celu_por_email(self,direcc_email):
        for celular in self.celulares_registrados.values():
            if celular.direcc_email == direcc_email:
                return celular
        return None

##Inicia el proceso de llamada entre dos celulares
def llamar (self,num_remitente):
        if self.verif_disponibilidad(num_remitente):
            remitente_celu = self.celulares_registrados[num_remitente]
            num_destino = remitente_celu.telefono.realizar_llamada()
            if self.celular_registrado(num_destino):
                if self.verif_disponibilidad(num_destino):
                    destino_celu = self.celulares_registrados[num_destino]

                    remitente_celu.telefono.realizar_llamada()
                    contestar = destino_celu.telefono.recibir_llamada(num_remitente)

                    if contestar == 'si':
                        hora_inicio = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
                        hora_fin = None
                        colgar = False
                        while not colgar:
                            print('Llamada en curso...')
                            colgar = destino_celu.telefono.colgar()
                        hora_fin = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

                    if contestar == 'no':
                        pass



