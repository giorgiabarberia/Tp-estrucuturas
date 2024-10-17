from class_operadora import Operadora

def mostrar_menu():
    print("Menú Principal")
    print("1. Operadora")
    print("2. Celular")
    print("3. Salir")

def mostrar_submenu_operadora():
    print("Submenú Operadora")
    print("1. Crear Celular")
    print("2. Eliminar Celular")
    print("3. Volver al Menú Principal")

def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            while True:
                mostrar_submenu_operadora()
                sub_opcion = input("Seleccione una opción: ")
                
                if sub_opcion == '1':
                    pass
                    ##Crea el celular
                elif sub_opcion == '2':
                    pass 
                    ## Elimina el celular
                elif sub_opcion == '3':
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
        
        elif opcion == '2':
            print("Accediendo a las funciones del celular...")
            # Aquí puedes agregar más funciones relacionadas con el celular

        elif opcion == '3':
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")