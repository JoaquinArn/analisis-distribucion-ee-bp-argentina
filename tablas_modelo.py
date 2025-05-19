# -*- coding: utf-8 -*-
"""
TABLAS MODELO
"""

import numpy as np
import pandas as pd
import duckdb as dd

#%% TABLA MODELO RELACIONAL: BP

bibliotecas_populares = pd.read_csv('bibliotecas-populares.csv')

#Seleccionamos las columnas que definimos en el Modelo Relacional, con los correspondientes nombres
consultaSQL = """
                SELECT nro_conabip, id_departamento AS id_depto, mail, fecha_fundacion
                FROM bibliotecas_populares
              """

bp = dd.sql(consultaSQL).df()

# Observación: el atributo 'mail' no puede ser usado como identificador de una BP; o el departamento de una BP.
# Hemos notado la presencia de dos bibliotecas de distintos departamentos que poseen mismo mail.

consultaSQL = """
                SELECT * 
                FROM bp
                WHERE mail IN (
                    SELECT mail
                    FROM bp AS bp2
                    WHERE bp.nro_conabip != bp2.nro_conabip)
                """
bibliotecas_mail_repetido = dd.sql(consultaSQL).df()

#Luego, eso significa que no será confiable el mail para identificar los datos relacionadas a una BP
#Por lo tanto, no existe dependencia funcional válida con el atributo mail como único atributo del lazo izquierdo de una DF.


#Ahora bien, con eso aclarado, queremos hacer cierta limpieza de datos, para asegurar:
    #1)atomicidad y correctitud de los atributos involucrados.
    #2)consistencia entre tablas.

#--En primer lugar, nos enfocamos en lograr atomicidad en el atributo mail --

#Lo hacemos realizando las siguientes consultas SQL

#Primero seleccionamos aquellos que no poseen mail NULL pues, en ese caso, el atributo ya es atómico.

consultaSQL = """
                SELECT *
                FROM bp
                WHERE mail LIKE '%@%'
              """
bibliotecas_con_mail = dd.sql(consultaSQL).df()
 
#La relación bibliotecas_con_mail tiene 1022 filas. 
#Una particularidad de los mails, es que todos llevan @. Comprobamos:

consultaSQL = """
                SELECT *
                FROM bibliotecas_con_mail
                WHERE mail LIKE '%@%'
              """

comprobacion_arroba_mail = dd.sql(consultaSQL).df()
#Devolvió 1022 filas, lo que implica que todos los mails llevan un @
#Es así que identificamos las que tienen dos (o más) mails contando los @ que tiene en su valor asociado al atributo mail

consultaSQL = """
                SELECT *
                FROM bibliotecas_con_mail
                WHERE mail LIKE '%@%@%'
              """

identificacion_mails_multiples = dd.sql(consultaSQL).df()
#Devolvió una única fila. Observamos que ésta biblioteca no posee dos mails, sino que está el mismo dos veces
#Hacemos limpieza, escribiéndolo una única vez

bp['mail'] = bp['mail'].replace({'sanestebanbibliotecapopular@yahoo.com.ar <SANESTEBANBIBLIOTECAPOPULAR@YAHOO.COM.AR>': 'sanestebanbibliotecapopular@yahoo.com.ar'})

#--Lo siguiente es asegurar la correctitud de los datos--

#Hemos observado un mail que posee un dominio incorrecto.
#Un dominio está determinado por la presencia de un '@' y, posteriormente (aunque no de forma inmediata), un '.'
#Sin embargo, hay un mail cargado que no cumple con la pauta. La siguiente consulta, lo muestra:   

consultaSQL = """
                SELECT *
                FROM bibliotecas_con_mail
                WHERE mail NOT LIKE '%@%.%'
              """

mail_dominio_incorrecto = dd.sql(consultaSQL).df()

