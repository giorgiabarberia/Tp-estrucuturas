import matplotlib.pyplot as plt
import csv

# Creo listas vacías para guardar la información del archivo csv
app = []
category = []
rating = []
reviews = []
size = []
installs = []
tipo = []
price = []
content_rating = []
genres = []
last_updated = []
current_ver = []
android_ver = []

# Abrir el archivo CSV
with open('Tp-estrucuturas/Play_Store_Data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar el encabezado
    for fila in reader:
        app.append(fila[0])
        category.append(fila[1])
        rating.append(float(fila[2]) if fila[2] != 'NaN' else 0.0)  # Manejo de NaN
        reviews.append(int(fila[3]))
        size.append(fila[4])
        installs.append(fila[5].replace('+', '').replace(',', ''))  # Limpio formato de installs
        tipo.append(fila[6])
        price.append(float(fila[7].replace('$', '')) if fila[7] != 'Free' else 0.0)  # Manejo precio
        content_rating.append(fila[8])
        genres.append(fila[9])
        last_updated.append(fila[10])
        current_ver.append(fila[11])
        android_ver.append(fila[12].strip())

# Convertir las instalaciones a enteros
installs = list(map(int, installs))

# Clasificar las aplicaciones en gratuitas y de pago
installs_free = [installs[i] for i in range(len(installs)) if price[i] == 0.0]
installs_paid = [installs[i] for i in range(len(installs)) if price[i] > 0.0]

# Calcular los promedios de instalaciones
avg_installs_free = sum(installs_free) / len(installs_free) if len(installs_free) > 0 else 0
avg_installs_paid = sum(installs_paid) / len(installs_paid) if len(installs_paid) > 0 else 0

# Visualizar los resultados con matplotlib
labels = ['Free Apps', 'Paid Apps']
averages = [avg_installs_free, avg_installs_paid]

plt.bar(labels, averages, color=['blue', 'orange'])
plt.xlabel('App Type')
plt.ylabel('Average Installs')
plt.title('Average Installs: Free vs Paid Apps')
plt.show()
