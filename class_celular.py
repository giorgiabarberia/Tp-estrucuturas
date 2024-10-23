from class_mensajeria import SMS,Email
from class_central import Central
from class_app_store import AppStore
from class_telefono import Telefono
from class_configuracion import Configuracion
from class_contactos import Contactos
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
        self.modelo = modelo
        self.sist_op = sistema_operativo
        self.version = version
        self.ram = cap_memoria_ram
        self.almacenamiento = cap_almacenamiento
        self.numero = numero
        self.direcc_email = direcc_email  ## Acá el email está dos veces, una vez como objeto y otra el mail en sí
        self.prendido = False
        self.bloqueo = True
        self.en_llamada = False
        self.sms = None
        self.telefono = None
        self.contactos = Contactos()
        self.configuracion = Configuracion(nombre)
        self.email = Email(self.direcc_email)
        self.apps = AppStore()   ## Crea la instancia de app store para este celular

        Celular.mails_usados.add(direcc_email)
        
    def __str__(self):
        return (f'Celular de {self.nombre}\nModelo: {self.modelo}\n'
                f'Sistema operativo: {self.sist_op}\nCapacidad de memoria RAM: {self.ram}\n'
                f'Capacidad de almacenamiento: {self.almacenamiento}\nNúmero telefónico: {self.numero}')
    
    def asignar_mensajeria(self,central):
        self.sms = SMS(self.id,central)
        self.telefono = Telefono(self.id,central)
    
    
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
            return True
        else:
            print('Prendiendo...')
            self.prendido = True
            ok = self.desbloquear()
            if ok:
                self.configuracion.activar_red_movil()
            return ok
            
    ## apagar el celular
    def apagar_celular(self):
        print('Apagando...')
        self.prendido = False

    ## desbloquear el celular automáticamente si no hay contraseña, si la hay usa validar_contraseña_actual
    def desbloquear(self):
        if self.configuracion.contraseña:
            if self.configuracion.validar_contraseña_actual():
                self.bloqueo = False
        else:
            self.bloqueo = False
        return not self.bloqueo

    #menu para todo lo que se pueda hacer con sms
    def abrir_app_sms(self):
        self.sms.ejecutar_sms()

    #menu para todo lo que se pueda hacer con email
    def abrir_app_email(self):
        self.email.ejecutar_email(central)

    #menu para todo lo que se pueda hacer con el teléfono (llamadas)
    def abrir_app_telefono(self):
        self.telefono.ejecutar_telefono()

