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
#%%

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

#%%

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
#%%

c = """
        SELECT * 
        FROM bp
        WHERE id_depto NOT IN (
            SELECT id_depto
            FROM departamento)
    """
c_res= dd.sql(c).df()

#%%

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
#%%%
consultaSQL = """
                SELECT 
                    p.nombre_provincia,
                    d.nombre_depto,
                    CASE  
                          WHEN gmail > hotmail THEN 'Gmail' 
                          WHEN hotmail = 0 THEN 'Otro / No poseen'
                          ELSE 'Hotmail' END
                    AS Dominio_mas_usado
                FROM
                    (SELECT
                         bp.id_depto,
                         SUM(CASE WHEN mail LIKE '%@gmail.%' THEN 1 ELSE 0 END) AS gmail,
                         SUM(CASE WHEN mail LIKE '%@hotmail.%' THEN 1 ELSE 0 END) AS hotmail
                     FROM bp
                     GROUP BY id_depto
                        ) bpm
                
                RIGHT OUTER JOIN
                    departamento d ON bpm.id_depto = d.id_depto
                JOIN
                    provincia p ON d.id_provincia = p.id_provincia
              """
SQL_4 = dd.sql(consultaSQL).df()