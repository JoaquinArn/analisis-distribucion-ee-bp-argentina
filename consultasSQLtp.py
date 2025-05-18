# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import duckdb as dd
#%%
bp = pd.read_csv('bp')
localizacion_ee = pd.read_csv('localizaciones_ee')
nivel_educativo_ee = pd.read_csv('nivel_educativo_ee')
provincia = pd.read_csv('provincia')
departamento = pd.read_csv('departamento')
#%% ANÁLISIS DE DATOS: CONSULTA SQL N°1

#Se busca informar, para cada departamento, su:
    # - Provincia
    # - Nombre del departamento
    # - Cantidad de EE de cada nivel educativo (de modalidad común)
    # - Cantidad de habitantes por edad según los niveles educativos.
    
#El resultado debe estar ordenado:
    # - Alfabéticamente por Provincia.
    # - Dentro de cada provincia, descendente por cantidad de escuelas primarias.


#Para ello, la consulta debe:
    # - Seleccionar cada atributo deseado
    # - Relacionar, a través de JOINs, las tablas 'nivel_educativo', 'localizacion_ee', 'departamento' y 'provincia'.
        # _ Tenemos en cuenta que no todos los departamentos tienen algun EE, por lo tanto, con 'departamento' habrá un OUTER JOIN.
    # - Hacer un conteo de los niveles jardín, primaria y secundaria de cada departamento.
    # - Realizar los agrupamientos y ordenamientos correspondientes.
    
consultaSQL = """
                SELECT 
                    provincia.nombre_provincia AS Provincia,
                    departamento.nombre_depto AS Departamento,
                    COUNT(CASE WHEN nivel_educativo_ee.tipo = 'jardin' THEN 1 END) AS Jardines,
                    departamento.pob_infantes AS Poblacion_Jardin,
                    COUNT(CASE WHEN nivel_educativo_ee.tipo = 'primario' THEN 1 END) AS Primarias,
                    departamento.pob_primaria AS Poblacion_Primaria,
                    COUNT(CASE WHEN nivel_educativo_ee.tipo = 'secundario' THEN 1 END) AS Secundarios,
                    departamento.pob_secundaria AS Poblacion_Secundaria
                FROM 
                    nivel_educativo_ee
                JOIN 
                    localizacion_ee ON nivel_educativo_ee.cueanexo = localizacion_ee.cueanexo
                RIGHT OUTER JOIN 
                    departamento ON localizacion_ee.id_depto = departamento.id_depto
                JOIN 
                    provincia ON departamento.id_provincia = provincia.id_provincia
                GROUP BY 
                    provincia.nombre_provincia, 
                    departamento.nombre_depto,
                    departamento.pob_infantes, 
                    departamento.pob_primaria, 
                    departamento.pob_secundaria
                ORDER BY 
                    provincia.nombre_provincia ASC,
                    Primarias DESC;

              """

SQL_1 = dd.sql(consultaSQL).df()

#%% ANÁLISIS DE DATOS: CONSULTA SQL N°2

#Se busca informar, para cada departamento, su:
    # - Provincia
    # - Nombre del departamento
    # - Cantidad de BP fundadas desde 1950

#El resultado debe estar ordenado:
    # - Alfabéticamente por Provincia.
    # - Dentro de cada provincia, descendente por cantidad de BP.

#Para ello, la consulta debe:
    # - Seleccionar cada atributo deseado
    # - Relacionar, a través de JOINs, las tablas 'bp', 'departamento' y 'provincia'.
        # _ Tenemos en cuenta que no todos los departamentos tienen alguna BP, por lo tanto, con 'departamento' habrá un OUTER JOIN.    
    # - Hacer un conteo de las bibliotecas que cumplen lo pedido.
    # - Realizar los agrupamientos y ordenamientos correspondientes.
    
consultaSQL = """
                SELECT 
                    provincia.nombre_provincia AS Provincia,
                    departamento.nombre_depto AS Departamento,
                    COUNT(CASE WHEN bp.fecha_fundacion >= '1950-01-01' THEN 1 END) AS 'Bibliotecas_fundadas_desde_1950'
                FROM
                    bp
                RIGHT OUTER JOIN
                    departamento ON bp.id_depto = departamento.id_depto
                JOIN
                    provincia ON departamento.id_provincia = provincia.id_provincia
                GROUP BY
                    provincia.nombre_provincia,
                    departamento.nombre_depto
                ORDER BY
                    provincia.nombre_provincia ASC,
                    Bibliotecas_fundadas_desde_1950 DESC;

              """

