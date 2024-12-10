from datetime import datetime
import re
# Función que valida que un número de teléfono sea válido
def validar_telefono(celular: str) -> bool:
    return celular.isdigit() and 10 == len(celular) 

# Función para preguntar si desea continuar
def desea_continuar() -> bool:
    while True:
        cont = input('¿Desea continuar? (si o no): ').strip().lower()
        if cont in {'si', 'no'}:
            return cont == 'si'
        
# Funcion para validar que el usuario este ingresado:
def ingreso_no_vacio(variable):
    while not variable:
        variable = input('Debe ingresar algo')
    return variable

# Funcion para validar el email: 
def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def obtener_fecha_actual():
    return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')

def confirmar_accion(mensaje):
        while True:
            respuesta = input(f"{mensaje} (sí/no): ").strip().lower()
            if respuesta in ["sí", "no"]:
                return respuesta == "sí"
            print("Por favor, responde con 'sí' o 'no'.")