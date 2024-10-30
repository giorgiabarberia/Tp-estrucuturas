## Mail:
## Asumimos que cada persona solo puede tener un mail, y este no se puede repetir
##El uso de pilas (con deque) en la bandeja de entrada y salida de correos electrónicos está justificado porque 
# facilita el acceso rápido a los correos más recientes, permite la inserción eficiente de nuevos mensajes, y simula 
# el comportamiento natural de visualización de correos electrónicos donde los más recientes son los más relevantes para 
# el usuario. Esto mejora la experiencia de usuario al interactuar con su bandeja de entrada y salida.

## Contactos:
## Al agendar un contacto, te deja agendar lo que quieras como número, porque así sucede en los celulares.
# Luego, al intentar mandarle algo a ese número se le dirá al usuario que no existe. 

## SMS: 
## es posible mandarse mensjaes a uno mismo. 
## Al buscar un chat, se ingresa en el mismo lugar estés buscando por contacto o por numero telefonico, ya que en la app es así.

## Eliminar apps:
## Eliminar app está en el menú, y no una vez que se ingresa a la app porque consideramos que el 
# menú principal del celular es su pantalla de inicio. Como para eliminar una app hay que mantenerla
# apretada desde la pantalla de inicio (sin ingresar en ella), 
# simulamos esto como seleccionar el 7 (Eliminar app). 
## Si no está descargada ninguna app, no aparece la opcion eliminar en el celular por lo asumido
# anteriormente con eliminaer apps. Como interpretamos esta funcion del celular como mantenerla apretada,
# si no hay ninguna app no hay ninguna que se pueda mantener apretada. 
## Asumimos que las aplicaciones como telefono, sms y email no se puede descargar ni eliminar

## Menúes:
## Como en los celulares, muchas veces te dicen por ejemplo: Presione 1 para xxx, presione 5 para salir (se saltea numeros)
# consideramos que es correcto que ciertos menúes a veces se salteen numeros.
# Es decir, no consideramos que sea un error que exista algún menú cuyas opciones sean 1,2,3,6,7,0

## Validaciones: programación defensiva
# Hay varios casos donde un dato realiza por ejemplo este recorrido: funcion 1 -> funcion2 -> funcion3
# Muchas veces validamos que el dato sea valido tanto en la funcion 1, como en la funcion 2, como en la 3
# Consideramos que es correcto hacer esto por programación defensiva. 
# Las funciones en las que hacemos esto podrían usarse pa∫ra otras cosas más adelante, o se les podrían agregar funcionalidades.
# Realizamos esto para evitar futuros errores. 
