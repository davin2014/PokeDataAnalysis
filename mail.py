import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


# Realizar una solicitud a la PokeAPI
response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100')
data = response.json()  # Convertir la respuesta en un diccionario de Python

# Crear una lista para almacenar los nuevos datos
new_data = []

# Supongamos que 'response' es una lista de diccionarios que contienen URLs
for item in data['results']:
    url = item['url']  # Reemplaza 'url' con la clave real en tu diccionario
    
    new_response = requests.get(url)
    new_data_item = new_response.json()
    url_region = f'https://pokeapi.co/api/v2/version-group/{new_data_item["id"]}'
    # Obtener la región del Pokémon
    region = requests.get(url_region)

    if region.status_code == 200:
        data_region = region.json()
    else:
        data_region['regions'][0]['name'] = 'NA'

    if data_region['regions'] == []:
        data_region['regions'] = [{'name': 'NA'}] 

    # Seleccionar los valores que te interesan
    selected_values = {
        'name': new_data_item['name'],
        'weight': new_data_item['weight'],
        'height': new_data_item['height'],
        'type': new_data_item['types'][0]['type']['name'],
        'region': data_region['regions'][0]['name']
    }

    # Agregar los valores seleccionados a la nueva lista de datos
    new_data.append(selected_values)

 
# Guardar la nueva lista de datos en un archivo JSON
with open('pokemon_data.json', 'w') as file:
    json.dump(new_data, file)

# Cargar los datos del archivo JSON en un DataFrame
df = pd.read_json('pokemon_data.json')

# Mostrar las primeras 5 filas del DataFrame
print(df.head())
print('')
print('')

# Calcular la cantidad total de Pokémon en la lista
total_pokemon = len(df)
print(f'Total Pokémon: {total_pokemon}')
print('')
# Encontrar el Pokémon con el mayor y menor peso
# Suponiendo que la columna de peso se llama 'weight'
max_weight_pokemon = df[df['weight'] == df['weight'].max()]
min_weight_pokemon = df[df['weight'] == df['weight'].min()]
print(f'Pokémon con mayor peso: {max_weight_pokemon}')
print('')
print(f'Pokémon con menor peso: {min_weight_pokemon}')
print('')

# Agrupar los Pokémon por tipo y contar cuántos hay de cada tipo
# Suponiendo que la columna de tipo se llama 'type'
pokemon_by_type = df.groupby('type').size()
print(pokemon_by_type)

# Crear un gráfico de barras que muestre la distribución de los Pokémon por tipo
# Supongamos que 'df' es tu DataFrame y que tiene una columna 'type' y una columna 'region'
# Primero, vamos a contar cuántos Pokémon hay de cada tipo y de cada región
type_counts = df['type'].value_counts()
region_counts = df['region'].value_counts()

# Ahora, vamos a crear los gráficos de barras
fig, axs = plt.subplots(2)

# Gráfico de barras para 'type'
type_counts.plot(kind='bar', ax=axs[0])
axs[0].set_title('Distribución de Pokémon por tipo')

# Gráfico de barras para 'region'
region_counts.plot(kind='bar', ax=axs[1])
axs[1].set_title('Distribución de Pokémon por región')

# Guardar la figura como una imagen
fig.savefig('pokemon_distribution.png')