from class_mensajeria import SMS,Email
from class_central import Central
import validaciones 
central = Central()

class Celular:
    mails_usados = set()
    
    def __init__(self, id: int, nombre: str, modelo: str, sistema_operativo: str, version: str, cap_memoria_ram: str, cap_almacenamiento: str, numero: str, direcc_email: str):
        if not validaciones.validar_telefono(numero):
            raise ValueError(f'Error: el número de teléfono {numero} no es válido.')
        if id in Central.ids_registrados.keys():
            raise ValueError(f'Error: el id ingresado ya está en uso.')
        if numero in Central.celulares_registrados.keys():
            raise ValueError(f'Error: el número de teléfono ya está en uso.')
        if direcc_email in Celular.mails_usados:
            raise ValueError(f'Error: el mail ya está en uso.')

        self.id = id
        self.nombre = nombre
        self.modelo = modelo
        self.sist_op = sistema_operativo
        self.version = version
        self.ram = cap_memoria_ram
        self.almacenamiento = cap_almacenamiento
        self.numero = numero
        self.direcc_email = direcc_email  ## Acá el email está dos veces, una vez como objeto y otra el mail en sí
        self.prendido = False
        self.contraseña = None
        self.bloqueo = True
        self.red_movil = False
        self.datos = False
        self.en_llamada = False
        self.sms = None
        self.email = None
        self.agenda_contactos = {}
        self.email = Email(self.direcc_email)
        
        Celular.mails_usados.add(direcc_email)
        
    def __str__(self):
        return (f'Celular de {self.nombre}\nModelo: {self.modelo}\n'
                f'Sistema operativo: {self.sist_op}\nCapacidad de memoria RAM: {self.ram}\n'
                f'Capacidad de almacenamiento: {self.almacenamiento}\nNúmero telefónico: {self.numero}')
    
    def asignar_mensajeria(self,central):
        self.sms = SMS(self.id,central)

    #agrega contacto a la agenda_contactos (nombre:num)
    def agendar_contacto(self):
        nombre = input('Nombre del contacto: ')
        numero = input('Número de teléfono: ')
        if not validaciones.validar_telefono(numero):
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
    
    ## Se llama esta funcion cuando desde class operadora se elimina un celular, porque una vez que se elimina
    # se pueden volver a usar el mail en otro. 
    @classmethod
    def eliminar_mail_celular(cls,mail):
        try:
            cls.mails_usados.remove(mail)
        except:
            print('No se eliminaron el mail de su celular porque no se encontraba registrado.')
        
        
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
            if not validaciones.desea_continuar():
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
        if validaciones.desea_continuar():
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

    def abrir_app_sms(self):
        self.sms.ejecutar_sms()

    #menu para todo lo que se pueda hacer con email
    def abrir_app_email(self):
        self.email.abrir_app_email(central)