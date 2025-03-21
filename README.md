
# Análisis de Causa Raíz para Servicios Bancarios - Davivienda

Este repositorio contiene el código necesario para realizar un análisis de causa raíz sobre los servicios bancarios de Davivienda. El objetivo es identificar y categorizar los problemas más frecuentes reportados en los servicios, a través de un procesamiento y filtrado detallado de los datos.

## Requisitos de la Base de Datos

El archivo de entrada debe contener las siguientes columnas:

- **PRODUCTOS**: Identifica el producto o servicio relacionado con el problema.
- **DESCRIPCION**: Describe el problema reportado.
- **CANAL_ORIGEN**: Indica el canal desde donde se originó el problema (e.g., sucursal, banca en línea, etc.).
- **MOTIVO**: Tipificación del asesor.
- **GRUPO2**: Grupo categorizador que indica si el registro pertenece a "No fraude" o "Empresas 2da Linea".
- **ESTADO**: Indica el estado actual del reporte (e.g., abierto, cerrado).

### Nota:

Si la base de datos no incluye la columna **PRODUCTOS**, es necesario solicitar el archivo `TODOSQR.xlsx` y cruzar los registros utilizando la columna **NUMERO_SS**.
## Filtrado de Datos

El proceso de análisis excluirá los siguientes registros:

1. Registros pertenecientes a "No fraude" o "Empresas 2da Linea" en la columna **GRUPO2**.
2. Registros marcados como "cerrados" en la columna **ESTADO**, ya que normalmente no contienen la información relevante en la columna **DESCRIPCION**.

## Configuración del Entorno

Para ejecutar el código, se debe configurar un archivo `.env` en la raíz del proyecto con la siguiente variable:

```bash
OPENAI_API_KEY=tu_api_key_aqui
```

Donde `tu_api_key_aqui` debe ser reemplazado con la clave de API correspondiente.

## Iniciar el Entorno Virtual

Para configurar y utilizar un entorno virtual, sigue estos pasos:

### Paso 1: Crear el Entorno Virtual

En la raíz del proyecto, ejecuta el siguiente comando para crear un entorno virtual:

```bash
python -m venv venv
```
Esto creará un entorno virtual llamado venv en tu proyecto.

### Paso 2: Activar el Entorno Virtual
#### En Windows:

```bash
venv\Scripts\activate
```

#### En macOS y Linux:

```bash
source venv/bin/activate
```
Una vez activado el entorno virtual, deberías ver el nombre del entorno (venv) precediendo a tu línea de comandos.

## Instrucciones de Ejecución

1. Instalar las dependencias necesarias utilizando el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. Iniciar el servidor local ejecutando el archivo `main.py` con Streamlit:

   ```bash
   streamlit run main.py
   ```

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la lógica de procesamiento y análisis de los datos.
- `requirements.txt`: Archivo que contiene todas las dependencias necesarias para ejecutar el proyecto.
- `.env`: Archivo de configuración que almacena las variables de entorno sensibles como la API key de OpenAI.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, revisa el archivo `LICENSE`.

