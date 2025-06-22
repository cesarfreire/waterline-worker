# Waterline - Worker MQTT para MongoDB

Este serviço é um worker em Python responsável por atuar como uma ponte entre o broker MQTT da AWS IoT Core e o banco de dados MongoDB. Sua principal função é assinar um tópico MQTT específico, receber os dados enviados pelos dispositivos IoT (como o ESP8266) e persistir essas informações no MongoDB para consultas futuras pela aplicação web.

## ➡️ Fluxo de Dados

O fluxo de informação que este worker gerencia é o seguinte:

**Dispositivo IoT (ESP8266)** → Publica dados no Tópico MQTT → **AWS IoT Core** → **Este Worker** (assina o tópico) → Salva os dados no → **MongoDB**

## ✅ Pré-requisitos

Antes de executar o worker, certifique-se de que você tem os seguintes pré-requisitos:

- **Python 3.8+** instalado.
- **Docker** instalado.
- **Docker compose** instalado.
- Credenciais e **certificados válidos** para se conectar ao seu endpoint da AWS IoT Core.

## 🛠️ Instalação

1.  **Clone o repositório** onde este worker está localizado:

    ```bash
    git clone https://github.com/cesarfreire/waterline-worker.git
    cd waterline-worker
    ```

2.  **Copie os certificados da AWS IoT** para o mesmo diretório

    - `root-CA.crt` - O certificado da Autoridade Raiz da Amazon.
    - `ESP8266.cert.pem` - O certificado do seu "dispositivo" (coisa) cadastrado na AWS IoT.
    - `ESP8266.private.pem` - A chave privada correspondente ao certificado do dispositivo.

3.  **Copie o arquivo `sample.env` para um novo arquivo chamado `prod.env` e ajuste os dados** conforme necessário.

4.  **Execute o docker compose**

    ```bash
    docker compose up -d
    ```
