import csv
from io import FileIO

class Exportador:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def exportar(self, lista):
        try:
            with open(self.nombre_archivo, "w", newline='') as archivo:  
                escritor = csv.writer(archivo)
                escritor.writerows(lista)  
        except IOError:
            print("Error al exportar archivo")
            raise FileIO('Error al exportar el archivo')


class ExportadorLlamada(Exportador):
    def __init__(self, nombre_archivo):
        super().__init__(nombre_archivo)

    # Recive una lista de diccionarios con los registros de llamadas y los exporta al csv de llamadas
    def exportar(self, registros_llamadas):
        encabezados = ["Remitente", "Destinatario", "Hora de Inicio", "Hora de Fin", "Duración"]
        datos = [encabezados]
        
        for registro in registros_llamadas:
            fila = [
                registro['Remitente'],
                registro['Destinatario'],
                registro['Hora de inicio'],
                registro['Hora de fin'],
                registro['Duración']
            ]
            datos.append(fila)

        if len(datos) > 1:
            try:
                # Llama al método exportar de Exportador para guardar los datos
                super().exportar(datos)
            except Exception as e:
                if isinstance(e, FileIO):
                    print("Error al exportar el archivo de llamadas")
                elif isinstance(e, FileNotFoundError):
                    print("Archivo no encontrado")
                else:
                    print("Error desconocido")


class ExportadorChats(Exportador):
    def __init__(self, nombre_archivo):
        super().__init__(nombre_archivo)

    ## Recibe una lista de diccionarios con los registros de sms y los exporta a un archivo csv.
    def exportar(self, registros_chats):
        encabezados = ["Remitente", "Destinatario", "Texto", "Fecha"]
        datos = [encabezados]

        for registro in registros_chats:
            fila = [
                registro['Remitente'],
                registro['Destinatario'],
                registro['Texto'],
                registro['Fecha'],
            ]
            datos.append(fila)

        if len(datos) > 1:
            try:
                # Llama al método exportar de Exportador para guardar los datos
                super().exportar(datos)
            except Exception as e:
                if isinstance(e, FileIO):
                    print("Error al exportar el archivo de sms")
                elif isinstance(e, FileNotFoundError):
                    print("Archivo no encontrado")
                else:
                    print("Error desconocido")