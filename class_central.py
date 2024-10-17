import datetime
from class_mensajeria import SMS

# Clase Central
class Central:
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
                remitente = self.celulares_registrados[num_remitente]
                destino = self.celulares_registrados[num_destino]
                
                remitente.sms.enviar_sms(num_destino,texto)
                destino.sms.recibir_mensaje(num_remitente,num_destino,texto)

                self.registros.append({
                    'Tipo':'SMS',
                    'Remitente':num_remitente,
                    'Destino':num_destino,
                    'Contenido':texto,
                    'Fecha':datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
                })
                print(f'SMS enviado a {num_destino}')
                return True
            else:
                print('Error: Verificar conexión a la red móvil.')
        else:
            print('El numero destinatario no está registrado')
            



