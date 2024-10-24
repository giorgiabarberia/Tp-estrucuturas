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

    def exportar(self, registros_llamadas):
        """
        Este método recibe una lista de diccionarios con los registros de las llamadas
        y los exporta a un archivo CSV.
        """
        # Definir los encabezados
        encabezados = ["Remitente", "Destinatario", "Hora de Inicio", "Hora de Fin", "Duración"]
        datos = [encabezados]

        # Agregar los registros de las llamadas
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
                # Llamar al método exportar de la superclase para guardar los datos
                super().exportar(datos)
            except Exception as e:
                if isinstance(e, FileIO):
                    print("Error al exportar el archivo de llamadas")
                elif isinstance(e, FileNotFoundError):
                    print("Archivo no encontrado")
                else:
                    print("Error desconocido")
        else:
            print("No hay datos que exportar")

# Ejemplo de cómo usar esta clase para exportar registros de llamadas

# Simulando algunos registros de llamadas
registros_llamadas = [
    {
        'Remitente': '123456789',
        'Destinatario': '987654321',
        'Hora de inicio': '23/10/2024 - 15:30:00',
        'Hora de fin': '23/10/2024 - 15:45:00',
        'Duración': '00:15:00'
    },
    {
        'Remitente': '123456789',
        'Destinatario': '111222333',
        'Hora de inicio': '23/10/2024 - 16:00:00',
        'Hora de fin': '23/10/2024 - 16:10:00',
        'Duración': '00:10:00'
    }
]

# Crear una instancia de ExportadorLlamada y exportar los registros
exportador = ExportadorLlamada("registros_llamadas.csv")
exportador.exportar(registros_llamadas)