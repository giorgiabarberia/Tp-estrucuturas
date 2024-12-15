import validaciones


class Configuracion:
    def __init__(self,nombre,celular,conectividad,red):
        self.nombre = nombre
        self.celular=celular
        self.conectividad = conectividad ## Como los celulares viejos no tienen internet, es FALSE para bloquearle los métodos
        self.contraseña = None
        self.bloqueo = True
        self.red_movil = False
        self.red = red #indica si un dispositivo necesita o no red movil
        self.datos = False
    
    ## función de configuración
    def opciones(self):
        print('1. Cambiar nombre')
        print('2. Cambiar código de desbloqueo')
        if self.conectividad:
            print('3. Datos')
        if self.red:
            print('4. Red movil')
        print('5. Visualizar información del celular')
        print('6. Salir')
        
    def configuracion(self): 
        while True:
            print("\nConfiguración:")
            self.opciones()
            opcion = input("Seleccione una opción: ").strip()
            if opcion == '1':
                self.cambiar_nombre()
            elif opcion == '2':
                self.cambiar_codigo()
            elif opcion == '3' and self.conectividad:
                self.configurar_datos()
            elif opcion == '4' and self.red:
                self.configurar_red_movil()
            elif opcion == '5': #Para que aparezca la info de tu celular
                print('Los datos de su celular son: ')
                print(self.celular) 
            elif opcion == '6':
                print("Saliendo de la configuración.")
                break
            else:
                print("Opción Inválida. Por favor, intente nuevamente.")
                
    # Menú configuración de datos
    def configurar_datos(self):
        if self.conectividad:
            opciones = {
                '1': 'Activar datos',
                '2': 'Desactivar datos',
                '3': 'Volver'
            }
            opcion = None
            while opcion != '3':
                print("\nConfiguración de Datos:")
                for key, value in opciones.items():
                    print(f"{key}. {value}")
                opcion = input("Seleccione una opción: ").strip()
                if opcion == '1':
                    self.activar_datos()
                elif opcion == '2':
                    self.desactivar_datos()
                elif opcion != '3':
                    print("Opción Inválida. Por favor, intente nuevamente.")
                
    # Cambiar el nombre del usuario
    def cambiar_nombre(self):
        print(f'{self.nombre}, ud. va a cambiar su nombre')
        if validaciones.desea_continuar():
            nuevo = ''
            while not (0 < len(nuevo) <= 50):
                nuevo = input('Ingrese un nuevo nombre: ').strip()
                if 0 < len(nuevo) <= 50:
                    self.nombre = nuevo
                else:
                    print('Nombre inválido. Intente nuevamente.')
                    
    
    # Menú configuración de red móvil
    def configurar_red_movil(self):
        if self.red:
            opciones = {
                '1': 'Activar red móvil',
                '2': 'Desactivar red móvil',
                '3': 'Volver'
            }
            opcion = ""
            while opcion != '3':
                print("\nConfiguración de Red Móvil:")
                for key, value in opciones.items():
                    print(f"{key}. {value}")
                opcion = input("Seleccione una opción: ").strip()
                if opcion == '1':
                    self.activar_red_movil()
                elif opcion == '2':
                    self.desactivar_red_movil()
                elif opcion != '3':
                    print("Opción Inválida. Por favor, intente nuevamente.")
            
    # Actualizar la contraseña
    def actualizar_codigo(self):
        nuevo, validar = None, None
        while nuevo != validar or not nuevo:
            nuevo = input('Ingrese su nuevo código: ')
            validar = input('Ingrese su nuevo código nuevamente: ')
            if nuevo != validar:
                print('No coinciden los códigos, intente nuevamente.')
        self.contraseña = nuevo
        
    ## Si el usuario ya tiene contraseña, valida que la sepa, y luego llama a actualizar_codigo  
    def cambiar_codigo(self):
        if self.contraseña:
            if self.validar_contraseña_actual():
                self.actualizar_codigo()
            else:
                print('Lo lamentamos, no podrás cambiar tu código')
        else:
            self.actualizar_codigo()
            
       
    ## Activar la red movil
    def activar_red_movil(self):
        if self.red:
            if self.red_movil:
                print('La red movil ya está activa.')
            else:
                print('Activando red movil...')
                self.red_movil = True
    
    ## Desactiva la red movil
    def desactivar_red_movil(self):
        if self.red:
            if not self.red_movil:
                print('La red movil ya está desactivada.')
            else:
                print('Desactivando red movil...')
                if self.celular.en_llamada:
                    self.celular.telefono.colgar()
                self.red_movil = False
        
    ## Activar datos
    def activar_datos(self):
        if self.conectividad:
            if self.datos:
                print('Los datos celulares ya están activados')
            else:
                print('Activando datos...')
                self.datos = True
        
    ## Desactivar datos
    def desactivar_datos(self):
        if self.conectividad:
            if not self.datos:
                print('Los datos celulares ya están desactivados')
            else:
                print('Desactivando datos...')
                self.datos = False
    
    ## validar que el usuario sepa cual es su contraseña actual
    def validar_contraseña_actual(self) -> str:
        while True:
            ingreso = input('Ingrese la contraseña: ')
            if ingreso == self.contraseña:
                return ingreso
            print('Contraseña incorrecta.')
            if not validaciones.desea_continuar():
                return ''
            
 