#El mail resultado es 'bib-arocha@educar'.
#Sin embargo, el dominio correcto es 'educ.ar'. Por lo tanto, realizamos el cambio correspondiente.
bp['mail'] = bp['mail'].replace({'bib-arocha@educar': 'bib-arocha@educ.ar'})

#--Revisamos, por último, consistencia entre las distintas bases de datos--

#Comparamos los id_depto de la tabla con los de las tablas originales de Establecimientos educativos y Padrón
#Nota: en el caso de Establecimientos Educativos, se puede extraer el código de departamento a partir de Código de localidad

#Observamos inconsistencia en el id_depto de Chascomús, Buenos Aires; en BP 
#Para arreglarlo, cambiados su id_depto de 6217 a 6218
bp['id_depto'] = bp['id_depto'].replace({6217: 6218})

#%% TABLA MODELO RELACIONAL: PROVINCIA

#Notamos que podemos obtener los id's de las provincias gracias al archivo bibliotecas populares
#Hemos observado la presencia de cada provincia de Argentina en la tabla.
#Por ende nos basta con extraer los ids y nombres de las provincias para formar PROVINCIA

consultaSQL = """
                SELECT DISTINCT id_provincia, provincia AS nombre_provincia
                FROM bibliotecas_populares
              """

provincia = dd.sql(consultaSQL).df()  


#Borramos las variables auxiliares usadas en el proceso.
del bibliotecas_populares

#%% TABLA MODELO RELACIONAL: LOCALIZACION_EE

ee = pd.read_excel('2022_padron_oficial_establecimientos_educativos.xlsx', sheet_name = 'padron2022', skiprows = 5, header = [0,1])

#Seleccionamos aquellos atributos que definimos en el Modelo Relacional
#Debemos tener en cuenta que solo queremos los de Modalidad Común
#Es entonces que armamos el siguiente filtro para seleccionar los jardines, primarios y secundarios de modalidad común
es_modalidad_comun = (ee[('Común', 'Nivel inicial - Jardín maternal')] == 1) | (ee['Común', 'Nivel inicial - Jardín de infantes'] == 1) | (ee[('Común', 'Primario')] == 1)  | (ee[('Común', 'Secundario')] == 1) | (ee[('Común', 'Secundario - INET')] == 1)

#Luego, al momento de seleccionar los EE, tendremos en cuenta que cumplan con la condición planteada
localizacion_ee = ee.loc[es_modalidad_comun, [('Establecimiento - Localización', 'Cueanexo'), ('Establecimiento - Localización', 'Código de localidad')]].copy()

#Hacemos un renombre de las columnas para que haya concordancia con lo predefinido
#Notar que renombramos el atributo 'Código de localidad' a 'id_depto'
nuevas_columnas = ['cueanexo', 'id_depto']
localizacion_ee.columns = nuevas_columnas

#--Realizamos una adaptación de los datos a lo que nosotros buscamos--

#Definimos como tipo de dato int las columnas de nuestra tabla para poder hacer ciertas correcciones
localizacion_ee.astype(int)

#Como hemos mencionado, el código de localidad podía determinar el departamento
#Esta relación consiste en que son aquellos primeros dígitos los que nos indican el departamento
#Vemos que los últimos tres dígitos son los que refieren a cada localidad específica del departamento
#Por lo tanto, quitamos los últimos tres dígitos y nos quedamos con el id del departamento
localizacion_ee.loc[:, 'id_depto'] = localizacion_ee['id_depto'] // 1000

#Por otra parte, notamos inconsistencias entre las tablas en relación a Ciudad de Buenos Aires
#Por un lado, BP no diferencia comunas
#Por el otro, el excel de Padrón Población asigna ids a las comunas que no concuerda con EE
#Es por eso, y analizando que difícilmente una comuna pueda ser considerada departamento, asignamos un id genérico
#Éste id genérico es el usado por BP para referirse a Ciudad de Buenos Aires.
#El id en cuestión es el 2000.
#Particularmente en la tabla de EE, las comunas de la Ciudad están identificadas con cierto patrón.
#Éstas son los números de cuatro cifras que empiezan en 2 (que es el id_provincia de CABA)
#Por lo tanto, aquellas que tengan tal patrón, le asignamos como 2000 su id_depto
localizacion_ee.loc[(localizacion_ee['id_depto'].astype(str).str.startswith('2'))
                    & (localizacion_ee['id_depto'].astype(str).str.len() == 4), 
                    'id_depto'] = 2000


