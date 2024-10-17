from collections import deque
import datetime

# Clase Mensajería
class Mensajeria:
    def __init__(self):
        self.bandeja_entrada = deque()  # Pila mensajes recibidos
        self.bandeja_salida = deque()   # Pila mensajes enviados

    # Devuelve la hora actual
    @staticmethod
    def obtener_hora_actual():
        return datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

    # Agrega un mensaje a la bandeja de salida
    def enviar_mensaje(self, remitente, destino, contenido):
        mensaje = {
            'Remitente': remitente,
            'Destino': destino,
            'Contenido': contenido,
            'Hora': self.obtener_hora_actual(),
            'Leido': False  # Se marca como no leído por defecto
        }
        self.bandeja_salida.append(mensaje)
    
    # Agrega un mensaje a la bandeja de entrada
    def recibir_mensaje(self, remitente, destino, contenido):
        mensaje = {
            'Remitente': remitente,
            'Destino': destino,
            'Contenido': contenido,
            'Hora': self.obtener_hora_actual(),
            'Leido': False  # Se marca como no leído
        }
        self.bandeja_entrada.append(mensaje)
    
    ## TENGO ENTENDIDO QUE TENEMOS QUE PODER ELEGIR QUE ELIMINAR
    # Elimina el último mensaje recibido
    def eliminar_mensaje_entrada(self):   #PREGUNTAR: ACA SUPONEMOS QUE ELIMINAMOS EL ULTIMO SOLO
        if self.bandeja_entrada:
            eliminado = self.bandeja_entrada.pop()
            print(f'Se eliminó el mensaje: {eliminado}')
        else:
            print('No hay mensajes en la bandeja de entrada.')
    
    # Elimina el último mensaje que se envió
    def eliminar_mensaje_salida(self):
        if self.bandeja_salida:
            eliminado = self.bandeja_salida.pop()
            print(f'Se eliminó el mensaje: {eliminado}')
        else:
            print('No hay mensajes en la bandeja de salida.')

    # Muestra la bandeja de entrada
    def mostrar_bandeja_entrada(self):
        if not self.bandeja_entrada:
            print('Bandeja de entrada vacía.')
        else:
            print('Bandeja de entrada:')
            for mensaje in self.bandeja_entrada:
                print(f'[{mensaje["Hora"]}] {mensaje["Remitente"]} | {mensaje["Contenido"]} | Leído: {mensaje["Leido"]}')

    # Muestra la bandeja de salida
    def mostrar_bandeja_salida(self):
        if not self.bandeja_salida:
            print('Bandeja de salida vacía.')
        else:
            print('Bandeja de salida:')
            for mensaje in self.bandeja_salida:
                print(f'[{mensaje["Hora"]}] {mensaje["Destino"]} | {mensaje["Contenido"]}')

# Clase SMS (herencia de Mensajería)
class SMS(Mensajeria):
    def __init__(self, num_remitente):
        super().__init__()
        self.num_remitente = num_remitente
    
    # Función para enviar un mensaje, se agrega a la bandeja de salida
    def enviar_sms(self, num_destino, texto):
        self.enviar_mensaje(self.num_remitente, num_destino, texto)

# Clase Email (herencia de Mensajería)
class Email(Mensajeria):
    def __init__(self, email_remitente):
        super().__init__()
        self.email_remitente = email_remitente
        self.leido = False
    
    # Función para enviar un email, se agrega a la bandeja de salida
    def enviar_email(self, email_destino:Mensajeria, asunto, cuerpo):
        mail = f'Asunto: {asunto}\n{cuerpo}'
        self.enviar_mensaje(self.email_remitente, email_destino, mail)

    #función para abrir un email y marcarlo como leído
    def ver_emails_noleidos(self):
        for mensaje in self.bandeja_entrada:
            if not mensaje['Leido']:
                mensaje['Leido'] = True
                print(f'Email de {mensaje["Remitente"]} abierto: {mensaje["Contenido"]}')
            return
        print('No hay mensajes no leídos.')
    
    #funcion para mostrar todos los emails no leidos (del primero al ultimo)
    def mostrar_emails_noleidos(self):
        for mensaje in self.bandeja_entrada:
            if mensaje['Leido'] == False:
                print(f'Email de {mensaje["Remitente"]} : {mensaje["Contenido"]}')
            return
        print('No hay mensajes no leídos.')

    # Esto seria una pila bien utilizada???
    # Función para mostrar todos los emails por fecha (del último al primero)
    def mostrar_emails_por_fecha(self):
        if not self.bandeja_entrada:
            print('Bandeja de entrada vacía.')
        else:
            print('Emails en bandeja de entrada (ordenados por fecha):')
            for mensaje in reversed(self.bandeja_entrada):
                print(f'Email de {mensaje["Remitente"]} - {mensaje["Hora"]}: {mensaje["Contenido"]}')

    