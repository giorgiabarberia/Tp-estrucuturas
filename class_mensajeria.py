from collections import deque
from datetime import datetime
from class_central import Central

# Clase SMS 
class SMS():
    def __init__(self, id_celular, central:Central):
        super().__init__()
        self.chats = {}  
        self.bandeja_entrada = {}
        self.celular = central.obtener_celu_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central

    @staticmethod
    def obtener_hora_actual():
        return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

    #Devuelve el nombre de contacto de un número o el número si no está agendado
    def obtener_nombre_o_num(self,numero):
        for num, nombre in self.celular.contactos.agenda_contactos.items():
            if num == numero:
                return nombre
        return numero

    #Se agrega el mensaje en el chat del que lo envía 
    def enviar_sms(self, num_destino, texto):
        if num_destino not in self.chats:
            self.chats[num_destino] = deque()   #Pila para los mensajes en un chat
        mensaje = f'Yo: {texto} | [{self.obtener_hora_actual()}]'
        self.chats[num_destino].append(mensaje)

    #Se agrega el mensaje en el chat del que lo recibe
    def recibir_sms(self, num_remitente, texto):
        mensaje = f'{self.obtener_nombre_o_num(num_remitente)}: {texto} | [{self.obtener_hora_actual()}]'
        if self.celular.prendido:
            if num_remitente not in self.chats:
                self.chats[num_remitente] = deque()     #Pila para los mensajes en un chat
            self.chats[num_remitente].append(mensaje)
        else:
            if num_remitente not in self.bandeja_entrada:
                self.bandeja_entrada[num_remitente] = deque()
            self.bandeja_entrada[num_remitente].append(mensaje)

    #Muestra todos los mensajes con una persona (con un índice)
    def mostrar_chat(self,numero):
        nombre = self.obtener_nombre_o_num(numero)
        print(f'---Chat con {nombre}---')
        if numero not in self.chats:
            return
        for i,mensaje in enumerate(self.chats[numero],start=1):
            print(f'{i}. {mensaje}')

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

    def actualizar_chats(self):
        if self.bandeja_entrada:
            for num_remitente, mensajes in self.bandeja_entrada.items():
                if num_remitente not in self.chats:
                    self.chats[num_remitente] = deque()
                self.chats[num_remitente].extend(mensajes)
            self.bandeja_entrada.clear()

    #todo en sms 
    def ejecutar_sms(self):
        numero = None
        while True:
            print('\n-----SMS-----')
            if self.celular.prendido and self.celular.configuracion.red_movil:
                self.actualizar_chats()
            for numero in self.chats.keys():
                nombre = self.obtener_nombre_o_num(numero)
                print(f'📞 {nombre}')
            print('\nElegir chat de SMS:\n1. Por contacto\n2. Por número telefónico\n3. Salir')
            opcion = input('Seleccione una opción: ').strip()
            if opcion == '1':
                nombre = input('\nAbrir chat con: ').strip()
                numero = self.celular.contactos.buscar_num_por_nombre(nombre)
                if not numero:
                    print(f'\nError: No se encontró el contacto {nombre}')
                    continue
                self.mostrar_chat(numero)
            elif opcion == '2': 
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
                