#Borramos las variables auxiliares usadas en el proceso.
del nuevas_columnas, es_modalidad_comun

#%% TABLA MODELO RELACIONAL: NIVEL_EDUCATIVO_EE

#Para su formación, utilizaremos una función que hemos programado.
#Consiste en armar un diccionario de dos claves y una lista de valores en cada una.
#La primer clave es 'cueanexo', que refiere al identificador único de cada establecimiento educativo.
#Ésta clave tendrá asociada una lista con los distintos establecimientos educativos.
#La segunda clave es 'tipo', que refiere al tipo de nivel educativo que presenta un establecimiento.
#Ésta clave tendrá asociada una lista con los distintos tipos de nivel educativo que tiene cada establecimiento

establecimientos = [] #valor que se asociará a la clave 'cueanexo'
tipos = [] #valor que se asociará a la clave 'tipo'

#La lógica es la siguiente: 
#Por cada posición i de 'tipos' y 'establecimientos' están relacionadas
#La posición i en 'establecimientos' marca el cueanexo de un establecimiento; y la posicion i en 'tipos' informará el tipo de establecimiento.
#Si un establecimiento cumple con más de un tipo, entonces aparecerá otro registro en una posicion j donde en 'establecimientos' se informe su clave y en 'tipos' su otro tipo.
#Por lo tanto, estas listas tendrán la misma longitud en cada momento.

#Recorremos ee
for fila in ee.iterrows(): #en iterrows, [0] es el índice de fila y [1] es la serie en la que están cada uno de los atributos
    #Observación solamente evaluamos acorde a la modalidad común
    
    #Primero vemos si el establecimiento posee nivel jardín
    if (fila[1][('Común', 'Nivel inicial - Jardín maternal')] == 1 or fila[1][('Común', 'Nivel inicial - Jardín de infantes')] == 1):
        #Caso afirmativo, agregamos el cueanexo a 'establecimientos'
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        #Agregamos el tipo 'jardin' a 'tipos' 
        tipos.append('jardin')
    
    #En segundo lugar, vemos si el establecimiento posee (posee también) nivel primario. 
    if (fila[1][('Común', 'Primario')] == 1):
        #Caso afirmativo, agregamos (volvemos a agregar) el cueanexo a 'establecimientos'  
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        #Agregamos el tipo 'primario' a 'tipos'
        tipos.append('primario')
        
    #En último lugar, vemos si el establecimiento posee (posee también) nivel secundario. 
    if (fila[1][('Común', 'Secundario')] == 1 or fila[1][('Común', 'Secundario - INET')] == 1):
        establecimientos.append(fila[1][('Establecimiento - Localización', 'Cueanexo')])
        tipos.append('secundario')

#Al finalizar, ya hemos construído las listas 'establecimientos' y 'tipos' acorde a lo planeado.
#Es fundamental notar que las listas se encuentran ordenadas según lo establecido.
#Es decir, su formación fue tal que se cumple lo dictaminado para cada posición i.

#Ahora, inicializamos el diccionario mencionado
nivel_educativo_ee = {'cueanexo' : [], 'tipo' : []}

#Luego, asignamos los valores correspondientes.
nivel_educativo_ee['cueanexo'] = establecimientos
nivel_educativo_ee['tipo'] = tipos

#Finalmente, formamos nuestro dataframe a partir del diccionario.
#La primer columna serán los cueanexos y la segunda los tipos. 
#Como los arrays los dimos ordenados, el dataframe contendrá la información correctamente.
nivel_educativo_ee = pd.DataFrame(data = nivel_educativo_ee) 

