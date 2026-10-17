# TA3 - Grupo 3 (Sector Minero) - Instalación sin Docker

Arquitectura: `simulador_IoT.py` → EMQX → `mqtt_to_influx.py` → InfluxDB → Grafana.

## 1. Python

```bash
pip install -r requirements.txt
```

## 2. EMQX (broker MQTT)

1. Descargar el paquete .zip de EMQX para Windows: https://www.emqx.io/downloads?os=Windows
2. Extraer en una carpeta, por ejemplo `C:\emqx`.
3. Abrir PowerShell en esa carpeta y ejecutar:
   ```
   .\bin\emqx.cmd start
   ```
4. Verificar en http://localhost:18083 (usuario `admin`, contraseña `public`).
5. Para detenerlo: `.\bin\emqx.cmd stop`.

## 3. InfluxDB

1. Descargar InfluxDB OSS 2.x para Windows: https://www.influxdata.com/downloads/
2. Extraer y ejecutar `influxd.exe`.
3. Ir a http://localhost:8086 y completar el setup inicial: organización (`ta3-minero`), bucket (`gabinete_electrico`), usuario y contraseña.
4. Generar un API Token (Load Data → API Tokens → Generate Token, con permisos de lectura/escritura sobre el bucket).
5. En `mqtt_to_influx.py`, definir las variables de entorno antes de ejecutar (o reemplazar los valores por defecto en el archivo):
   ```
   $env:INFLUX_TOKEN="tu_token_generado"
   ```

## 4. Grafana

1. Descargar el instalador de Grafana OSS para Windows: https://grafana.com/grafana/download?platform=windows
2. Instalar y ejecutar el servicio (o `grafana-server.exe` si usaste el .zip).
3. Ir a http://localhost:3000 (usuario/contraseña por defecto `admin`/`admin`).
4. Agregar datasource: Connections → Data sources → Add → InfluxDB.
   - Query language: Flux
   - URL: `http://localhost:8086`
   - Organization: `ta3-minero`
   - Token: el generado en el paso 3
   - Default bucket: `gabinete_electrico`
5. Importar el dashboard: Dashboards → New → Import → subir `grafana/dashboard_gabinete_electrico.json` → seleccionar el datasource InfluxDB creado.

## 5. Ejecutar el flujo completo

En dos terminales distintas (con EMQX, InfluxDB y Grafana ya corriendo):

```bash
python simulador_IoT.py
```

```bash
python mqtt_to_influx.py
```

## 6. Verificación con MQTT Explorer

1. Conectar a `localhost:1883`.
2. Suscribirse a `iot/minera/gabinete_electrico/temperatura`.
3. Confirmar que los valores publicados coinciden con los que aparecen en InfluxDB/Grafana.

## Pruebas de la rúbrica

- **Lectura normal**: consola de `simulador_IoT.py` mostrando temperaturas.
- **Transmisión y recepción**: MQTT Explorer recibiendo los mensajes.
- **Almacenamiento**: Data Explorer de InfluxDB (http://localhost:8086) mostrando los puntos del bucket `gabinete_electrico`.
- **Visualización**: dashboard de Grafana con los paneles de última temperatura y evolución.
- **Umbral superado**: esperar a que `simulador_IoT.py` genere un pico (>45°C, ~15% de probabilidad en cada lectura) y mostrar la alerta en consola + el punto en rojo en Grafana.
- **Interrupción de comunicación**: detener `simulador_IoT.py` y mostrar que Grafana deja de recibir datos nuevos (el panel de evolución se aplana).
