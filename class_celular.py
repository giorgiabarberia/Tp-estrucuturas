from class_mensajeria import SMS,Email
from class_central import Central

central = Central()

# Función que valida que un número de teléfono sea válido
def validar_telefono(telefono: str) -> bool:
    return telefono.isdigit() and 10 <= len(telefono) <= 13

# Función para preguntar si desea continuar
def desea_continuar() -> bool:
    while True:
        cont = input('¿Desea continuar? (si o no): ').strip().lower()
        if cont in {'si', 'no'}:
            return cont == 'si'

class Celular:
    id_usados = set()
    numeros_usados = set()
    
    def __init__(self, id: int, nombre: str, modelo: str, sistema_operativo: str, version: str, cap_memoria_ram: str, cap_almacenamiento: str, numero: str, direcc_email: str = None):
        if not validar_telefono(numero):
            raise ValueError(f'Error: el número de teléfono {numero} no es válido.')
        if id in Celular.id_usados:
            raise ValueError(f'Error: el id ingresado ya está en uso.')
        if numero in Celular.numeros_usados:
            raise ValueError(f'Error: el número de teléfono ya está en uso.')
        
        self.id = id
        self.nombre = nombre
        self.modelo = modelo
        self.sist_op = sistema_operativo
        self.version = version
        self.ram = cap_memoria_ram
        self.almacenamiento = cap_almacenamiento
        self.numero = numero
        self.direcc_email = direcc_email
        self.prendido = False
        self.contraseña = None
        self.bloqueo = True
        self.red_movil = False
        self.datos = False
        self.en_llamada = False
        
        Celular.id_usados.add(id)
        Celular.numeros_usados.add(numero)

        self.sms = SMS(numero)
        self.email = Email(direcc_email) if direcc_email else None
        self.agenda_contactos = {}
        
    def __str__(self):
        return (f'Celular de {self.nombre}\nModelo: {self.modelo}\n'
                f'Sistema operativo: {self.sist_op}\nCapacidad de memoria RAM: {self.ram}\n'
                f'Capacidad de almacenamiento: {self.almacenamiento}\nNúmero telefónico: {self.numero}')
    
    #agrega contacto a la agenda_contactos (nombre:num)
    def agendar_contacto(self):
        nombre = input('Nombre del contacto: ')
        numero = input('Número de teléfono: ')
        if not validar_telefono(numero):
            print(f'Error: El número {numero} no es válido.')
            return
        if nombre in self.agenda_contactos:
            print(f'Error: El contacto {nombre} ya existe.')
        else:
            self.agenda_contactos[nombre] = numero
            print(f'Contacto {nombre} agendado con éxito.')

    #devuelve el número de un contacto  
    def buscar_num_por_nombre(self, nombre):
        return self.agenda_contactos.get(nombre)
    
    def buscar_celu_por_email(self, email):
        for celular in central.celulares_registrados.values():
            if celular.direcc_email == email:
                return celular
        print(f"No se encontró ningún celular registrado con el email {email}.")
        return None

    ## prendo el celular, y al prenderlo se ejecuta la funcion desbloquear
    def prender_celular(self):
        if self.prendido:
            print('El celular ya está prendido.')
        else:
            print('Prendiendo...')
            self.prendido = True
            self.desbloquear()
            self.activar_red_movil()
            
    ## apagar el celular
    def apagar_celular(self):
        print('Apagando...')
        self.prendido = False
        
    ## Activar la red movil
    def activar_red_movil(self):
        if self.red_movil:
            print('La red movil ya está activa.')
        else:
            print('Activando red movil...')
            self.red_movil = True
    
    ## Desactiva la red movil
    def desactivar_red_movil(self):
        if not self.red_movil:
            print('La red movil ya está desactivada.')
        else:
            print('Desactivando red movil...')
            self.red_movil = False
        
    ## Activar datos
    def activar_datos(self):
        if self.datos:
            print('Los datos celulares ya están activados')
        else:
            print('Activando datos...')
            self.datos = True
        
    ## Desactivar datos
    def desactivar_datos(self):
        if not self.datos:
            print('Los datos celulares ya están desactivados')
        else:
            print('Desactivando datos...')
            self.datos = False
        
    ## validar que el usuario sepa cual es su contraseña actual
    def validar_contraseña_actual(self) -> str:
        while True:
            ingreso = input('Ingrese la contraseña actual: ')
            if ingreso == self.contraseña:
                return ingreso
            print('Contraseña incorrecta.')
            if not desea_continuar():
                return ''
    
    ## desbloquear el celular automáticamente si no hay contraseña, si la hay usa validar_contraseña_actual
    def desbloquear(self):
        if self.contraseña:
            if self.validar_contraseña_actual():
                self.bloqueo = False
        else:
            self.bloqueo = False
    
    ## cambiar el nombre del usuario, valida que no sea muy largo y que exista     
    def cambiar_nombre(self):
        print(f'{self.nombre}, ud. va a cambiar su nombre')
        if desea_continuar():
            while True:
                nuevo = input('Ingrese un nuevo nombre: ').strip()
                if 0 < len(nuevo) <= 50:
                    self.nombre = nuevo
                    break
                print('Nombre inválido. Intente nuevamente.')
    
    ## Hace la acción de cambiar la contraseña
    def actualizar_codigo(self):
        while True:
            nuevo = input('Ingrese su nuevo código: ')
            validar = input('Ingrese su nuevo código nuevamente: ')
            if nuevo and nuevo == validar:
                self.contraseña = nuevo
                break
            print('No coinciden los códigos, intente nuevamente.')
    
    ## Si el usuario ya tiene contraseña, valida que la sepa, y luego llama a actualizar_codigo  
    def cambiar_codigo(self):
        if self.contraseña:
            if self.validar_contraseña_actual():
                self.actualizar_codigo()
            else:
                print('Lo lamentamos, no podrás cambiar tu código')
        else:
            self.actualizar_codigo()
            
    ## función de configuración
    def configuracion(self):
        opciones = {'1': 'Cambiar nombre','2': 'Cambiar código de desbloqueo','3': 'Datos','4': 'Red móvil','5': 'Salir'}
        while True:
            print("\nConfiguración:")
            for key, value in opciones.items():
                print(f"{key}. {value}")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                self.cambiar_nombre()
            elif opcion == '2':
                self.cambiar_codigo()
            elif opcion == '3':
                self.configurar_datos()
            elif opcion == '4':
                self.configurar_red_movil()
            elif opcion == '5':
                print("Saliendo de la configuración.")
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")
    
    ## configuración de datos
    def configurar_datos(self):
        while True:
            print("\nConfiguración de Datos:")
            print("1. Activar datos")
            print("2. Desactivar datos")
            print("3. Volver")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                self.activar_datos()
            elif opcion == '2':
                self.desactivar_datos()
            elif opcion == '3':
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")
    
    ## configuración de red móvil
    def configurar_red_movil(self):
        while True:
            print("\nConfiguración de Red Móvil:")
            print("1. Activar red móvil")
            print("2. Desactivar red móvil")
            print("3. Volver")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                self.activar_red_movil()
            elif opcion == '2':
                self.desactivar_red_movil()
            elif opcion == '3':
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")

    #menu para todo lo que se pueda hacer con sms
    def abrir_app_sms(self):
        opciones = {
            '1': 'Enviar SMS',
            '2': 'Eliminar mensaje recibido',
            '3': 'Eliminar mensaje enviado',
            '4': 'Mostrar mensajes recibidos',
            '5': 'Mostrar mensajes enviados',
            '6': 'Salir'
        }
        while True:
            print("\n---SMS---")
            for key, value in opciones.items():
                print(f"{key}. {value}")
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == '1':
                self.enviar_sms()
            elif opcion == '2':
                self.sms.eliminar_mensaje_entrada()
            elif opcion == '3':
                self.sms.eliminar_mensaje_salida()
            elif opcion == '4':
                self.sms.mostrar_bandeja_entrada()
            elif opcion == '5':
                self.sms.mostrar_bandeja_salida()
            elif opcion == '6':
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")
   
   ##COMPLETAR BIEN, USAR CENTRAL   
    def enviar_sms(self):
        opciones = {
            '1': 'Contacto',
            '2': 'Número telefónico',
            '3': 'Volver'
        }
        while True:
            for key, value in opciones.items():
                print(f"{key}. {value}")
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == '1':
                nombre = input('Enviar mensaje a: ').strip()
                numero = self.buscar_num_por_nombre(nombre)
                if not numero:
                    print(f'No se encontró el contacto {nombre}')
                    return
            elif opcion == '2':
                numero = input('Enviar mensaje al número: ').strip()
                ## Se me hace rara esta forma de validar 
                if not validar_telefono(numero):
                    print(f'El número {numero} no es válido.')
                    return
            elif opcion == '3':
                break
            else:
                print('Opción Inválida. Por favor intente nuevamente.')
            texto = input('Mensaje: ')
            central.enviar_sms(self.numero,numero,texto)
  
    #menu para todo lo que se pueda hacer con email
    def abrir_app_email(self):
        opciones = {
            '1': 'Enviar email',
            '2': 'Eliminar email recibido',
            '3': 'Eliminar email enviado',
            '4': 'Mostrar bandeja de entrada',
            '5': 'Mostrar bandeja de salida',
            '6':'Salir'
        }
        while True:
            print("\n---EMAIL---")
            for key, value in opciones.items():
                print(f"{key}. {value}")
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == '1':
                self.enviar_email()
            elif opcion == '2':
                self.email.eliminar_mensaje_entrada()
            elif opcion == '3':
                self.email.eliminar_mensaje_salida()
            elif opcion == '4':
                self.mostrar_bandeja_entrada_email()
            elif opcion == '5':
                self.email.mostrar_bandeja_salida()
            elif opcion == '6':
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")

    #COMPLETAR BIEN, AGREGAR VERIFICACIONES Y DEMÁS
    def enviar_email(self):
        mail_destino = input('Dirección de email: ')
        celu_destino = self.buscar_celu_por_email(mail_destino)
        asunto = input('Asunto: ')
        cuerpo = input('Cuerpo: ')
        self.email.enviar_email(mail_destino,asunto,cuerpo)
        celu_destino.email.recibir_mensaje(self.email,mail_destino,cuerpo)

    
    def mostrar_bandeja_entrada_email(self):
        opciones = {'1': 'No leídos primero','2': 'Por fecha','3':'Salir'}
        while True:
            print("\nBandeja de entrada Email:")
            for key, value in opciones.items():
                print(f"{key}. {value}")
            opcion = input("\nSeleccione una opción: ").strip()
            if opcion == '1':
                self.email.mostrar_emails_noleidos()
            elif opcion == '2':
                self.email.mostrar_emails_por_fecha()
            elif opcion == '3':
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")