#Borramos las variables auxiliares usadas en el proceso.
del establecimientos, tipos, fila, ee


#%% TABLA MODELO RELACIONAL: DEPARTAMENTO - PARTE 1: RECOLECCIÓN DE DATOS

#Ésta tabla presenta una complejidad mayor de formación.
#El nivel de dificultad procede a que la fuente de datos donde se extrae la información posee formato complicado.
#La primer parte del proceso consistirá en transformar éste formato a uno que podamos manejar.

#Primero armamos un dataframe donde se toma la información en el formato en el que se encuentra. 
df = pd.read_excel('padron_poblacion.xlsx', header=None)

#Luego, definimos variables auxiliares que utilizaremos en el proceso de reformateo. 
n_rows = len(df) #la cantidad de filas presentes

#Nuestra intención es crear un DataFrame para cada tabla asociada a los departamentos.
#Éstos DataFrame los iremos adjuntando en una lista que después usaremos para lograr la concatenación total de la información.

#Es por eso que necesitamos definir ciertas variables auxiliares:
segmentos = [] #lista que contendrá los DataFrames
i = 0 #iterador
col_area   = 1  #Llamamos col_area a aquella en donde se indica el area (en el excel, era la B)
col_nombre = 2  #Llamamos col_nombre a aquella en donde se indica el nombre del departamento(en el excel, era la C)

#Recorremos las filas de nuestro DataFrame
while i < n_rows: 
    
    #Recorremos las celdas de la col_area
    celda = df.iat[i, col_area]
    
    #En esta columna, solo nos interesa donde aparezca la palabra clave "AREA"
    if isinstance(celda, str) and celda.strip().startswith('AREA'):
        #Observamos cierto patrón en aquellos valores de col_area donde se define un departamento
        #Este patron es que el id_depto del departamento son los últimos cinco caracteres
        area   = celda.strip()[-5:]
        
        #Y luego su nombre es el dispuesto en col_nombre
        nombre = df.iat[i, col_nombre]

        #Otro patrón que se repite es que la información sobre esa tabla se encuentra dos filas debajo.
        #Definimos un número que marca el lugar donde se halla el encabezado/las columnas de la tabla de cada departamento. 
        header_row = i + 2 
        
        #Primero nos aseguramos de que no estar al final de la tabla
        if header_row >= n_rows:
            break
        
        #Caso contrario, podemos crear el encabezado, que serán los atributos de la tabla asociada al departamento
        header = df.iloc[header_row].tolist() 
        
        #Al estar en la tabla, recorreremos las filas hasta que hallemos una vacía
        #El hallazgo de una fila vacía, representa finalización de la tabla asociada al departamento.
        #Guardamos las filas como listas en el dataframe
        
        #Para recorrer las filas, inicializamos un iterador
        j = header_row + 1 #justamente el número será el siguiente a donde se encuentra el encabezado.
        
        #Inicializamos una lista vacía que contendrá la información de cada fila de la tabla correspondiente al departamento.
        filas = []
        
        #El recorrido se realizará hasta que se termine la tabla del departamento.
        while j < n_rows and not df.iloc[j].isnull().all():
            #Agregamos la fila y avanzamos el iterador
            filas.append(df.iloc[j].tolist())
            j += 1

        #Si hay datos, creamos el sub‑DataFrame, o sea, el DataFrame relacionado a ese departamento.
        if filas:
            #la creación consiste en guardar su código de área, su nombre y la información poblacional detallada por las filas 
            sub = pd.DataFrame(filas, columns=header)
            sub['Area']   = area
            sub['Nombre'] = nombre
            
            #Finalmente, agregamos el sub-dataframe a nuestra lista de Dataframes
            segmentos.append(sub)

        # Luego, el iterador inicializado al inicio, avanzará directamente al final de ésta tabla recorrida.
        i = j + 1
        continue
        
    
    #En caso de que la fila haya sido de interés pues no posee información de un departamento, seguimos avanzando. 
    i += 1


