from datetime import datetime

# Clase Central
class Central:
    ids_registrados = {}
    celulares_registrados = {}  # Diccionario de celulares registrados por número
    registros = []  # log PREGUNTAR COMO SE USA (actividad, lista de registros de celualres)

    # Para verificar si un celular está disponible (encendido y con red móvil activa)
    def verif_disponibilidad(self, numero):
        celu = self.celulares_registrados.get(numero)
        if celu and celu.prendido and celu.configuracion.red_movil:
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
            if self.verif_disponibilidad(num_remitente) and self.celular_registrado(num_destino):
                
                remitente_celu = self.celulares_registrados[num_remitente]
                destino_celu = self.celulares_registrados[num_destino]

                remitente_celu.sms.enviar_sms(num_destino,texto)
                destino_celu.sms.recibir_sms(num_remitente,texto)
                id = len(self.registros)
                self.registros.append({
                    'ID': id,
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
    def llamar (self,num_remitente,num_destino):
        if not self.verif_disponibilidad(num_remitente):
            print(f'Error: El celular no está disponible.')
            return False
        remitente_celu = self.celulares_registrados[num_remitente]
        if remitente_celu.en_llamada:
            print('Error: Ya estás en una llamada.')
            return False
        if not self.celular_registrado(num_destino):
            print(f'Error: El número {num_destino} no está registrado.')
            return False
        if not self.verif_disponibilidad(num_destino):
            print(f'Error: El número {num_destino} no está disponible.')
            return False
        
        destino_celu = self.celulares_registrados[num_destino]
        if destino_celu.en_llamada:
            print(f'Error: {num_destino} se encuentra ocupado')
            return False
        
        print(f'Llamando a {num_destino}...')
        hora_inicio = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        destino_celu.telefono.llamadas_entrantes.append(f'{remitente_celu}')
        return True
        
       



