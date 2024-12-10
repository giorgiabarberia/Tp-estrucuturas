from mensajeria import SMS,Email
from central import Central
from app_store import AppStore
from telefono import Telefono
from configuracion import Configuracion
from contactos import Contactos
from dispositivo import Dispositivo
import validaciones 

class Celular:
    central = Central(Dispositivo)

    def __init__(self, nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento, id, numero):
        super().__init__(nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento)
        if not validaciones.validar_telefono(numero):
            raise ValueError(f'Error: el número de teléfono {numero} no es válido.')
        if id in Celular.central.ids_registrados.keys():
            raise ValueError(f'Error: el id ingresado ya está en uso.')
        if numero in Celular.central.celulares_registrados.keys():
            raise ValueError(f'Error: el número de teléfono ya está en uso.')
        self.id = id
        self.numero = numero
        self.prendido = False
        self.bloqueo = True
        self.en_llamada = False
        self.sms = None
        self.telefono = None
        self.contactos = Contactos() 
    
    def __str__(self):
        return (f'Celular de {self.configuracion.nombre}\nModelo: {self.modelo}\nSistema operativo: {self.sist_op}\nCapacidad de memoria RAM: {self.ram}\nCapacidad de almacenamiento: {self.almacenamiento}\nNúmero telefónico: {self.numero}')
    
    def asignar_sms_telefono(self,central):
        self.sms = SMS(self.id,central)
        self.telefono = Telefono(self.id,central)
        
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

    #menu para todo lo que se pueda hacer con el teléfono (llamadas)
    def abrir_app_telefono(self):
        self.telefono.ejecutar_telefono()


class CelularNuevo(Celular):
    mails_usados = set()
    
    def __init__(self, nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento, id, numero, direcc_email):
        super().__init__(nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento, id, numero)
        if direcc_email in CelularNuevo.mails_usados:
            raise ValueError(f'Error: el email ya está en uso.')
        self.direcc_email = direcc_email  ## Acá el email está dos veces, una vez como objeto y otra el email en sí
        self.email = Email(self.direcc_email)
        self.apps = AppStore()   ## Crea la instancia de app store para este celular
        self.configuracion = Configuracion(nombre,self)
        CelularNuevo.mails_usados.add(direcc_email)
    
    def buscar_celu_por_email(self, email):
        for celular in Celular.central.celulares_registrados.values():
            if isinstance(celular,CelularNuevo) and celular.direcc_email == email:
                return celular
        print(f"No se encontró ningún celular registrado con el email {email}.")
        return None
    
    ## Se llama esta funcion cuando desde class operadora se elimina un celular, porque una vez que se elimina
    # se pueden volver a usar el email en otro. 
    @classmethod
    def eliminar_mail_celular(cls,mail):
        try:
            cls.mails_usados.remove(mail)
        except:
            print('No se eliminaron el email de su celular porque no se encontraba registrado.')

    #menu para todo lo que se pueda hacer con email
    def abrir_app_email(self):
        self.email.ejecutar_email(Celular.central)

#VER COMO SACARLE LA CONFIGURACION PARA QUE NO SE CONECTE A INTERNET
class CelularAntiguo(Celular):
    def __init__(self, nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento, id, numero):
        super().__init__(nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento, id, numero)