#Al finalizar toda la revisión del archivo, procedemos a hacer la concatenación de los sub-dataframes.
#Es decir, originamos un nuevo dataframe que tiene toda la información obtenida.
#Si bien el formato no es ideal, es lo suficientemente amigable para cumplir nuestro objetivo.

resultado = pd.concat(segmentos, ignore_index=True)
#Eliminamos la columna 0 (en el excel, A) que esta llena de valores NULL
resultado = resultado.drop(resultado.columns[0], axis=1)

#Borramos las variables auxiliares usadas en el proceso.
del df, n_rows, segmentos, i, col_area, col_nombre, celda, area, nombre, header_row, header, j, filas, sub

#%% TABLA MODELO RELACIONAL: DEPARTAMENTO - PARTE 2: FILTRADO DE DATOS

#Ahora trabajamos a partir del formato obtenido.
#Nos enfocamos en obtener, de cada departamento, su área, nombre y datos poblacionales.

#Primero seleccionamos las columnas area y nombre, sin pares duplicados.
#Es decir, creamos otro dataframe que por el momento contiene únicamente la información del código de área y nombre de cada departamento.
pp = resultado[['Area', 'Nombre']].drop_duplicates()

#Para facilitar el manejo de los datos de área, lo pasamos a string.
pp['Area'] = pp['Area'].astype(str)

#Luego, nos enfocamos en el filtrado de los datos poblacionales.
#Nuestra intención es lograr un segundo dataframe que contenga los datos poblacionales de cada departamento.
#El identificador único será el área, cuya presencia tiene un rol clave. 
#Éste será lograr el rejunte de toda la información de los departamentos en una sola tabla.

#Para el segundo DataFrame, tendremos las claves 'Area', 'pob_infantes', 'pob_primaria', 'pob_secundaria' y 'pob_total'
#Las claves tendrán asociadas listas. En principio, vacías. 
#En cada índice i de las listas, se hallará:
    #En Área el código de un departamento.
    #En pob_infantes la población de infantes (niñ@s que atienden el jardín) de ese departamento.
    #En pob_primaria la población de chicos en edad de escolzarización primaria de ese departamento.
    #En pob_secundaria la población de chicos en edad de escolarización secundaria de ese departamento.
    #En pob_total la población total de ese departamento.
data_pp = {'Area' : [], 'pob_infantes': [], 'pob_primaria' : [], 'pob_secundaria' : [], 'pob_total' : []}

#Ahora definimos variables auxiliares que nos ayudarán con el recuento de las poblaciones determinadas.
sumaPobJardin = 0
sumaPobPrimaria = 0
sumaPobSecundaria = 0

