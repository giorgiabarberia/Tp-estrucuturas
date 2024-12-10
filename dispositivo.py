from configuracion import Configuracion
from app_store import AppStore

class Dispositivo:
    def __init__(self, nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento):
        self.marca = marca
        self.modelo = modelo
        self.sistema_operativo = sistema_operativo
        self.version = version
        self.memoria_ram = memoria_ram
        self.almacenamiento = almacenamiento
        self.configuracion = Configuracion(nombre,self)

    def __str__(self):
        return (f"{self.marca} {self.modelo}\nSistema Operativo: {self.sistema_operativo} {self.version}\nRAM: {self.memoria_ram}, Almacenamiento: {self.almacenamiento}")
        
class Tablet(Dispositivo):
     def __init__(self, nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento):
         super().__init__(nombre, marca, modelo, sistema_operativo, version, memoria_ram, almacenamiento)
         self.apps = AppStore() 