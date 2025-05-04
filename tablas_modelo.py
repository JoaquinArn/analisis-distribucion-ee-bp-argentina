# -*- coding: utf-8 -*-
"""
TABLAS A USAR

@author: Joaco
"""

import numpy as np
import pandas as pd
import duckdb as dd

#%% Tablas originales para formación de las que vamos a usar : BP y EE

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

#%% Tablas originales para formación de las que vamos a usar : PP parte 1
#Pruebo como hacer la primer tabla
df_raw = pd.read_excel("padron_poblacion.xlsx", header=None)

area_val = df_raw.iloc[13, 1]    # B14: fila 13, columna 1
comuna_val = df_raw.iloc[13, 2]   # C14: fila 13, columna 2

df_tabla = pd.read_excel("padron_poblacion.xlsx", header=15)

df_tabla["Area"] = area_val
df_tabla["Comuna"] = comuna_val

#%% Tablas originales para formación de las que vamos a usar : PP parte 2
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


#%% AHORA LAS QUE VAMOS A USAR: bp
consultaSQL = """
                SELECT nro_conabip, cod_localidad, mail, fecha_fundacion
                FROM bibliotecas_populares
              """

bp = dd.sql(consultaSQL).df()

#%% AHORA LAS QUE VAMOS A USAR: localizacion_ee

localizacion_ee = ee[[('Establecimiento - Localización', 'Cueanexo'), ('Establecimiento - Localización', 'Código de localidad')]]
nuevas_columnas = ['cueanexo', 'cod_localidad'] #renombro las columnas
localizacion_ee.columns = nuevas_columnas

#%% AHORA LAS QUE VAMOS A USAR: tipo_establecimiento

#Yo quiero armar dos listas a las cuales pasar después a un diccionario
#Estas listas tendrán la misma longitud en cada momento
#La posición i de la lista 'establecimientos' marcará la clave de un establecimiento; y la posicion i de la lista 'tipos' informará el tipo de establecimientos
# Si un establecimiento cumple con más de un tipo, entonces aparecerá otro registro en una posicion j en la que en 'establecimientos' se informe su clave y en 'tipos' su otro tipo  
establecimientos = []
tipos = []
for fila in ee.iterrows(): #en iterrows, [0] es el índice de fila y [1] es la serie en la que están cada uno de los atributos
    if (fila[1][('Común', 'Nivel inicial - Jardín maternal')] == 1 or fila[1][('Común', 'Nivel inicial - Jardín de infantes')] == 1):
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        tipos.append('jardin')
    if (fila[1][('Común', 'Primario')] == 1):
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        tipos.append('primario')
    if (fila[1][('Común', 'Secundario')] == 1 or fila[1][('Común', 'Secundario - INET')] == 1 or fila[1][('Común', 'SNU')] == 1):
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        tipos.append('secundario')


tipo_establecimiento = {'cueanexo' : [], 'tipo' : []} #inicializo dict vacío donde irán las claves y sus tipos (notar que los arrays están ordenados)
tipo_establecimiento['cueanexo'] = establecimientos
tipo_establecimiento['tipo'] = tipos

tipo_establecimiento = pd.DataFrame(data = tipo_establecimiento) #la primer columna serán las claves y la segunda los tipos. Como los arrays los dí ordenados, el dataframe contendrá la info correctamente

#%% AHORA LAS QUE VAMOS A USAR: pp

pp = resultado[['Area', 'Nombre']].drop_duplicates() #agarro las columnas area y nombre, sin pares duplicados
pp['Area'] = pp['Area'].astype(str)

pob_infantes = {'Area' : [], 'pob_infantes': [], 'pob_primaria' : [], 'pob_secundaria' : []}
sumaPobJardin = 0
sumaPobPrimaria = 0
sumaPobSecundaria = 0
area = '02007' #selecciono el primer área
for fila in resultado.iterrows():
    if (fila[1]['Area'] != area or fila[0] == len(resultado) - 1):
        pob_infantes['Area'].append(area)
        pob_infantes['pob_infantes'].append(sumaPobJardin)
        pob_infantes['pob_primaria'].append(sumaPobPrimaria)
        pob_infantes['pob_secundaria'].append(sumaPobSecundaria)
        area = fila[1]['Area']
        sumaPobJardin = 0
        sumaPobPrimaria = 0
        sumaPobSecundaria = 0
        
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(0, 6)):
        sumaPobJardin += int(fila[1]['Casos'])
    
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(6, 13)):
        sumaPobPrimaria += int(fila[1]['Casos'])
        
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(13, 19)):
        sumaPobSecundaria += int(fila[1]['Casos'])
    
    
dfaux = pd.DataFrame(data = pob_infantes)

consultaSQL = """
                SELECT *
                FROM pp
                NATURAL JOIN dfaux
              """

pp = dd.sql(consultaSQL).df()


#%% AHORA LAS QUE VAMOS A USAR: localidades_en_departamento

localidades_en_departamento = pd.read_excel('2022_padron_oficial_establecimientos_educativos.xlsx', sheet_name = 'padron2022', skiprows = 6)
localidades_en_departamento = localidades_en_departamento[['Código de localidad', 'Departamento']]
localidades_en_departamento.rename(columns = {'Código de localidad' : 'cod_loc'}, inplace = True)

consultaSQL = """
                SELECT DISTINCT cod_loc, UPPER(Departamento) AS departamento
                FROM localidades_en_departamento
              """

localidades_en_departamento = dd.sql(consultaSQL).df()

#%% AHORA LAS QUE VAMOS A USAR: jurisdiccion_departamento


jurisdiccion_departamento = ee[[('Establecimiento - Localización', 'Departamento'), ('Establecimiento - Localización', 'Jurisdicción')]].drop_duplicates()
nuevas_columnas = ['departamento', 'jurisdiccion'] #renombro las columnas
jurisdiccion_departamento.columns = nuevas_columnas
