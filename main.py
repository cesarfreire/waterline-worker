import paho.mqtt.client as mqtt
import pymongo
import json
import os
import logging
import datetime
import pytz

logging.basicConfig(level=logging.INFO)
class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[{os.getenv('WORKER_MODE')}] {msg}", kwargs
logger = CustomAdapter(logging.getLogger(__name__), {})

# Definir o fuso horário de São Paulo (UTC-3)
br_tz = pytz.timezone("America/Sao_Paulo")

# Conectar ao MongoDB
client_mongo = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client_mongo[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]

def on_connect(client, userdata, flags, rc):
    """ Callback quando o worker se conecta ao MQTT """
    logger.info(f"Conectado ao AWS IoT com código de resultado: {str(rc)}")
    client.subscribe(os.getenv("MQTT_TOPIC"))

def on_message(client, userdata, msg):
    """ Callback quando uma mensagem chega """
    logger.info(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

    try:
        # Converter JSON recebido
        data = json.loads(msg.payload.decode())

        if "timestamp" in data:
            # boot_time_ms = data["time"]
            # now_utc = datetime.datetime.now(datetime.timezone.utc)
            # timestamp_utc = now_utc - datetime.timedelta(milliseconds=boot_time_ms)

            # # Converter de UTC para UTC-3
            # timestamp_br = timestamp_utc.astimezone(br_tz)

            # data["timestamp"] = timestamp_br  # Salva no MongoDB com UTC-3
            # data["timezone"] = "America/Sao_Paulo"
            # del data["time"]  # Remove o campo "time" original
            
            iso_timestamp_str = data["timestamp"]
            data["timestamp"] = datetime.datetime.fromisoformat(iso_timestamp_str.replace('Z', '+00:00'))

        # Inserir no MongoDB
        collection.insert_one(data)
        logger.info(f"Dados salvos no MongoDB: {data}")

    except Exception as e:
        logger.error(f"Erro ao salvar no MongoDB: {str(e)}")

def run():
    # Configurar cliente MQTT
    client = mqtt.Client()
    # Conectar ao AWS IoT
    client.tls_set(
        "root-CA.crt",
        "ESP8266.cert.pem",
        "ESP8266.private.pem"
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("AWS_IOT_ENDPOINT"), int(os.getenv("MQTT_PORT")), 60)

    # Manter o worker rodando
    client.loop_forever()


if __name__ == "__main__":
    run()
