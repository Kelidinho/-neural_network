# Predicción de Demanda en Transporte Público

## Propósito del Proyecto

Este repositorio documenta el proceso de aprendizaje y desarrollo para construir un modelo de **Machine Learning** capaz de predecir la demanda de pasajeros en el transporte público. El objetivo principal no es solo alcanzar una solución final, sino también **reconstruir y fortalecer los fundamentos de programación, lógica algorítmica y matemáticas aplicadas** que sustentan la inteligencia artificial.

El proyecto comienza desde los conceptos más básicos, implementando algoritmos fundamentales manualmente con librerías como NumPy para asegurar una comprensión profunda de su funcionamiento interno. Progresivamente, avanzará hacia el uso de frameworks modernos y arquitecturas de modelos complejas, como los **Temporal Fusion Transformers (TFT)**, especializadas en el análisis de series temporales.

Este es un proyecto de formación práctica que sirve como un puente entre la programación de software tradicional y la ingeniería de Machine Learning, abordando los desafíos de una manera estructurada, modular y reproducible.

---

## Pila Tecnológica (Tech Stack)

Este proyecto utiliza un conjunto de herramientas modernas para asegurar la reproducibilidad y eficiencia del desarrollo:

- **Lenguaje:** Python 3.12
- **Cálculo y Datos:** NumPy, Pandas
- **Visualización:** Matplotlib, Seaborn
- **Entorno Interactivo:** JupyterLab
- **Base de Datos:** MariaDB (gestionada con Docker)
- **Contenerización:** Docker, Docker Compose
- **Calidad de Código:** Black, Ruff

---

## Estructura y Metodología

El desarrollo sigue una **Arquitectura Modular Orientada a Pipelines**, separando la experimentación del código de producción. La estructura es la siguiente:

-   `data/`: Almacenamiento de datasets (CSV, etc.)
-   `environment/`: Ficheros de configuración de Docker (develop, pro)
-   `notebooks/`: Jupyter Notebooks para exploración y experimentación
-   `scripts/`: Scripts de utilidad (ej. run-dev.sh, stop.sh)
-   `src/`: Código fuente de la aplicación
    -   `data_processing/`: Módulos para carga y preprocesamiento de datos
    -   `models/`: Módulos para cada modelo de ML
    -   `utils/`: Funciones auxiliares reutilizables
-   `storage/`: Volúmenes persistentes de Docker (ej. datos de la BD)
-   `requirements.txt`: Lista de dependencias de Python

La metodología se centra en:

1.  **Fundamentos Primero:** Comprensión y aplicación de conceptos matemáticos a través de la implementación de código.
2.  **Modularidad:** Construcción de componentes reutilizables para el procesamiento de datos, entrenamiento y predicción.
3.  **Reproducibilidad:** Uso de Docker y scripts para garantizar un entorno de desarrollo consistente.

---

## Cómo Empezar

Para configurar el entorno de desarrollo local, siga estos pasos:

1.  **Clonar el Repositorio**
    ```bash
    git clone [URL-DEL-REPOSITORIO]
    cd [NOMBRE-DEL-REPOSITORIO]
    ```

2.  **Configurar el Entorno Virtual**
    Se recomienda el uso de un entorno virtual para gestionar las dependencias.
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar Dependencias**
    Todas las librerías necesarias están listadas en el fichero `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar el Entorno Dockerizado**
    El proyecto utiliza una base de datos MariaDB gestionada a través de Docker. Los siguientes scripts gestionan el ciclo de vida del entorno.

    -   Para iniciar los servicios:
        ```bash
        ./scripts/run-dev.sh
        ```
    -   Para detener los servicios:
        ```bash
        ./scripts/stop.sh
        ```
    Una vez completado, la base de datos estará disponible en `localhost:3306` y el entorno estará listo para comenzar a trabajar.

---

## Cómo Contribuir

Aunque este es principalmente un proyecto de aprendizaje personal, las contribuciones que sigan buenas prácticas son bienvenidas. El flujo de trabajo sugerido es:

1.  Crea un fork del repositorio.
2.  Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nombre-feature`).
3.  Realiza tus cambios y haz commit (`git commit -m "feat: Describe tu cambio"`).
4.  Haz push a tu rama (`git push origin feature/nombre-feature`).
5.  Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el fichero `LICENSE` para más detalles.