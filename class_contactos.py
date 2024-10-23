import validaciones
class Contactos:
    def __init__(self):
        self.agenda_contactos = {}

    # Agrega contacto a la agenda_contactos (num:nombre)
    def agendar_contacto(self):
        nombre = input('Nombre del contacto: ')
        numero = input('Número de teléfono: ')
        if not validaciones.validar_telefono(numero):
            print(f'Error: El número {numero} no es válido.')
            return
        if numero in self.agenda_contactos.keys():
            print(f'Error: El contacto con el número {numero} ya existe.')
        else:
            self.agenda_contactos[numero] = nombre
            print(f'Contacto {nombre} agendado con éxito.')

    #Muestra la información de un contacto por numero o por nombre
    def mostrar_informacion_contacto(self, busqueda):
        resultados = [(numero, nombre) for numero, nombre in self.agenda_contactos.items() if busqueda == nombre or busqueda == numero]
        if not resultados:
            print('Contacto no encontrado.')
        elif len(resultados) == 1:
            numero, nombre = resultados[0]
            print(f'Nombre: {nombre}, Número: {numero}')
        else:
            print(f'\nSe encontraron múltiples contactos con el nombre "{busqueda}":')
            for i, (numero, nombre) in enumerate(resultados, 1):
                print(f'{i}. Nombre: {nombre}, Número: {numero}')
            seleccion = int(input('Seleccione el número correspondiente al contacto deseado: '))
            numero, nombre = resultados[seleccion - 1]
            print(f'Nombre: {nombre}, Número: {numero}')
    

# Devuelve el número de un contacto por nombre
    def buscar_num_por_nombre(self, nombre):
        numeros = [numero for numero, contacto_nombre in self.agenda_contactos.items() if contacto_nombre == nombre]
        if not numeros:
            return None
        elif len(numeros) == 1:
            return numeros[0]
        else:
            print(f'\nSe encontraron múltiples contactos con el nombre "{nombre}":')
            for i, numero in enumerate(numeros, 1):
                print(f'{i}. Número: {numero}')
            seleccion = int(input('Seleccione el número correspondiente al contacto deseado: '))
            return numeros[seleccion - 1]
        
    # Elimina un contacto por nombre o número
    def eliminar_contacto(self):
        busqueda = input('Ingrese el nombre o número del contacto a eliminar: ')
        resultados = [(numero, nombre) for numero, nombre in self.agenda_contactos.items() if busqueda == nombre or busqueda == numero]
        if len(resultados) == 0:
            print('Contacto no encontrado.')
        elif len(resultados) == 1:
            numero, nombre = resultados[0]
            del self.agenda_contactos[numero]
            print(f'Contacto {nombre} eliminado con éxito.')
        else:
            print(f'\nSe encontraron múltiples contactos con el nombre "{busqueda}":')
            for i, (numero, nombre) in enumerate(resultados, 1):
                print(f'{i}. Nombre: {nombre}, Número: {numero}')
            seleccion = int(input('Seleccione el número correspondiente al contacto a eliminar: '))
            numero, nombre = resultados[seleccion - 1]
            del self.agenda_contactos[numero]
            print(f'Contacto {nombre} eliminado con éxito.')


    # Actualiza el número o nombre de un contacto existente - REVISAR
    def actualizar_contacto(self):
        busqueda = input('Ingrese el nombre o número del contacto a actualizar: ')
        resultados = [(numero, nombre) for numero, nombre in self.agenda_contactos.items() if busqueda == nombre or busqueda == numero]
        
        if len(resultados) == 0:
            print('Contacto no encontrado.')
            return
        elif len(resultados) == 1:
            numero, nombre = resultados[0]
        else:
            print(f'\nSe encontraron múltiples contactos con el nombre "{busqueda}":')
            for i, (numero, nombre) in enumerate(resultados, 1):
                print(f'{i}. Nombre: {nombre}, Número: {numero}')
            seleccion = int(input('Seleccione el número correspondiente al contacto a actualizar: '))
            numero, nombre = resultados[seleccion - 1]

        nuevo_nombre = input(f'Nuevo nombre (actual: {nombre}, si lo quiere mantener presione intro): ') or nombre
        nuevo_numero = input(f'Nuevo número (actual: {numero}, si lo quiere mantener presione intro): ') or numero
        if nuevo_numero != numero and not validaciones.validar_telefono(nuevo_numero):
            print(f'Error: El número {nuevo_numero} no es válido.')
            return
        del self.agenda_contactos[numero]
        self.agenda_contactos[nuevo_numero] = nuevo_nombre
        print(f'Contacto actualizado: Nombre: {nuevo_nombre}, Número: {nuevo_numero}')
        
    def menu_contactos(self):
        while True:
            print("\n--- Menú de Contactos ---")
            print("1. Agendar Contacto")
            print("2. Mostrar Información de Contacto")
            print("3. Eliminar Contacto")
            print("4. Actualizar Contacto")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.agendar_contacto()
            elif opcion == '2':
                busqueda = input('Ingrese el nombre o número del contacto a mostrar: ')
                self.mostrar_informacion_contacto(busqueda)
            elif opcion == '3':
                self.eliminar_contacto()
            elif opcion == '4':
                self.actualizar_contacto()
            elif opcion == '5':
                print("Saliendo del menú de contactos.")
                return  # Regresa del método, saliendo del bucle
            else:
                print("Opción no válida, por favor intente de nuevo.")