# Análisis de Distribución: Establecimientos Educativos y Bibliotecas Populares en Argentina

Este repositorio presenta una solución técnica basada en datos públicos para investigar la relación entre infraestructura educativa y cultural en Argentina, a nivel departamental. La propuesta abarca todo el flujo: desde la recolección y modelado de datos hasta el análisis visual y estadístico.

---

## 🎯 Objetivos del proyecto

- Integrar datos educativos, culturales y poblacionales desde fuentes públicas oficiales.
- Modelar conceptualmente las relaciones entre las entidades para apoyar el análisis.
- Identificar y cuantificar problemas de calidad mediante métricas GQM.
- Generar reportes con SQL y comunicar hallazgos mediante visualizaciones efectivas.
- Evaluar correlaciones entre instituciones y población a nivel regional.

---

## 🧰 Herramientas y tecnologías

- **Python**: pandas, numpy, matplotlib, seaborn, duckdb
- **SQL**: consultas embebidas para análisis estructurado
- **Diseño de datos**: DER, normalización (3FN), claves primarias y foráneas
- **Documentación técnica**: código comentado y y resultados replicables

---

## 📊 Visualizaciones incluidas

- Cantidad de BP por provincia
- Relación entre EE y población por nivel educativo
- Boxplots de EE por provincia
- Comparativas de EE y BP cada mil habitantes

---

## 🧠 Enfoque metodológico

1. Planteo del problema y selección de fuentes relevantes
2. Diseño del modelo relacional (DER + esquema normalizado)
3. Limpieza y validación de datos con métricas GQM
4. Generación de reportes con SQL embebido
5. Análisis visual con herramientas de gráficos exploratorios

---

## 🔍 Resultados clave
Se evaluó si existe correlación entre la cantidad de BP y EE por departamento, considerando la influencia de la población. Las conclusiones se sustentan con indicadores gráficos y cuantitativos.

---

## 👥 Autores
- Arango, Joaquin
- Cardinale, Dante
- Herrero, Lucas

---

## 🔗 Fuentes utilizadas
. Padrones de Establecimientos Educativos
. Bibliotecas Populares
. Población por Departamento (INDEC)
