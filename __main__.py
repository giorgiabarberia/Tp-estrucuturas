from class_celular import Celular
from class_operadora import Operadora
from class_central import Central
from class_mensajeria import Email, SMS

operadora = Operadora('Personal')
central = Central()

# Crear celulares
celular1 = Celular(1, "Juan", "Galaxy S21", "Android", "11.0", "8GB", "128GB", "1130087090", "juan@example.com")
celular2 = Celular(2, "Ana", "iPhone 13", "iOS", "14.0", "6GB", "256GB", "1141790650", "ana@example.com")
celular3 = Celular(3,"Ana", "iPhone 13", "iOS", "14.0", "6GB", "256GB", "1100004444", "anaa@example.com")

# Registrar los celulares en la central
operadora.registrar_celu_autom(celular1)
operadora.registrar_celu_autom(celular2)
operadora.registrar_celu_autom(celular3)

# Prender los celulares
celular1.prender_celular()
celular2.prender_celular()
celular3.prender_celular()


celular1.contactos.agendar_contacto()
celular1.contactos.agendar_contacto()

# Enviar un email desde Juan a Ana
celular1.abrir_app_sms()
celular2.abrir_app_sms()
celular3.abrir_app_sms()

# print('CELULAR 1')
# celular1.abrir_app_email()
# print('CELULAR 2')
# celular2.abrir_app_email()
#print('celu 1')
#celular1.abrir_app_telefono()
#print('celu 2')
#celular2.abrir_app_telefono()
#print('celu 1')
#celular1.abrir_app_telefono()