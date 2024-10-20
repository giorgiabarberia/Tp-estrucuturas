from class_celular import Celular
from class_operadora import Operadora
from class_central import Central

operadora = Operadora('Personal')
central = Central()

# Crear celulares
celular1 = Celular(1, "Juan", "Galaxy S21", "Android", "11.0", "8GB", "128GB", "1234567890", "juan@example.com")
celular2 = Celular(2, "Ana", "iPhone 13", "iOS", "14.0", "6GB", "256GB", "0987654321", "")

# Registrar los celulares en la central
operadora.registrar_celu_autom(celular1)
operadora.registrar_celu_autom(celular2)

# Prender los celulares
celular1.prender_celular()
celular2.prender_celular()

# # Agregar contactos
# celular1.agendar_contacto()
# celular2.agendar_contacto()

# # Enviar un SMS desde Juan a Ana
# celular1.abrir_app_sms()
# celular2.abrir_app_sms()

celular1.abrir_app_email()
