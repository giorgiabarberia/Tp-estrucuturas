from collections import deque
from datetime import datetime
from class_central import Central

# Clase Mensajería
class Mensajeria:
    def __init__(self):
        self.bandeja_entrada = deque()  # Pila mensajes recibidos
        self.bandeja_salida = deque()   # Pila mensajes enviados

    # Devuelve la hora actual
    @staticmethod
    def obtener_hora_actual():
        return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

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
    def __init__(self, id_celular, central:Central):
        super().__init__()
        self.chats = {}  
        self.celular = central.obtener_celu_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central

    #Devuelve el nombre de contacto de un número o el número si no está agendado
    def obtener_nombre_o_num(self,numero):
        for nombre, num in self.celular.agenda_contactos.items():
            if num == numero:
                return nombre
        return numero
    
    #A partir del nombre de contacto, devuelve el número de teléfono
    def buscar_num_por_nombre(self, nombre):
        return self.celular.agenda_contactos.get(nombre)

    #Se agrega el mensaje en el chat del que lo envía 
    def enviar_sms(self, num_destino, texto):
        if num_destino not in self.chats:
            self.chats[num_destino] = deque()   #Pila para los mensajes en un chat
        mensaje = f'Yo: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_destino].append(mensaje)

    #Se agrega el mensaje en el chat del que lo recibe
    def recibir_sms(self, num_remitente, texto):
        if num_remitente not in self.chats:
            self.chats[num_remitente] = deque()     #Pila para los mensajes en un chat
        mensaje = f'{self.obtener_nombre_o_num(num_remitente)}: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_remitente].append(mensaje)
    
    #Muestra todos los mensajes con una persona (con un índice)
    def mostrar_chat(self,numero):
        nombre = self.obtener_nombre_o_num(numero)
        print(f'---Chat con {nombre}---')
        if numero not in self.chats:
            return
        for i,mensaje in enumerate(self.chats[numero]):
            print(f'{i+1}. {mensaje}')

    #Eliminar un mensaje a partir de su índice (se elimina sólo en el celular de la persona)
    def eliminar_mensaje(self, num_destino, num_mensaje_a_elim):
        if num_destino not in self.chats:
            print('Chat no encontrado')
        if 1 <= num_mensaje_a_elim <= len(self.chats[num_destino]):
            self.chats[num_destino][int(num_mensaje_a_elim)-1] = 'Mensaje eliminado' 
            print('Mensaje eliminado correctamente.')
        else:  
            print('Número de mensaje inválido.')

    #Llama a la funcion de la central para que envie el mensaje
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
        numero = None
        while True:
            print('\n---SMS---')
            for numero in self.chats.keys():
                nombre = self.obtener_nombre_o_num(numero)
                print(f'📞 {nombre}')
            print('\nElegir chat de SMS:\n1. Por contacto\n2. Por número telefónico\n3. Salir')
            opcion = input('Seleccione una opción: ').strip()
            if opcion == '1':
                nombre = input('\nAbrir chat con: ').strip()
                numero = self.buscar_num_por_nombre(nombre)
                if not numero:
                    print(f'\nError: No se encontró el contacto {nombre}')
                    continue
                self.mostrar_chat(numero)
            elif opcion == '2': ###VALIDAR QUE EL NUMERO EXISTA
                numero = input('\nAbrir chat con: ').strip()
                self.mostrar_chat(numero)
            elif opcion == '3':
                print('\nSaliendo de SMS...')
                break
            else:
                print('\nOpción Inválida. Por favor intente nuevamente.')
                continue

            while True:
                print('\n1. Enviar un mensaje\n2. Eliminar un mensaje\n3. Salir')
                sub_opcion = input('Seleccione una opcion: ').strip()
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

    