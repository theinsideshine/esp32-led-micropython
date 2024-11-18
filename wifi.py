# wifi.py
import network
import uasyncio as asyncio

SSID = 'Pablo'
PASSWORD = '01410398716'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # Activar la interfaz Wi-Fi

    if not wlan.isconnected():
        print(f"Conectando a la red {SSID}...")
        wlan.connect(SSID, PASSWORD)
        
        # Esperar hasta que se establezca la conexión o se alcance el tiempo máximo
        intentos = 0
        while not wlan.isconnected() and intentos < 10:
            print(f"Esperando conexión... Intento {intentos + 1}")
            asyncio.sleep(1)  # Pausa de 1 segundo entre intentos
            intentos += 1

    # Mostrar el estado final de la conexión
    if wlan.isconnected():
        print(f"Conexión Wi-Fi establecida con IP: {wlan.ifconfig()[0]}")
    else:
        print("Error: No se pudo conectar a la red Wi-Fi después de varios intentos.")
