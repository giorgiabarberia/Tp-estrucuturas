from collections import deque
import datetime
from class_celular import Celular
from class_central import Central

central = Central()

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
    
    # Elimina el último mensaje recibido
    def eliminar_mensaje_entrada(self):  
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
    def __init__(self, celular:Celular):
        super().__init__()
        self.chats = {}  
        self.celular = celular
        self.num_remitente = celular.numero

    def obtener_nombre_o_num(self,numero):
        return self.celular.agenda_contactos.get(numero,numero)
    
    def buscar_num_por_nombre(self, nombre):
        return self.celular.agenda_contactos.get(nombre)

    # Función para enviar un mensaje, se agrega a la bandeja de salida
    def enviar_sms(self, num_destino, texto):
        if num_destino not in self.chats:
            self.chats[num_destino] = deque()
        mensaje = f'Yo: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_destino].append(mensaje)

    def recibir_mensaje(self, num_remitente, texto):
        if num_remitente not in self.chats:
            self.chats[num_remitente] = deque()     #Pila con mensajes recibidos
        mensaje = f'{num_remitente}: {texto} 1 [{self.obtener_hora_actual()}]'
        self.chats[num_remitente].append(mensaje)
    
    def eliminar_mensaje(self, num_destino, num_mensaje_a_elim):
        if num_destino not in self.chats:
            print('Chat no encontrado')
        self.chats[num_destino][num_mensaje_a_elim] = 'Mensaje eliminado'
        
    def ejecutar_sms(self):
        print('\n---SMS---')
        for numero in self.chats.keys():
            nombre = self.obtener_nombre_o_num(numero)
            print(f'- {nombre}')
        while True:
            print('Elegir chat de SMS:\n1. Por contacto\n2.Por número telefónico\nSalir')
            opcion = print('Seleccione una opción: ').strip()
            if opcion == '1':
                nombre = input('Abrir chat con: ').strip()
                numero = self.buscar_num_por_nombre(nombre)
                if not numero:
                    print(f'No se encontró el contacto {nombre}')
                    return
            elif opcion == '2': ###VALIDAR QUE EL NUMERO EXISTA
                numero = input('Enviar mensaje al número: ').strip()
                if not 
            elif opcion == '3':
                break
            else:
                print('Opción Inválida. Por favor intente nuevamente.')
        for mensaje in self.chats[numero]:
            print(mensaje)
        while True:
            print('1. Enviar un mensaje\n2.Eliminar un mensaje\n3.Salir')
            opcion = print('Seleccione una opcion: ').strip()
            if opcion == '1':
                texto = input('Mensje: ')
                if central.enviar_sms(self.num_remitente,numero,texto):
                    self.enviar_mensaje(numero,texto)
                    ##HACER QUE EL OTRO NÚMERO LO RECIBA
            
                

   
   
   
        


# Clase Email (herencia de Mensajería)
class Email(Mensajeria):
    def __init__(self, email_remitente):
        self.bandeja_entrada=deque()
        self.bandeja_salida=deque()
        #self.email_remitente = email_remitente
        #self.leido = False
    
     # Agrega un mensaje a la bandeja de salida
    def enviar_email(self, remitente, destino, contenido):
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
  
    # Función para enviar un email, se agrega a la bandeja de salida
    #def enviar_email(self, email_destino, asunto, cuerpo):
        #mail = f'Asunto: {asunto}\n{cuerpo}'
        #self.enviar_mensaje(self.email_remitente, email_destino, mail) 
 

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

    