import uasyncio as asyncio
from wifi import connect_wifi
from server import start_server_with_config
from led import Led  # Importar la clase Led
from config import Config  # Importar la clase Config



async def blink_led(led, config):
    """Controla el parpadeo del LED alternando entre estados ON y OFF."""
    state = True  # Estado inicial: LED encendido
    
    while True:
        # Leer el tiempo actual del parpadeo desde la configuración
        blink_time = config.led_blink_time  # Obtener el valor actualizado de blink_time

        print(f"Parpadeando LED con tiempo: {blink_time} ms")
        
        # Controlar el estado del LED
        if state:
            print("LED ENCENDIDO")
            led.on(color=(0, 255, 0))  # Encender el LED con el color verde
        else:
            print("LED APAGADO")
            led.off()  # Apagar el LED

        # Alternar el estado
        state = not state
        
        # Pausar según el tiempo configurado
        await asyncio.sleep(blink_time / 1000.0)  # Usar el tiempo de parpadeo desde la configuración




async def main():
    # Conectar a Wi-Fi
    connect_wifi()
    
    # Crear instancia de configuración
    config = Config()
    config.initialize_config()  # Verifica y carga la configuración inicial
    
    # Iniciar el servidor en una tarea asíncrona y pasar `config`
    asyncio.create_task(start_server_with_config(config))
    
    # Crear la instancia del LED
    led = Led(pin_number=48, num_leds=1)  # Cambiar según lo necesites
    
    # Iniciar el parpadeo del LED con acceso a la configuración
    await blink_led(led, config)

# Ejecutar el script
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")







       