#Clase Email 
class Email():
    def __init__(self, direcc_email):
        self.bandeja_entrada = deque()
        self.bandeja_salida = deque()
        self.email_remitente = direcc_email

    @staticmethod
    def obtener_fecha_actual():
        return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

    #Agrega un email a la bandeja de salida y a la bandeja de entrada de quien lo recibe 
    def enviar_email(self,central:Central):
        print('\nMensaje nuevo')
        destino = input('Para: ')
        asunto = input('Asunto: ')
        cuerpo = input('Cuerpo: ')
        mensaje = {
            'Remitente': self.email_remitente,
            'Destino': destino,
            'Asunto': asunto,
            'Cuerpo': cuerpo,
            'Fecha': self.obtener_fecha_actual(),
            'Leído': False  #Se marca como no leído por defecto
        }
        self.bandeja_salida.appendleft(mensaje) 

        celu_destino = central.obtener_celu_por_email(destino)
        if celu_destino:    #Aclaración: podemos enviar un mail a una dirección que no exista, pero a esta nunca le va a llegar el mail
            celu_destino.email.recibir_email(self.email_remitente,destino,asunto,cuerpo)
    
    #Agrega un mensaje a la bandeja de entrada
    def recibir_email(self, remitente, destino, asunto,cuerpo):
        mensaje = {
            'Remitente': remitente,
            'Destino': destino,
            'Asunto': asunto,
            'Cuerpo': cuerpo,
            'Fecha': self.obtener_fecha_actual(),
            'Leído': False  #Se marca como no leído
        }
        self.bandeja_entrada.appendleft(mensaje)

    #función para abrir un email y marcarlo como leído
    def abrir_un_email(self, indice, bandeja):
        if 1 <= indice <= len(bandeja):
            email = bandeja[indice-1]
            print(f"\n📧 {email['Remitente']} | [{email['Fecha']}]\nAsunto: {email['Asunto']}\n{email['Cuerpo']}")
            email['Leído'] = True
        else: 
            print('Email no encontrado.')

    #Función para mostrar los emails no leidos primero
    def mostrar_emails_noleidos(self):
        no_leidos = []
        leidos = []
        for email in self.bandeja_entrada:
            if not email['Leído']:
                no_leidos.append(email)
            else:
                leidos.append(email)
        print('\nFiltro: No leídos primero.')
        self.bandeja_entrada = no_leidos + leidos
        for i,email in enumerate(self.bandeja_entrada, start = 1):
            print(f'{i}. 📧 {email["Remitente"]}\n{email["Asunto"]} | [{email["Fecha"]}]')
            
    # Función para mostrar todos los emails por fecha (del último al primero)
    def mostrar_emails_por_fecha(self):
        print('\nFiltro: Por Fecha.')
        self.bandeja_entrada = sorted(self.bandeja_entrada, key=lambda e: e['Fecha'], reverse = True)
        for i,email in enumerate(self.bandeja_entrada, start = 1):
            print(f'{i}. 📧 {email["Remitente"]}\n{email["Asunto"]} | [{email["Fecha"]}]')

    #Función para mostrar la bandeja 
    def mostrar_bandeja(self,bandeja):
        for i,email in enumerate(bandeja,start=1):
            print(f'{i}. 📧 {email["Remitente"]}\n{email["Asunto"]} | [{email["Fecha"]}]')

    def ejecutar_email(self,central):
        while True:
            print('\n-----EMAIL-----')
            print('\n1. ✏️  Redactar\n2. 📥 Recibidos\n3. ➡️  Enviados\n4. Salir')
            opcion = input('Seleccione una opción: ')
            if opcion == '1':
                self.enviar_email(central)
            elif opcion == '2':
                print('\n---Bandeja de entrada---')
                self.mostrar_bandeja(self.bandeja_entrada)
                while True:
                    print('\n1. Aplicar filtro: No leídos primero\n2. Aplicar filtro: Por fecha\n3. Abrir email\n4. Volver')
                    subopcion = input('Seleccione una opción: ')
                    if subopcion == '1':
                        self.mostrar_emails_noleidos()
                    elif subopcion == '2':
                        self.mostrar_emails_por_fecha()
                    elif subopcion == '3':
                        try:
                            indice = int(input('Seleccione un email: '))
                            self.abrir_un_email(indice,self.bandeja_entrada)
                        except ValueError:
                            print('Error: Ingrese un número de email válido.')
                    elif subopcion == '4':
                        break
                    else:
                        print('Opción inválida. Intente nuevamente.')
            elif opcion == '3':
                print('\n---Bandeja de salida---')
                self.mostrar_bandeja(self.bandeja_salida)
                while True:
                    print('\n1. Abrir un email\n2. Volver')
                    subopcion = input('Selecciona una opción: ')
                    if subopcion == '1':
                        try:
                            indice = int(input('\nSeleccione un email: '))
                            self.abrir_un_email(indice,self.bandeja_salida)
                        except ValueError:
                            print('Error: Ingrese un número de email válido.')
                    elif subopcion == '2':
                        break
                    else: 
                        print('Opción inválida. Intente nuevamente.')
            elif opcion == '4':
                print('Saliendo de Email...')
                break
            else:
                print('Opción inválida. Intente nuevamente.')

        if not self.bandeja_entrada:
            print('Bandeja de entrada vacía.')
        else:
            print('Emails en bandeja de entrada (ordenados por fecha):')
            for mensaje in reversed(self.bandeja_entrada):
                print(f'Email de {mensaje["Remitente"]} - {mensaje["Hora"]}: {mensaje["Contenido"]}')

