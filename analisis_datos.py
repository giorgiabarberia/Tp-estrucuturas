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
plt.title('Porcentaje de descargas promedio: Free vs Paid Apps')
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
plt.xlabel('Total de instalaciones')
plt.ylabel('Categoría')
plt.title('Las 5 categorías más exitoras')
plt.show()




# Histograma de la distribución de ratings
ratings = np.array(rating)

plt.hist(ratings, bins=20, color='purple', edgecolor='black')
plt.xlabel('Rating')
plt.ylabel('número de apps')
plt.title('Distribución de ratings')
plt.grid(axis='y', linestyle='--')
plt.show()


##--GRAFICO: Box Plot de la distribución de ratings por género en la categoría 'GAME'---

# Filtrar aplicaciones de la categoría 'GAME'
game_indices = [i for i in range(len(category)) if category[i] == 'GAME']
game_genres = np.array([genres[i] for i in game_indices])
game_ratings = np.array([rating[i] for i in game_indices])

# Encontrar los géneros únicos dentro de la categoría 'GAME'
unique_game_genres = np.unique(game_genres)

# Crear una lista de ratings por género y filtrar géneros sin ratings
ratings_by_genre = [game_ratings[game_genres == genre] for genre in unique_game_genres if len(game_ratings[game_genres == genre]) > 0]
valid_genres = [genre for genre in unique_game_genres if len(game_ratings[game_genres == genre]) > 0]

plt.boxplot(ratings_by_genre, labels=valid_genres, patch_artist=True, notch=True)
plt.xlabel('Género')
plt.ylabel('Rating')
plt.title('Distribución de ratings por género en la categoría GAME')
plt.xticks(rotation=40)
plt.grid(True)
plt.show()



##--GRAFICO: Promedio de Reviews según última actualización---

# Convertir las fechas a un formato manejable
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        return datetime.strptime("January 1, 1970", "%B %d, %Y")  # Fecha por defecto en caso de error

dates = np.array([parse_date(date) for date in last_updated])

# Ordenar por fecha
sorted_indices = np.argsort(dates)
sorted_dates = dates[sorted_indices]
sorted_reviews = np.array(reviews)[sorted_indices]

# Agrupar y calcular el promedio de reviews por mes
unique_months = np.unique(sorted_dates.astype('datetime64[M]'))
avg_reviews_per_month = np.array([np.mean(sorted_reviews[sorted_dates.astype('datetime64[M]') == month]) for month in unique_months])

plt.plot(unique_months, avg_reviews_per_month, marker='o', linestyle='-', color='blue')
plt.xlabel('Month')
plt.ylabel('Average Reviews')
plt.title('Average Reviews Over Time')
plt.grid(True)
plt.show()