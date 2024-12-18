from collections import deque
from datetime import datetime
from central import Central
from exportador import ExportadorChats
from listaenlazada import Nodo,ListaEnlazada
import validaciones


# Clase SMS 
class SMS():
    def __init__(self, id_celular, central: Central):
        self.chats = {}
        self.bandeja_entrada = {}  # Para cuando el celular está apagado
        self.celular = central.obtener_dispos_por_id(id_celular)
        if self.celular is None:
            raise ValueError('Error: Celular no encontrado en la central.')
        self.num_remitente = self.celular.numero
        self.central = central

    # Devuelve el nombre de contacto de un número o el número si no está agendado
    def obtener_nombre_o_num(self, numero):
        for num, nombre in self.celular.contactos.agenda_contactos.items():
            if num == numero:
                return nombre
        return numero

    # Se agrega el mensaje en el chat del que lo envía 
    def enviar_sms(self, num_destino, texto):
        if num_destino not in self.chats:
            self.chats[num_destino] = ListaEnlazada()   #Lista enlazada para los mensajes en un chat
        mensaje = f'Yo: {texto} | [{validaciones.obtener_fecha_actual()}]'
        self.chats[num_destino].agregarFinal(Nodo(mensaje))

    # Se agrega el mensaje en el chat del que lo recibe
    def recibir_sms(self, num_remitente, texto):
        mensaje = f'{self.obtener_nombre_o_num(num_remitente)}: {texto} | [{validaciones.obtener_fecha_actual()}]'
        if self.celular.prendido:
            if num_remitente not in self.chats:
                self.chats[num_remitente] = ListaEnlazada() #Lista enlazada para los mensajes en un chat
            self.chats[num_remitente].agregarFinal(Nodo(mensaje))
        else:
            if num_remitente not in self.bandeja_entrada:
                self.bandeja_entrada[num_remitente] = ListaEnlazada()
            self.bandeja_entrada[num_remitente].agregarFinal(Nodo(mensaje))

    # Muestra todos los mensajes con una persona (con un índice)
    def mostrar_chat(self, numero):
        nombre = self.obtener_nombre_o_num(numero)
        print(f'--- Chat con {nombre} ---')
        if numero not in self.chats or not self.chats[numero]:
            print('No hay mensajes en este chat.')
        else:
            for i, mensaje in enumerate(self.chats[numero], start=1):
                print(f'{i}. {mensaje}')

    # Eliminar un mensaje a partir de su índice (se elimina sólo en el celular de la persona)
    def eliminar_mensaje(self, num_destino, num_mensaje_a_elim):
        if num_destino not in self.chats:
            print('Chat no encontrado')
        elif 1 <= num_mensaje_a_elim <= len(self.chats[num_destino]):
            # Recorremos la lista enlazada hasta llegar al índice deseado
            aux = self.chats[num_destino].inicio
            for _ in range(num_mensaje_a_elim - 1):
                aux = aux.siguiente
            # Al llegar al nodo deseado, lo modificamos
            if aux:
                aux.dato = f'Mensaje eliminado | [{validaciones.obtener_fecha_actual()}]'
                print('Mensaje eliminado correctamente.')
        else:
            print('Número de mensaje inválido.')

    # Llama a la función de la central para que envíe el mensaje
    def enviar_nuevo_sms(self, num_destino):
        texto = input('Mensaje: ')
        if texto:
            if self.central.enviar_sms(self.num_remitente, num_destino, texto):
                print('Mensaje enviado correctamente.')
                self.central.registrar_sms(self.num_remitente, num_destino, texto)
            else:
                print('No se pudo enviar el mensaje. Verifica disponibilidad.')
        else:
            print('No se puede enviar un mensaje vacío.')
            
    # Muestra los chats existentes con el último mensaje
    def mostrar_chats_existentes(self):
        print('\n--- Chats Existentes ---')
        for i, (numero, mensajes) in enumerate(self.chats.items(), start=1):
            nombre = 'Yo' if numero == self.num_remitente else self.obtener_nombre_o_num(numero)
            ultimo_mensaje = mensajes.obtener_ultimo()
            remitente = 'Yo' 
            if 'Yo:' in ultimo_mensaje or numero == self.num_remitente:
                remitente = 'Yo'
            else: 
                remitente = nombre
            texto_mensaje = ultimo_mensaje.split('|')[0].split(': ')[-1]
            fecha_hora = ultimo_mensaje.split('|')[1].strip()
            print(f'{i}. {nombre} - [{remitente}: {texto_mensaje} - {fecha_hora} ]')

    def actualizar_chats(self):
        if self.bandeja_entrada:
            for num_remitente, mensajes in self.bandeja_entrada.items():
                if num_remitente not in self.chats:
                    self.chats[num_remitente] = ListaEnlazada()
                # Transferir todos los mensajes a la cola de chats
                self.chats[num_remitente].extend(mensajes)
            self.bandeja_entrada.clear()  # Ya se prendió el celular
     
    # Ejecutar la aplicación de SMS
    def ejecutar_sms(self):
        continuar = True
        while continuar:
            print('\n----- SMS -----')
            if self.celular.prendido and self.celular.configuracion.red_movil:
                self.actualizar_chats()
            if self.chats:
                self.mostrar_chats_existentes()
                print('\n📞 Opciones:')
                print('1. Elegir chat por indice: ')
                print('2. Abrir nuevo chat: ')
                print('3. Salir')
            else:
                print('\nNo hay chats existentes.')
                print('\n📞 Opciones:')
                print('1. Abrir nuevo chat')
                print('2. Salir')
                
            opcion = input('Seleccione una opción: ').strip()

            if opcion == '1' and self.chats:
                chat_num = input('Ingrese el indice del chat: ').strip()
                if chat_num.isdigit() and 1 <= int(chat_num) <= len(self.chats):
                    numero = list(self.chats.keys())[int(chat_num) - 1]
                    self.mostrar_y_manejar_chat(numero)
                else:
                    print('Número de chat inválido.')
            elif (opcion == '2' and self.chats) or (opcion == '1' and not self.chats):
                destino = input('Ingrese el número o nombre del contacto: ').strip()
                if destino in self.celular.contactos.agenda_contactos.values():
                    numero = self.celular.contactos.buscar_num_por_nombre(destino)
                    self.mostrar_y_manejar_chat(numero)
                elif destino in self.central.celulares_registrados.keys():
                    self.mostrar_y_manejar_chat(destino)
                else:
                    print('Número o contacto inválido.')
            elif (opcion == '3' and self.chats) or (opcion == '2' and not self.chats):
                print('Saliendo de SMS...')
                continuar = False
            else:
                print('Opción inválida. Intente nuevamente.')

    # Mostrar y manejar chat
    def mostrar_y_manejar_chat(self, numero):
        continuar = True
        while continuar:
            self.mostrar_chat(numero)
            print('\nOpciones:')
            print('1. Mandar nuevo mensaje')
            if numero in self.chats:
                print('2. Eliminar mensaje')
            print('3. Salir')
            sub_opcion = input('Seleccione una opción: ').strip()
            
            if sub_opcion == '1':
                self.enviar_nuevo_sms(numero)
            elif sub_opcion == '2' and numero in self.chats:
                try:
                    num_mensaje_a_elim = int(input('Indice del mensaje que desea eliminar: '))
                    self.eliminar_mensaje(numero, num_mensaje_a_elim)
                except ValueError:
                    print('Error. Ingrese un número válido.')
            elif sub_opcion == '3':
                continuar = False
                exportador = ExportadorChats("registros_chats.csv")
                exportador.exportar(self.central.registros_chats)
            else:
                print('Opción inválida. Intente nuevamente.')
                
                
