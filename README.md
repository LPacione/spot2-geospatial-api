# Spot2 Geospatial API

API utilizada para la búsqueda, filtrado y análisis geoespacial de datos relacionados con **Props** y **Spots**. El objetivo de este informe es adjuntar la información necesaria para replicar la existencia de la API, realizar la carga de datos y utilizar los endpoints definidos.

## 📑 Índice
1. [Configuración y Entorno](#1-configuración-y-entorno)
2. [Endpoints de la API](#2-endpoints-de-la-api)
3. [Carga de Datos Inicial](#3-carga-de-datos-inicial)
4. [Verificación y Ejemplos de Consultas](#4-verificación-y-ejemplos-de-consultas)
5. [Ejecución de Tests](#5-ejecución-de-tests)

---

## 1. Configuración y Entorno

Los siguientes comandos deben ejecutarse para levantar los servicios y la base de datos.

### 1.1 Levantar Servicios

```bash
docker-compose up -d
```

### 1.2 Aplicar Migraciones

Una vez que el contenedor está funcionando correctamente, se crean y aplican las migraciones ejecutando los siguientes comandos **dentro del contenedor**:

```bash
docker-compose exec app python manage.py makemigrations inventory
docker-compose exec app python manage.py migrate
```
----------

## 2. Endpoints de la API

Los endpoints y schemas creados pueden verificarse en el Swagger, accesible en `/api/docs`

### Spots

**GET**`/api/spots/`

Listar spots. Permite filtrado por `sector`, `type`, `municipality`.

**GET**`/api/spots/{spot_id}/`

Obtener un spot específico por su ID.

**GET**`/api/spots/average-price-by-sector/`

Obtener el precio promedio de spots por sector.

**GET**`/api/spots/nearby/`

Obtener spots cercanos. Requiere `lat`, `long` y `radius` como atributos.

**GET**`/api/spots/top-rent/`

Obtener los spots con el alquiler más alto. Acepta el atributo opcional `limit`.

**POST**`/api/spots/within/`

Obtener spots dentro de un polígono. Requiere un JSON de tipo `Polygon` en el cuerpo.

### Props

**GET** `/api/props/`

Listar todas las propiedades.

**GET** `/api/props/{public_id}/`

Obtener una propiedad específica por su ID

----------
## 3. Carga de Datos Inicial

Antes de la carga, la base de datos está vacía. Una vez que los endpoints están creados, se procede a ejecutar los siguientes comandos personalizados dentro del contenedor para cargar los datos:

```
docker-compose exec app python manage.py load_spots
#Load completed: 2052 rows created, 0 omitted 
```

```
docker-compose exec app python manage.py load_props
#Load completed: 64 rows created/updated, 0 omitted 
```

Se añadió una salida por consola para que quien ejecute estos comandos personalizados pueda confirmar de manera visual y ágil los resultados.

----------
## 4. Verificación y Ejemplos de Consultas

Luego de la carga, se pueden probar los _endpoints_.

### Ejemplo de Consulta: `/api/spots/`

-   **Estado Antes de la Carga**: `{"count": 0, "results": []}`
    
-   **Estado Después de la Carga**: `{"count": 2052, ...}`
    

### Ejemplo de Consulta: `/api/props/`

-   **Estado Antes de la Carga**: `{"count": 0, "results": []}`
    
-   **Estado Después de la Carga**: `{"count": 64, ...}`

----------
## 5. Ejecución de Tests

Se crearon tests para cada _endpoint_ de Props y Spots, incluyendo un test para el filtro de Spots y tests para validar el uso correcto de los métodos (GET, POST).

Para ejecutar los tests, sigue estos pasos:

1.  *Acceder al contenedor*:
    
    ```
    docker exec -it spot2_app bash
    ```
    
2.  Ejecutar los tests:
    
    ```
    python manage.py test
    #Ran 10 tests in 0.095s OK 
    ```

----------
## 6. Utilización de IAs como asistencia

La asistencia por parte de herramientas de IA fueron:

En primer lugar, utilice Gemini como soporte para la planificación del proceso, ya que considero que es la más adecuada para este tipo de tareas. Luego, una vez avanzado el proyecto, me permiti "dialogar" para explicarle mis avances y hacia donde pensaba avanzar y con que fundamentos, para obtener una opinion o tal vez descubrir algun pain point que estaba obviando.
En segundo lugar, para la parte técnica opte por apoyarme en ChatGPT, ya que considero que es mas útil para este tipo de tareas ligadas al código, por ejemplo en errores que pude haber tenido con un output era muy extenso para no perder tiempo.

Considero que es una herramienta en la que, bien utilizada, podemos apoyarnos ya sea para mejorar nuestro código, para ahorrar tiempo o para aprender, es por ese motivo que decido incluirla en mis tareas. Obviamente hay recaudos a tomar, sobre todo en lugares productivos o en situaciones con PII.
