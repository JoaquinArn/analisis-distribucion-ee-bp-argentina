# -*- coding: utf-8 -*-
"""

@author: Joaco
"""
import numpy as np
import pandas as pd
import duckdb as dd

#%% Tablas originales
establecimientos_educativos = pd.read_excel('2022_padron_oficial_establecimientos_educativos.xlsx', sheet_name = 'padron2022', skiprows = 6)
#después de analaizarlo, llego a la conclusión de que no está ni siquiera en primera forma normal
#tiene relaciones dentro de relaciones

bibliotecas_populares = pd.read_csv('bibliotecas-populares.csv')

#%%
consultaSQL = """
                SELECT cod_localidad, nombre, COUNT(*) AS cantidad
                FROM bibliotecas_populares
                GROUP BY cod_localidad, nombre;
              """
dataframeResultado = dd.sql(consultaSQL).df()

# con esta consulta, ví que la Bib.Pop Florentino Ameghino (cod_localidad: 6441030) está repetida

#%%
consultaSQL = """
                SELECT *
                FROM bibliotecas_populares
                WHERE (
                    SELECT COUNT(*) 
                    FROM bibliotecas_populares AS b2
                    WHERE b2.cod_localidad = bibliotecas_populares.cod_localidad
                    AND LEVENSHTEIN(b2.nombre, bibliotecas_populares.nombre) <=3
                    ) > 1;
              """
dataframeResultado = dd.sql(consultaSQL).df()
# con esta consulta, veo que no son iguales pero por alguna razón tienen el mismo cod_localidad cuando pertenecen a distintas localidades
# es raro el mail de una de las dos pues su mail no da indicios de que se está hablando de una bp llamada Florentino Ameghino
#%%
consultaSQL = """
                SELECT cod_localidad
                FROM bibliotecas_populares
                WHERE localidad = 'La Plata';
              """
dataframeResultado = dd.sql(consultaSQL).df()