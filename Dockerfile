FROM python:3.11.7
WORKDIR /app

# Copia los archivos de requisitos y actualiza pip
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia los archivos CSS, documentos y otros recursos necesarios
COPY ./data /app/data/
COPY ./results /app/results/

# Copia el resto de la aplicación
COPY . .

# Exponer el puerto para el contenedor
EXPOSE 8082

# Comando de entrada para ejecutar la aplicación
ENTRYPOINT [ "streamlit", "run", "main.py", "--server.port=8082", "--server.address=0.0.0.0" ]
