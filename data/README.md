📂 Recopilación de Datos - Predicción de Demanda de Autobuses

Este documento detalla el origen, la descripción y el método de adquisición de los datos utilizados para el modelo de predicción de demanda de rutas de autobús.

🌎 Fuente de los Datos

Los datos se obtienen a través de la API pública proporcionada por la Autoridad de Transporte Metropolitano (MTA) de la ciudad de Nueva York. La MTA publica una gran variedad de conjuntos de datos operativos en su portal de datos abiertos, alojado en la plataforma Socrata.

    Organización: Metropolitan Transportation Authority (MTA)

    Ciudad: Nueva York, EE. UU.

    Plataforma: Socrata Open Data

    Enlace al Dataset: MTA Bus Hourly Ridership

📊 Descripción de los Datos

El conjunto de datos contiene información sobre el número de pasajeros por hora (ridership) para cada ruta de autobús de la red de la MTA. Es un dataset de series temporales ideal para modelar y predecir la demanda de pasajeros.

Para nuestro proyecto, no utilizamos el dataset completo (que supera los 300 millones de registros), sino que extraemos un subconjunto relevante a través de la API. Las columnas principales que utilizamos son:

    transit_timestamp: La fecha y hora exactas del registro.

    bus_route: El identificador de la ruta de autobús (ej: 'M15', 'Q58').

    ridership: El número de pasajeros registrados en esa hora para esa ruta.

    transfers: El número de transbordos realizados.

⚙️ Método de Adquisición: API de Socrata

Para evitar la descarga masiva de datos, accedemos a la información mediante una llamada directa a la API de Socrata. Utilizamos su lenguaje de consulta (SoQL), similar a SQL, para filtrar y solicitar únicamente un subconjunto de los datos.

Esto nos permite definir:

    Un periodo de tiempo específico (ej: todo el año 2023).

    Un conjunto de rutas de autobús concretas.

Este método es eficiente, reproducible y nos proporciona un dataset manejable y enfocado para el entrenamiento del modelo.