#Empezamos a recorrer el DataFrame armado en la parte 1.
#Agarramos el primer área que observamos de éste Dataframe
area = '02007'
#La idea es recorrer todo el dataframe e ir analizando la información que se presenta.
#Yo quiero para cada departamento, agregar a mi diccionario la información sobre su población
#Para lograr el objetivo, vamos consultando el Area 
for fila in resultado.iterrows(): #importante: fila[0] es el índice de la fila, f[1] es la serie los valores de los distintos atributos

    #Primero vemos si nos encontramos con la información de otra área, o ya terminamos el recorrido de la tabla 
    if (fila[1]['Area'] != area or fila[0] == len(resultado) - 1):
        #En ese caso, agregamos el área vista al diccionario
        data_pp['Area'].append(area)
        #Y le adjuntamos la información poblacional de la misma
        data_pp['pob_infantes'].append(sumaPobJardin)
        data_pp['pob_primaria'].append(sumaPobPrimaria)
        data_pp['pob_secundaria'].append(sumaPobSecundaria)
        
        #luego, para que el proceso continúe, si es que no estamos en la última fila, reasignamos el área
        area = fila[1]['Area']
        #además, reinicializamos las variables, para evitar mezcla de información sobre poblaciones distintas
        sumaPobJardin = 0
        sumaPobPrimaria = 0
        sumaPobSecundaria = 0
    
    #Ahora vemos el caso de que estemos procesando la información del mismo departamento
    #A nosotros nos interesa la población infante, primaria y secundaria.

    #Empezamos evaluando si estamos en edad primaria. Evaluamos si la edad es de entre 3 y 5 (inclusive) años   
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(3, 6)):
        #si es ese el caso, suma el dato poblacional de la variable sumaPobJardin
        sumaPobJardin += int(fila[1]['Casos'])
    
    #Evaluamos si estamos en edad primaria, es decir, si tenemos dato de la población de entre 6 y 12 (inclusive) años
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(6, 13)):
        #si es ese el caso, suma el dato poblacional a la variable de sumaPobPrimaria
        sumaPobPrimaria += int(fila[1]['Casos'])
    
    #Evaluamos si estamos en edad secundaria, es decir, si tenemos dato de la población de entre 13 y 18 (inclusive) años
    if (str(fila[1]['Edad']) != 'Total' and int(fila[1]['Edad']) in range(13, 19)):
        #si es ese el caso, suma el dato poblacional a la variable de sumaPobSecundaria
        sumaPobSecundaria += int(fila[1]['Casos'])
    
    #Evaluamos si, en cambio, nos hallamos en la fila donde se indica el total de la población del departamento.
    if (str(fila[1]['Edad']) == 'Total'):
        #Si es ese el caso, agrega el dato al diccionario, en la clave correspondiente a las poblaciones totales de los departamentos.
        data_pp['pob_total'].append(int(fila[1]['Casos']))


#Al finalizar, nos queda un diccionario en donde tenemos los distintos datos poblacionales asociados a cada departamento 
#Es importante notar que los valores asociados a cada clave del diccionario está ordenado tal como se definió

#A partir de este diccionario, armamos un dataframe auxiliar, donde Area, 'pob_infantes', 'pob_primaria', 'pob_secundaria', 'pob_total' son los atributos    
dfaux = pd.DataFrame(data = data_pp)

#Luego, para a traves de una consulta SQL juntamos el código de área, nombre de departamento y los datos poblacionales.
consultaSQL = """
                SELECT *
                FROM pp
                NATURAL JOIN dfaux
              """

pp = dd.sql(consultaSQL).df()


#Borramos las variables auxiliares usadas en el proceso.
del resultado, data_pp, sumaPobJardin, sumaPobPrimaria, sumaPobSecundaria, area, fila, dfaux

#%% TABLA MODELO RELACIONAL: DEPARTAMENTO - PARTE 3: REFINAMIENTO DE DATOS

#Por últimos, nos concentraremos en ver temas de:
    #1)Emprolijamiento de los datos
    #2)Adaptación al modelo relacional propuesto
    #3)Consistencia entre tablas
    
#Empezamos con el emprolijamiento de los datos.    
#En primer lugar, aquellos códigos de área que empiezan en 0, los reescribimos sin éste.
#Todos los códigos tienen 5 dígitos, entonces para identificar que empieza con 0, comparamos el número con el 10000
#A tener en cuenta, el código está como un string.
for indice, fila in pp.iterrows():
    if (int(fila['Area']) < 10000) :
        #En caso de que sea menor de 10000, entonces como tiene 5 dígitos, significa que el primero es 0.
        #Al ser string, agarramos el código a partir del segundo caracter
        pp.at[indice, 'Area'] = fila['Area'][1:]
        

