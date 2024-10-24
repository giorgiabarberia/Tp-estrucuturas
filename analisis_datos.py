import matplotlib.pyplot as plt
import csv
import numpy as np

# Inicializamos listas vacías para guardar la información del archivo CSV
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

with open('Play_Store_Data.csv', 'r', encoding='utf-8') as file:
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

##--GRAFICO TORTA Percentage of Average Installs: Free vs Paid Apps---
 
installs = np.array(list(map(int, installs)))
price = np.array(price)

# Clasificar las aplicaciones en gratuitas y de pago
installs_free = installs[price == 0.0]
installs_paid = installs[price > 0.0]

# Calcular los promedios de instalaciones
avg_installs_free = np.mean(installs_free) if len(installs_free) > 0 else 0
avg_installs_paid = np.mean(installs_paid) if len(installs_paid) > 0 else 0

# Visualizar los resultados con un gráfico de torta
labels = ['Free Apps', 'Paid Apps']
averages = [avg_installs_free, avg_installs_paid]
colors = ['lightblue', 'orange']

plt.pie(averages, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title('Percentage of Average Installs: Free vs Paid Apps')
plt.axis('equal')  # Para que el gráfico sea circular
plt.show()


##--GRAFICO BARRAS: Top 5 Most Successful Categories--

category = np.array(category)
installs = np.array(list(map(int, installs)))

# Encontrar las categorías únicas
unique_categories = np.unique(category)

# Sumar las instalaciones por cada categoría
total_installs_by_category = np.array([np.sum(installs[category == cat]) for cat in unique_categories])

# Obtener las 5 categorías con más instalaciones
top_indices = np.argsort(total_installs_by_category)[-5:]  # Indices de las 5 categorías más exitosas
top_categories = unique_categories[top_indices]
top_installs = total_installs_by_category[top_indices]

# Visualizar los resultados
plt.barh(top_categories, top_installs, color='skyblue')
plt.xlabel('Total Installs')
plt.ylabel('Category')
plt.title('Top 5 Most Successful Categories')
plt.show()