SQL_2 = dd.sql(consultaSQL).df()

#%% ANÁLISIS DE DATOS: CONSULTA SQL N°3

#Se busca informar, para cada departamento, su:
    # - Provincia
    # - Nombre del departamento
    # - Cantidad de BP
    # - Cantidad de EE (de modalidad común)
    # - Población total

#El resultado debe estar ordenado:
    # - Cantidad de EE descendente
    # - Cantidad de BP descendente
    # - Nombre de provincia ascendente
    # - Nombre de departamento ascendente
    
#Para ello, la consulta debe:
    # - Seleccionar cada atributo deseado
    # - Relacionar, a través de JOINs, las tablas 'departamento' y 'provincia'
    # - Armar subconsultas donde:
        #_ Se haga un conteo de los EE que hay en el departamento.
        #_ Se haga un conteo de las BP que hay en el departamento.
    # - Realizar los ordenamientos correspondientes    
    
consultaSQL = """
                SELECT 
                    p.nombre_provincia AS Provincia,
                    d.nombre_depto AS Departamento,
                    (SELECT COUNT(*) FROM localizacion_ee le WHERE le.id_depto = d.id_depto) AS Cant_EE,
                    (SELECT COUNT(*) FROM bp WHERE bp.id_depto = d.id_depto) AS Cant_BP,
                    d.pob_total AS Poblacion_Total
                FROM
                    departamento AS d
                JOIN
                    provincia AS p ON d.id_provincia = p.id_provincia
                ORDER BY
                    Cant_EE DESC,
                    Cant_BP ASC,
                    p.nombre_provincia ASC,
                    d.nombre_depto DESC;
              """

SQL_3 = dd.sql(consultaSQL).df()

#%% ANÁLISIS DE DATOS: CONSULTA SQL N°4

#Se busca informar, para cada departamento, su:
    # - Provincia
    # - Nombre del departamento
    # - Dominio de mail más usado por las bibliotecas del departamento.

#Esta consulta presenta una mayor dificultad
#Es por eso que optamos por la creación de un Dataframe auxiliar 'aux'
#Lo generamos a partir de una consulta SQL
#Su función será almacenar:
    #los departamentos que poseen alguna biblioteca
    #la cantidad de BP por cada dominio distinto hallado en las BP de ese departamento  

#Para ello, la consulta debe:
    # - Seleccionar cada atributo deseado
    # - Por cada mail, extraer su dominio.
    # - Contar cantidad de BP con cierto dominio por departamento.
    # - Realizar los agrupamientos correspondientes.

consultaSQL = """
        SELECT
            bp.id_depto,
            COUNT(*) AS cant_BP,
            SUBSTRING(mail FROM POSITION('@' IN mail) + 1) AS dominios,
        FROM bp
        GROUP BY id_depto, dominios
    """
    
aux = dd.sql(consultaSQL).df()

#A partir de esta consulta auxiliar, realizamos el ejercicio original
#Para ello, la consulta debe:
    # - Seleccionar cada atributo deseado
    # - Por cada departamento, sumar la cantidad de BP registrados.
    # - Extraer el dominio más usado por las BP de ese departamento (en caso de empate, devuelve indistintamente).
    # - Relacionar, a través de JOINs, las tablas 'departamento' y 'provincia'

consultaSQL = """
                SELECT 
                    p.nombre_provincia,
                    d.id_depto, 
                    IFNULL((SELECT SUM(aux.cant_BP) 
                            FROM aux 
                            WHERE aux.id_depto = d.id_depto), 0) AS cant_BP,
                    (SELECT dominios 
                     FROM aux 
                     WHERE aux.id_depto = d.id_depto 
                     AND aux.cant_BP = (
                                         SELECT MAX(aux2.cant_BP) 
                                         FROM aux AS aux2 
                                         WHERE aux2.dominios IS NOT NULL AND aux2.id_depto = d.id_depto
                                       )
                     LIMIT 1) AS dominio_mas_frecuente
                FROM departamento AS d
                JOIN 
                    provincia AS p ON d.id_provincia = p.id_provincia
    """
SQL_4 = dd.sql(consultaSQL).df()
