# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 08:25:14 2025

@author: ASUS
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import duckdb as dd
import seaborn as sns

#%%
fashion = pd.read_csv('Fashion-MNIST.csv')

#Eliminamos la primer fila pues únicamente es el indice de la fila
fashion = fashion.drop(columns=['Unnamed: 0'])

# Plot imagen 

img = fashion.iloc[32000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% SEPARAMOS EL DATASET POR PRENDA

remera_top = fashion[fashion['label'] == 0]
pantalon = fashion[fashion['label'] == 1]
pullover = fashion[fashion['label'] == 2]
vestido = fashion[fashion['label'] == 3]
saco = fashion[fashion['label'] == 4]
sandalia = fashion[fashion['label'] == 5]
camisa = fashion[fashion['label'] == 6]
zapatilla = fashion[fashion['label'] == 7]
cartera = fashion[fashion['label'] == 8]
bota = fashion[fashion['label'] == 9]

#Nota: los dataset tienen en mismo tamaño, por lo tanto hay misma cantidad de cada clase de prenda

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: REMERAS/TOPS

img = remera_top.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = remera_top.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = remera_top.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = remera_top.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = remera_top.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 


#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: PANTALONES

img = pantalon.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pantalon.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pantalon.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pantalon.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pantalon.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#Distingir pantalones parece fácil; solo hay que considerar que haya espacio vació en el medio y lineas largas rodeandolo

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: PULLOVER

img = pullover.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pullover.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pullover.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pullover.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = pullover.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: VESTIDO

img = vestido.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = vestido.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = vestido.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = vestido.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = vestido.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: SACO

img = saco.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = saco.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = saco.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = saco.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = saco.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: SANDALIAS

img = sandalia.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = sandalia.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = sandalia.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = sandalia.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = sandalia.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show()

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: CAMISAS

img = camisa.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = camisa.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = camisa.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = camisa.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = camisa.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% #%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: ZAPATILLAS

img = zapatilla.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = zapatilla.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = zapatilla.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = zapatilla.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = zapatilla.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: CARTERA

img = cartera.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = cartera.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = cartera.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = cartera.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = cartera.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%% VISUALIZAMOS VARIAS IMÁGENES DE CADA SUBCONJUNTO: BOTAS

img = bota.iloc[0, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = bota.iloc[6999, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = bota.iloc[3500, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = bota.iloc[100, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

img = bota.iloc[1000, :-1].values.reshape((28,28)) 
plt.imshow(img, cmap='gray') 
plt.show() 

#%%IMÁGENES PROMEDIO CALZADOS
promedio_bota = bota.mean()

img = promedio_bota.values[:-1].reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()


promedio_sandalia = sandalia.mean()
              
img = promedio_sandalia.values[:-1].reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()      


              
promedio_zapatilla = zapatilla.mean()
              
img = promedio_zapatilla.values[:-1].reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()   
              
#%% IMÁGENES PROMEDIO PRENDAS TORSO

promedio_remera_top = remera_top.mean()

img = promedio_remera_top[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()


promedio_camisa = camisa.mean()
              
img = promedio_camisa[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()      


              
promedio_pullover = pullover.mean()
              
img = promedio_pullover[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()  


promedio_saco = saco.mean()
              
img = promedio_saco[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()  


promedio_vestido = vestido.mean()
              
img = promedio_vestido[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()  

#%% PROMEDIO PANTALON Y CARTERA

promedio_pantalon = pantalon.mean()
              
img = promedio_pantalon[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()  


promedio_cartera = cartera.mean()
              
img = promedio_cartera[:-1].values.reshape((28,28))
plt.imshow(img, cmap = 'gray')
plt.show()  
#%% PASO LAS SERIES DE LOS PROMEDIOS A DATAFRAMES
df_promedio_bota = promedio_bota.to_frame().T
df_promedio_camisa = promedio_camisa.to_frame().T
df_promedio_cartera = promedio_cartera.to_frame().T
df_promedio_pantalon = promedio_pantalon.to_frame().T
df_promedio_pullover = promedio_pullover.to_frame().T
df_promedio_remera_top = promedio_remera_top.to_frame().T
df_promedio_saco = promedio_saco.to_frame().T
df_promedio_sandalia = promedio_sandalia.to_frame().T
df_promedio_vestido = promedio_vestido.to_frame().T
df_promedio_zapatilla = promedio_zapatilla.to_frame().T

#%% PONGO LOS PROMEDIOS EN UNA TABLA

consultaSQL = """
                SELECT * FROM df_promedio_bota
                UNION
                SELECT * FROM df_promedio_camisa
                UNION
                SELECT * FROM df_promedio_cartera
                UNION
                SELECT * FROM df_promedio_pantalon
                UNION
                SELECT * FROM df_promedio_pullover
                UNION
                SELECT * FROM df_promedio_remera_top
                UNION
                SELECT * FROM df_promedio_saco
                UNION
                SELECT * FROM df_promedio_sandalia
                UNION
                SELECT * FROM df_promedio_vestido
                UNION
                SELECT * FROM df_promedio_zapatilla;

              """

df = dd.sql(consultaSQL).df()

#con el pixel1,2,3,4,5,6,7,8,12,13,18,21,22,23,24,25 se puede distinguir a la zapatilla del resto porque es la única prenda que no tiene nada ahí
#desde el pixel 155 al pixel165, la zapatilla presenta gran diferencia de intensidad
#en los pixeles 169,170 hay una gran diferencia entre la cartera y el resto 


#%% SCATTERPLOT PROMEDIO PANTALÓN
sns.scatterplot(x = promedio_pantalon.index, y = promedio_pantalon.values)

plt.xticks(' ')

#%% SCATTERPLOT PROMEDIO ZAPATILLA
sns.scatterplot(x = promedio_zapatilla.index, y = promedio_zapatilla.values)

#%% SCATTERPLOT PROMEDIO CARTERA
sns.scatterplot(x = promedio_cartera.index, y = promedio_cartera.values)

#%% SCATTERPLOT PROMEDIO SANDALIA
sns.scatterplot(x = promedio_sandalia.index, y = promedio_sandalia.values)

#%% SCATTERPLOT PROMEDIO BOTA
sns.scatterplot(x = promedio_bota.index, y = promedio_bota.values) 

#es el que menor alcance de intensidad presenta; con maximos cercanos a 120 

#%% SCATTERPLOT PROMEDIO REMERA-TOP
sns.scatterplot(x = promedio_remera_top.index, y = promedio_remera_top.values)

#%% SCATTERPLOT PROMEDIO CAMISA
sns.scatterplot(x = promedio_camisa.index, y = promedio_camisa.values)

#%% SCATTERPLOT PROMEDIO PULLOVER
sns.scatterplot(x = promedio_pullover.index, y = promedio_pullover.values)

#%% SCATTERPLOT PROMEDIO SACO
sns.scatterplot(x = promedio_saco.index, y = promedio_saco.values)

#%% SCATTERPLOT PROMEDIO VESTIDO
sns.scatterplot(x = promedio_vestido.index, y = promedio_vestido.values)