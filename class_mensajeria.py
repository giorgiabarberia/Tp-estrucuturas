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
    def __init__(self, celular:Celular, central):
        super().__init__()
        self.chats = {}  
        self.celular = celular
        self.num_remitente = celular.numero
        self.central = central

    #devuelve el nombre de contacto de un numero o el numero si no está agendado
    def obtener_nombre_o_num(self,numero):
        return self.celular.agenda_contactos.get(numero,numero)
    
    #a partir del nombre de contacto devuelve el numero
    def buscar_num_por_nombre(self, nombre):
        return self.celular.agenda_contactos.get(nombre)

    # se agrega el mensaje en el chat del que lo envia 
    def enviar_sms(self, num_destino, texto):
        if num_destino not in self.chats:
            self.chats[num_destino] = deque()
        mensaje = f'Yo: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_destino].append(mensaje)

    #se agrega el mensaje en el chat del que lo recibe
    def recibir_sms(self, num_remitente, texto):
        if num_remitente not in self.chats:
            self.chats[num_remitente] = deque()     #Pila con mensajes recibidos
        mensaje = f'{self.obtener_nombre_o_num(num_remitente)}: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_remitente].append(mensaje)
    
    #muestra todos los mensajes con una persona
    def mostrar_chat(self,numero):
        if numero not in self.chats:
            print('')
            return
        nombre = self.obtener_nombre_o_num(numero)
        print(f'---Chat con {nombre}---')
        for i,mensaje in enumerate(self.chats[numero]):
            print(f'{i+1}. {mensaje}')

    def eliminar_mensaje(self, num_destino, num_mensaje_a_elim):
        if num_destino not in self.chats:
            print('Chat no encontrado')
        if 0 <= num_mensaje_a_elim < len(self.chats[num_destino]):
            self.chats[num_destino][num_mensaje_a_elim] = 'Mensaje eliminado' 
            print('Mensaje eliminado correctamente.')
        else:  
            print('Número de mensaje inválido.')

    #llama a la funcion de la central para que envie el mensaje
    def enviar_nuevo_sms(self,num_destino):
        texto = input('Mensaje: ')
        if texto:
            if self.central.enviar_sms(self.num_remitente,num_destino,texto):
                print('Mensaje enviado correctamente.')
            else:
                print('No se pudo enviar el mensaje. Verifica disponibilidad.')
        else:
            print('No se puede enviar un mensaje vacío.')

    #todo en sms 
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
                    continue
                self.mostrar_chat(numero)
            elif opcion == '2': ###VALIDAR QUE EL NUMERO EXISTA
                numero = input('Enviar mensaje al número: ').strip()
                self.mostrar_chat(numero)
            elif opcion == '3':
                print('Saliendo de SMS...')
                break
            else:
                print('Opción Inválida. Por favor intente nuevamente.')
                continue

        while True:
            print('1. Enviar un mensaje\n2.Eliminar un mensaje\n3.Salir')
            sub_opcion = print('Seleccione una opcion: ').strip()
            if sub_opcion == '1':
                self.enviar_nuevo_sms(numero)
            elif sub_opcion == '2':
                try:
                    num_mensaje_a_elim = int(input('Número del mensaje que desea eliminar: '))
                    self.eliminar_mensaje(numero,num_mensaje_a_elim)
                except ValueError:
                    print('Error. Ingrese un número válido.')
            elif sub_opcion == '3':
                break
            else:
                print('Opción inválida. Intente nuevamente.')
                
            
                

   
   
   
        


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

    