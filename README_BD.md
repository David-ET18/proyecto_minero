## Almacenamiento + consultas (InfluxDB)

Esto guarda las temperaturas que llegan por MQTT en InfluxDB, y las consulta de vuelta.

Requisitos antes de correrlo:
- El broker MQTT (EMQX) corriendo, con el simulador publicando.
- Una InfluxDB corriendo (local o la que estés usando), con un bucket creado.

Instalar dependencias:

```
pip install -r requirements.txt
```

Configurar variables de entorno con tus datos reales (broker e InfluxDB):

```
$env:MQTT_BROKER="tu_broker"
$env:MQTT_PORT="1883"
$env:MQTT_TOPIC="iot/minera/gabinete_electrico/temperatura"
$env:INFLUX_URL="http://localhost:8086"
$env:INFLUX_TOKEN="tu_token"
$env:INFLUX_ORG="tu_org"
$env:INFLUX_BUCKET="tu_bucket"
```

Guardar los datos (déjalo corriendo):

```
python mqtt_to_influx.py
```

Consultar lo guardado (última temperatura, histórico, lecturas sobre el umbral):

```
python consultas_influx.py
```

Para Grafana: datasource InfluxDB (Flux), apuntando al mismo bucket/measurement (`temperatura_gabinete`, field `temperatura`). Dashboard listo para importar: `grafana/dashboard_gabinete_electrico.json`.

Guía completa de instalación de InfluxDB sin Docker: `INSTALACION.md`.