#Seguimos con la adaptación al modelo relacional
#Creamos otra tabla con el nombre correcto: DEPARTAMENTO
#Además, renombramos los atributos 'Area' que será el id_depto; y 'Nombre' será nombre_depto. El resto de los atributos mantendrá el nombre definido.
#Por último, hemos observado que para aquellos departamentos de id de cuatro dígitos, el id de su provincia es su primer número; y en los de cinco dígitos, los dos primeros.
#Todo esto, lo hacemos a través de una consulta SQL
consultaSQL = """
                SELECT Area AS id_depto, Nombre AS nombre_depto, CAST(Area AS INTEGER)//1000 AS id_provincia, pob_infantes, pob_primaria, pob_secundaria, pob_total 
                FROM pp
              """
              
#El resultado de esta consulta, será la tabla DEPARTAMENTO definida en el Modelo Relacional. 
departamento = dd.sql(consultaSQL).df()


#Finalmente, nos enfocamos en la consistencia de los datos. 
#Buscamos que haya coherencia entre las distintas tablas.

#Empezamos modificando los id_depto de Ushuaia y Río Grande, pues en las demás tablas son levemente diferentes.
#Para ello, primero convertimos el id_depto a int.
departamento['id_depto'] = departamento['id_depto'].astype(int)

#Luego, hacemos los cambios: el id de Rio Grande pasa de 94008 a 94007; el de Ushuaia, de 94015 a 94014. 
departamento['id_depto'] = departamento['id_depto'].replace({94008: 94007, 94015: 94014})


#Ahora nos enfocamos en las comunas de la Ciudad de Buenos Aires.
#Juntaremos la información correspondiente a éstas en una única fila correspondiente a Ciudad de Buenos Aires.

#Para cumplir nuestro objetivo, primero renombramos como 'Ciudad de Buenos Aires' a las comunas.
#Observación: los departamentos que se llaman 'Comuna%' todos describen a CABA.
for nombre in departamento['nombre_depto']:
    if (nombre.startswith('Comuna')):
        departamento['nombre_depto'] = departamento['nombre_depto'].replace({nombre: 'Ciudad de Buenos Aires'})


#Creamos un subdataframe con solo las filas con nombre_depto "Ciudad de Buenos Aires"
#En el mismo paso:
    #Agrupamos las filas
    #Sumamos los datos poblacionales correspondientes a cada comuna.

departamentos_de_ciudad_bsas = departamento[departamento['nombre_depto'] == 'Ciudad de Buenos Aires'].groupby('nombre_depto')[['pob_infantes', 'pob_total', 'pob_primaria', 'pob_secundaria']].sum().reset_index()
#Como resultado, queda una única fila.
#A ésta, le asignamos el 2000, que es el id genérico para la Ciudad, como su valor en 'id_depto'.
departamentos_de_ciudad_bsas['id_depto'] = 2000
#Además, definimos que el id_provincia es 2, correspondiente a Ciudad de Buenos Aires 
departamentos_de_ciudad_bsas['id_provincia'] = 2

#Creamos un subdataframe con las filas que no posean como nombre 'Ciudad de Buenos Aires'
#Notar que el conjunto de las filas de cada dataframe son disjuntos entre sí (no se puede pertenecer y no pertenecer a CABA a la vez)
departamentos_fuera_de_ciudad_bsas = departamento[departamento['nombre_depto'] != 'Ciudad de Buenos Aires']

#Finalmente, concatenamos los subdataframe, consiguiendo la tabla original, pero con la información sobre las comunas agrupadas en una única fila de Ciudad de Buenos Aires.
departamento = pd.concat([departamentos_fuera_de_ciudad_bsas, departamentos_de_ciudad_bsas], ignore_index=True)


#Borramos las variables auxiliares usadas en el proceso.
del indice, fila, nombre, consultaSQL, departamentos_de_ciudad_bsas, departamentos_fuera_de_ciudad_bsas


#%%PASAMOS A ARCHIVOS .CSV NUESTRAS TABLAS
bp.to_csv('bp', index = False)
localizacion_ee.to_csv('localizaciones_ee', index = False)
nivel_educativo_ee.to_csv('nivel_educativo_ee', index = False)
provincia.to_csv('provincia', index =  False)
departamento.to_csv('departamento', index = False)