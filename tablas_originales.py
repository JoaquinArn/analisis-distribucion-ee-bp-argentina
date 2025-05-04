# -*- coding: utf-8 -*-
"""
TABLAS ORIGINALES
@author: Joaco
"""


import numpy as np
import pandas as pd
import duckdb as dd

#%% Tablas originales

bibliotecas_populares = pd.read_csv('bibliotecas-populares.csv')

ee = pd.read_excel('2022_padron_oficial_establecimientos_educativos.xlsx', sheet_name = 'padron2022', skiprows = 5, header = [0,1])
#después de analaizarlo, llego a la conclusión de que no está ni siquiera en primera forma normal
#tiene relaciones dentro de relaciones

#Modificamos la columna Unnamed: 43_level_1 por vacío en ee
# Extrae la lista actual de columnas (cada columna es una tupla)
columnas = ee.columns.tolist()

# Armamos una nueva lista de columnas la cual reemplaza el Unnamed: 43_level_1
nuevas_columnas = []
for columna in columnas:
    if (columna == ('Servicios complementarios', 'Unnamed: 43_level_1')):
        columna = ('Servicios complementarios', ' ')
    nuevas_columnas.append(columna)

# Reasignamos los nombres con el cambio realizado
ee.columns = pd.MultiIndex.from_tuples(nuevas_columnas)

#%%
#Pruebo como hacer la primer tabla
df_raw = pd.read_excel("padron_poblacion.xlsx", header=None)

area_val = df_raw.iloc[13, 1]    # B14: fila 13, columna 1
comuna_val = df_raw.iloc[13, 2]   # C14: fila 13, columna 2

df_tabla = pd.read_excel("padron_poblacion.xlsx", header=15)

df_tabla["Area"] = area_val
df_tabla["Comuna"] = comuna_val

#%%
df = pd.read_excel('padron_poblacion.xlsx', header=None)
n_rows = len(df)

segmentos = []
i = 0
col_area   = 1   # columna B porque indica area
col_nombre = 2   # columna C porque indica nombre

while i < n_rows:
    celda = df.iat[i, col_area] #recorro celdas de la columna b
    # Solo miro en columna B si empieza con "AREA"
    if isinstance(celda, str) and celda.strip().startswith('AREA'):
        area   = celda.strip()[-5:]               # últimos 5 caracteres pues es un patron que se repite
        nombre = df.iat[i, col_nombre]            # valor en columna C

        # Cabecera dos filas abajo
        header_row = i + 2
        if header_row >= n_rows:
            break
        header = df.iloc[header_row].tolist() #pongo como header la de la tabla

        # Leo hasta fila vacía y voy guardando las filas como listas en el df
        j = header_row + 1
        filas = []
        while j < n_rows and not df.iloc[j].isnull().all():
            filas.append(df.iloc[j].tolist())
            j += 1

        # Si hay datos, creo el sub‑DataFrame
        if filas:
            sub = pd.DataFrame(filas, columns=header)
            sub['Area']   = area
            sub['Nombre'] = nombre
            segmentos.append(sub)

        # Salto al final de esta mini‑tabla
        i = j + 1
        continue

    i += 1

#Concateno

resultado = pd.concat(segmentos, ignore_index=True)
resultado = resultado.drop(resultado.columns[0], axis=1) #Elimino la columna A que esta llena de NULLS
