# Proyecto ETL - PREMIER PADEL 2024

## Descripción
Este proyecto ETL (Extracción, Transformación y Carga) tiene como objetivo recopilar y analizar datos de los torneos de PREMIER PADEL 2024. Los datos extraídos permiten realizar un análisis en Looker Studio sobre:
- Cantidad de torneos por categoría.
- Ubicación de los torneos (país y ciudad).
- Cantidad de torneos ganados por cada pareja.
- Cantidad de premios obtenidos por cada jugador.

## Tecnologías utilizadas
El desarrollo del proyecto está realizado en **Python**, utilizando las siguientes herramientas:

- **Extracción de datos:** `playwright`
- **Transformación de datos:** `pandas`
- **Carga de datos en base de datos:** `sqlalchemy`
- **Base de datos:** `PostgreSQL`
- **Visualización de datos:** `Looker Studio`

## Arquitectura del Proyecto
1. **Extracción de datos:** Se utiliza Playwright para navegar y extraer información de los torneos desde fuentes web.
2. **Transformación de datos:** Mediante Pandas, los datos se limpian, estructuran y transforman en un formato adecuado para el análisis.
3. **Carga en base de datos:** SQLAlchemy se emplea para cargar los datos en una base de datos PostgreSQL.
4. **Visualización:** Se crea un dashboard en Looker Studio para analizar los datos obtenidos.

## Instalación y Configuración
### Requisitos previos
Asegúrate de tener:
- Instalado Python 3.9+
- Acceso a una base de datos PostgreSQL
- Dependencias del proyecto (indicadas en `requirements.txt`)

### Instalación
Clona este repositorio:
```bash
$ git clone https://github.com/nicocorddoba/padel-etl.git
$ cd padel-etl
```
Instala las dependencias:
```bash
$ pip install -r requirements.txt
```
Configura las credenciales de la base de datos PostgreSQL asignando una variable de entorno con el nombre de POSTGRES_URL.

## Uso
Ejecuta el proceso ETL con:
```bash
$ python main.py
```
Esto iniciará la extracción, transformación y carga de los datos en la base de datos PostgreSQL.

## Dashboard en Looker Studio
El análisis de los datos se puede visualizar en el dashboard de Looker Studio, donde se presentan los KPIs y gráficos relevantes sobre los torneos de PREMIER PADEL 2024.
https://lookerstudio.google.com/reporting/d3e5094e-a2ad-495e-b9f4-aaf65b3e73e9

## Contribuciones
Si deseas contribuir a este proyecto, siéntete libre de hacer un fork.

