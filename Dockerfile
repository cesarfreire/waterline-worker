# Usa a imagem base do Python
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY main.py .
COPY ESP8266.cert.pem .
COPY ESP8266.private.pem .
COPY root-CA.crt .
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o worker
CMD ["python", "main.py"]