#Clase Email 
class Email():
    def __init__(self, direcc_email):
        self.bandeja_entrada = deque() #Pila para la bandeja de entrada
        self.bandeja_salida = deque() #Pila para la bandeja de salida
        self.email_remitente = direcc_email

    #Agrega un email a la bandeja de salida y a la bandeja de entrada de quien lo recibe 
    def enviar_email(self,central:Central):
        print("\nMensaje nuevo")
        destino = input("Para: ").strip()
        asunto = input("Asunto: ").strip()
        cuerpo = input("Cuerpo: ").strip()
        mensaje = {
            "Remitente": self.email_remitente,
            "Destinatario": destino,
            "Asunto": asunto,
            "Cuerpo": cuerpo,
            "Fecha": datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        }
        if central.verif_mail(destino):  # Verifica que el e-mail exista en la central
            if asunto or cuerpo:
                self.bandeja_salida.append(mensaje)
                dispositivo_destino = central.obtener_dispositivo_por_email(destino)
                dispositivo_destino.email.recibir_email(self.email_remitente, destino, asunto, cuerpo)
                print('¡Email enviado!')
            else:
                print('No puedes enviar un email sin ningún contenido.')
        else:
            print('Dirección de email no encontrada.')
            
    #Agrega un mensaje a la bandeja de entrada
    def recibir_email(self, remitente, destino, asunto,cuerpo):
        mensaje = {
            'Remitente': remitente,
            'Destino': destino,
            'Asunto': asunto,
            'Cuerpo': cuerpo,
            'Fecha': validaciones.obtener_fecha_actual(),
            'Leído': False  #Se marca como no leído
        }
        self.bandeja_entrada.append(mensaje)

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
    def mostrar_bandeja(self, bandeja,nombre_bandeja):
        if not bandeja:
            print(f'La {nombre_bandeja} está vacía.')
        else:
            for i, email in enumerate(bandeja, start=1):
                print(f'{i}. 📧 {email["Remitente"]}\n{email["Asunto"]} | [{email["Fecha"]}]')
    
    def ejecutar_email(self,central):
        continuar = True
        while continuar:
            print('\n-----EMAIL-----')
            print('\n1. ✏️  Redactar\n2. 📥 Recibidos\n3. ➡️  Enviados\n4. Salir')
            opcion = input('Seleccione una opción: ')

            # Opciones principales del menú de email
            if opcion == '1':
                self.enviar_email(central)
            elif opcion == '2':
                self._mostrar_bandeja_entrada()
            elif opcion == '3':
                self._mostrar_bandeja_salida()
            elif opcion == '4':
                print('Saliendo de Email...')
                continuar = False
            else:
                print('Opción inválida. Intente nuevamente.')
            
    def _mostrar_bandeja_entrada(self):
        cont2 = True
        while cont2:
            print('\n---Bandeja de entrada---')
            self.mostrar_bandeja(self.bandeja_entrada, "bandeja de entrada")

            if self.bandeja_entrada:
                print('\n1. Aplicar filtro: No leídos primero\n2. Aplicar filtro: Por fecha\n3. Abrir email\n4. Volver')
                subopcion = input('Seleccione una opción: ')

                if subopcion == '1':
                    self.mostrar_emails_noleidos()
                elif subopcion == '2':
                    self.mostrar_emails_por_fecha()
                elif subopcion == '3':
                    self._abrir_email(self.bandeja_entrada)
                elif subopcion == '4':
                    cont2 = False
                else:
                    print('Opción inválida. Intente nuevamente.')
            else:
                self._volver_a_menu("V", "\nPresione 'V' para volver al menú de email: ")
                cont2 = False
    
    def _mostrar_bandeja_salida(self):
        cont3 = True
        while cont3:
            print('\n---Bandeja de salida---')
            self.mostrar_bandeja(self.bandeja_salida, "bandeja de salida")

            if self.bandeja_salida:
                print('\n1. Abrir un email\n2. Volver')
                subopcion = input('Seleccione una opción: ')

                if subopcion == '1':
                    self._abrir_email(self.bandeja_salida)
                elif subopcion == '2':
                    cont3 = False
                else:
                    print('Opción inválida. Intente nuevamente.')
            else:
                self._volver_a_menu("V", "\nPresione 'V' para volver al menú de email: ")
                cont3 = False
    
    def _abrir_email(self, bandeja):
        try:
            indice = int(input('Seleccione un email: '))
            self.abrir_un_email(indice, bandeja)
            self._volver_a_menu("V", "\nPresione 'V' para volver: ")
        except ValueError:
            print('Error: Ingrese un número de email válido.')

    def _volver_a_menu(self, opcion_esperada, mensaje):
        continuar = True
        while continuar:
            volver = input(mensaje).upper()
            if volver == opcion_esperada:
                continuar = False