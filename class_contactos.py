import validaciones

class Contactos:
    def __init__(self):
        agenda_contactos = {}

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

    #Muestra la información de un contacto por numero y nombre
    def mostrar_informacion_contacto(self, nombre):
        pass

    #devuelve el número de un contacto  
    def buscar_num_por_nombre(self, nombre):
        return self.agenda_contactos.get(nombre)

    def eliminar_contacto():
        pass

    def actualizar_contacto():
        pass
