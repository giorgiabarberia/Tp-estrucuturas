import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime

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

# Función para convertir el tamaño a megabytes (MB)
def convert_size(size_str):
    if 'M' in size_str:
        return float(size_str.replace('M', '').strip()) 
    elif 'k' in size_str:
        return float(size_str.replace('k', '').strip()) / 1024  # Convertir a MB los que están en k
    return ''  # Para tamaños que no son válidos (cuando dice "Varies with device")

with open('Play_Store_Data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar el encabezado
    for fila in reader:
        app.append(fila[0])
        category.append(fila[1])
        rating.append(float(fila[2]) if fila[2] != 'NaN' else 0.0)  # Manejo de NaN
        reviews.append(int(fila[3]))
        valor_size = convert_size(fila[4]) # Paso size a un dato manejable
        if valor_size is not None:  # Ignorar valores no válidos
            size.append(valor_size)
        installs.append(fila[5].replace('+', '').replace(',', ''))  # Limpio formato de installs
        tipo.append(fila[6])
        price.append(float(fila[7].replace('$', '')) if fila[7] != 'Free' else 0.0)  # Manejo precio
        content_rating.append(fila[8])
        genres.append(fila[9])
        last_updated.append(fila[10])
        current_ver.append(fila[11])
        android_ver.append(fila[12].strip())
        
        
##--GRAFICO de DISPERSION (usamos logaritmo): cantidad de installs según tamaño de la dating app
dating_indices = [i for i, genre in enumerate(genres) if 'dating' in genre.lower() and size[i] != ""]

# Obtener los valores de size e installs correspondientes
dating_sizes = np.array([size[i] for i in dating_indices])
dating_installs = np.array([int(installs[i]) for i in dating_indices])

# Graficar los datos
plt.tight_layout() # Ajusto tamaño a los ejes
plt.scatter(dating_sizes, dating_installs, alpha=0.65) # Ajusto tamaño de los puntos, para que se vean mejor
plt.title("Dating Apps: tamaño vs. cantidad de installs", fontsize=14)
plt.xlabel("Size (MB)", fontsize=12)
plt.ylabel("Cantidad de installs (10^7)", fontsize=12)
plt.yscale('log')  # Escala logarítmica para los ejes Y
plt.grid(True)  # Agrego la grilla
plt.show()



##--GRAFICO BARRAS: Top 5 categorás más exitosas--
category = np.array(category)
installs = np.array(list(map(int, installs)))
ratings = np.array(rating)

# Filtrar categorías con un rating promedio mayor a 3.5 
valid_categories = [cat for cat in np.unique(category) if np.mean(ratings[category == cat]) > 3.5]
valid_categories = np.array(valid_categories)

# Sumar las instalaciones por cada categoría
total_installs_by_category = np.array([np.sum(installs[category == cat]) for cat in valid_categories])

# Obtener las 5 categorías con más instalaciones
top_indices = np.argsort(total_installs_by_category)[-5:]  # Indices de las 5 categorías más exitosas
top_categories = valid_categories[top_indices]
top_installs = total_installs_by_category[top_indices]

# Crear colores diferentes para cada barra
colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral']

# Visualizar los resultados
plt.figure(figsize=(13, 5))  # Aumentar el tamaño del gráfico, para que se vean los ejes
bars = plt.barh(top_categories, top_installs, color=colors)
plt.xlabel('Total de Installs (en 10^10)', fontsize=12)
plt.ylabel('Categoría', fontsize=12)
plt.title('Top 5 categorías de Apps más exitosas', fontsize=14)
plt.show()



##--HISTOGRAMA: distribución de ratings ---
ratings = np.array(rating)

# Filtrar ratings que son mayores a 0
filtered_ratings = ratings[ratings > 0]

# Histograma de la distribución de ratings
plt.tight_layout() # Ajusto tamaño a los ejes
plt.hist(filtered_ratings, bins=20, color='purple', edgecolor='black', alpha=0.7)  # Agregar transparencia
plt.xlabel('Rating', fontsize=12)
plt.ylabel('Number of apps', fontsize=12)
plt.title('Distribución de Ratings', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7) 
plt.show()





##--GRAFICO DE DISPERSION: distribución de ratings por género en la categoría 'GAME'---

# Filtrar aplicaciones de la categoría 'GAME'
game_indices = [i for i in range(len(category)) if category[i] == 'GAME']
game_genres = np.array([genres[i] for i in game_indices])
game_ratings = np.array([rating[i] for i in game_indices])

# Crear un filtro para ignorar ratings que son cero
non_zero_ratings_indices = game_ratings > 0
filtered_game_genres = game_genres[non_zero_ratings_indices]
filtered_game_ratings = game_ratings[non_zero_ratings_indices]

# Encontrar los géneros únicos dentro de la categoría 'GAME'
unique_game_genres = np.unique(filtered_game_genres)

# Crear un gráfico de dispersión
plt.figure(figsize=(12, 6))

# Colorear los puntos según el género
colors = plt.cm.get_cmap('tab10', len(unique_game_genres))  # Obtener una paleta de colores

for idx, genre in enumerate(unique_game_genres):
    ratings_for_genre = filtered_game_ratings[filtered_game_genres == genre]
    if len(ratings_for_genre) >= 2:  # Filtrar géneros con al menos 2 ratings
        plt.scatter([genre] * len(ratings_for_genre), ratings_for_genre, color=colors(idx), alpha=0.6, label=genre)

# Configurar el gráfico
plt.xlabel('Género', fontsize=11)
plt.ylabel('Rating', fontsize=11)
plt.title('Distribución de rating por genero en la categoría "GAME"', fontsize=13)
plt.xticks(rotation=90)
plt.grid(True)

# Mostrar el gráfico
plt.tight_layout()
plt.show()




## GRAFICO DE LINEA: Cantidad de instalaciones según año de la última update---

# Función para convertir las fechas a un formato manejable
def date_format(date_str):
    return datetime.strptime(date_str, "%B %d, %Y")

# Convertir las fechas y los datos a arrays
dates = np.array([date_format(date) for date in last_updated])

# Ordenar por fecha
sorted_indices = np.argsort(dates)
sorted_dates = dates[sorted_indices]
sorted_installs = np.array(installs)[sorted_indices]
sorted_ratings = np.array(rating)[sorted_indices]  # Asegúrate de tener los ratings ordenados

# Agrupar y calcular el promedio de installs y ratings por año
years = sorted_dates.astype('datetime64[Y]').astype(int) + 1970
unique_years = np.unique(years)

avg_installs_per_year = np.array([np.average(sorted_installs[years == year]) for year in unique_years])
avg_ratings_per_year = np.array([np.average(sorted_ratings[years == year][sorted_ratings[years == year] > 0]) for year in unique_years])  # Filtrar ratings > 0

# Crear la figura y el eje principal
fig, ax1 = plt.subplots()

# Graficar el promedio de instalaciones
ax1.plot(unique_years, avg_installs_per_year, marker='o', linestyle='-', color='blue', label='Average Installs')
ax1.set_xlabel('Año de la última actualización')
ax1.set_ylabel('Installs promedio (10^7)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Crear el segundo eje
ax2 = ax1.twinx()
ax2.plot(unique_years, avg_ratings_per_year, marker='o', linestyle='-', color='orange', label='Average Ratings')
ax2.set_ylabel('Rating promedio', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Añadir título y leyendas
plt.title('Installs (en 10^7) y ratings promedio por año de última actualización')
fig.tight_layout()  # Para ajustar bien los ejes
plt.show()