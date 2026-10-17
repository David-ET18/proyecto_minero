import os

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "iot/minera/gabinete_electrico/temperatura")

INFLUX_URL = os.environ.get("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN", "REEMPLAZA_CON_TU_TOKEN")
INFLUX_ORG = os.environ.get("INFLUX_ORG", "ta3-minero")
INFLUX_BUCKET = os.environ.get("INFLUX_BUCKET", "gabinete_electrico")

influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)


def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado al broker MQTT con código {rc}. Suscribiendo a '{MQTT_TOPIC}'...")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        temperatura = float(msg.payload.decode())
    except ValueError:
        print(f"Mensaje no numérico ignorado: {msg.payload!r}")
        return

    punto = (
        Point("temperatura_gabinete")
        .tag("sector", "minero")
        .tag("equipo", "gabinete_electrico")
        .field("temperatura", temperatura)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=punto)
    print(f"Guardado en InfluxDB: {temperatura:.2f}°C")


try:
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except AttributeError:
    mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
