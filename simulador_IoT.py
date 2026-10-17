import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/minera/gabinete_electrico/temperatura"
INTERVALO_SEGUNDOS = 10
UMBRAL_C = 45.0

RANGO_NORMAL = (25.0, 42.0)
RANGO_SOBRECALENTAMIENTO = (46.0, 55.0)
PROBABILIDAD_SOBRECALENTAMIENTO = 0.15

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

client.connect(BROKER, PORT, 60)

print(f"Conectado al broker {BROKER}:{PORT}. Publicando en '{TOPIC}' cada {INTERVALO_SEGUNDOS} segundos...")

while True:
    if random.random() < PROBABILIDAD_SOBRECALENTAMIENTO:
        temperatura = random.uniform(*RANGO_SOBRECALENTAMIENTO)
    else:
        temperatura = random.uniform(*RANGO_NORMAL)

    alerta = " ⚠️ SUPERA EL UMBRAL - requiere inspección" if temperatura > UMBRAL_C else ""
    print(f"Temperatura del gabinete eléctrico: {temperatura:.2f}°C{alerta}")

    client.publish(TOPIC, f"{temperatura:.2f}")

    time.sleep(INTERVALO_SEGUNDOS)
