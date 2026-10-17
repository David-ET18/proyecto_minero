import os

from influxdb_client import InfluxDBClient

INFLUX_URL = os.environ.get("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN", "REEMPLAZA_CON_TU_TOKEN")
INFLUX_ORG = os.environ.get("INFLUX_ORG", "ta3-minero")
INFLUX_BUCKET = os.environ.get("INFLUX_BUCKET", "gabinete_electrico")
UMBRAL_C = 45.0

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()


def ultima_temperatura():
    flux = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "temperatura_gabinete" and r._field == "temperatura")
      |> last()
    '''
    tablas = query_api.query(flux)
    for tabla in tablas:
        for registro in tabla.records:
            print(f"Última temperatura: {registro.get_value():.2f}°C a las {registro.get_time()}")


def historico(minutos=30):
    flux = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutos}m)
      |> filter(fn: (r) => r._measurement == "temperatura_gabinete" and r._field == "temperatura")
    '''
    tablas = query_api.query(flux)
    for tabla in tablas:
        for registro in tabla.records:
            print(f"{registro.get_time()} -> {registro.get_value():.2f}°C")


def lecturas_sobre_umbral(minutos=60):
    flux = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutos}m)
      |> filter(fn: (r) => r._measurement == "temperatura_gabinete" and r._field == "temperatura")
      |> filter(fn: (r) => r._value > {UMBRAL_C})
    '''
    tablas = query_api.query(flux)
    for tabla in tablas:
        for registro in tabla.records:
            print(f"{registro.get_time()} -> {registro.get_value():.2f}°C (supera {UMBRAL_C}°C)")


if __name__ == "__main__":
    print("--- Última temperatura ---")
    ultima_temperatura()

    print("\n--- Histórico (últimos 30 min) ---")
    historico()

    print("\n--- Lecturas que superan el umbral (última hora) ---")
    lecturas_sobre_umbral()
