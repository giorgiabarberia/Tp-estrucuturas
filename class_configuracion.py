import validaciones
## ACA VA CONFIGURACION
#### NINFA DIHO Q TIENE Q IR ACA
class Configuracion:
    def __init__(self,nombre):
        self.nombre = nombre
        self.contraseña = None
        self.bloqueo = True
        self.red_movil = False
        self.datos = False
    
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