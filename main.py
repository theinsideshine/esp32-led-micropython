import uasyncio as asyncio
from wifi import connect_wifi
from server import start_server_with_config
from led import Led  # Importar la clase Led
from config import Config  # Importar la clase Config

# Definir estados
IDLE = 0
BLINKING = 1

async def blink_led(led, config):
    """Controla el parpadeo del LED alternando entre estados IDLE y BLINKING."""
    state = IDLE  # Estado inicial

    while True:
        if state == IDLE:
                        
            # Verificar si `st_test` está en True
            if config.st_test:
                print("st_test es True. Cambiando a estado BLINKING.")
                state = BLINKING
            else:
                # Esperar brevemente antes de revisar de nuevo
                await asyncio.sleep(0.1)

        elif state == BLINKING:
            print("Estado: BLINKING. Iniciando parpadeo.")
            # Leer configuración de parpadeo
            blink_time = config.led_blink_time
            blink_quantity = config.led_blink_quantity
            
            for _ in range(blink_quantity):
                print("LED ENCENDIDO")
                led.on(color=(0, 255, 0))  # Encender LED en verde
                await asyncio.sleep(blink_time / 1000.0)

                print("LED APAGADO")
                led.off()  # Apagar LED
                await asyncio.sleep(blink_time / 1000.0)

            # Reiniciar `st_test` y volver al estado IDLE
            print("Parpadeo completado. Regresando al estado IDLE.")
            config.update_config("st_test", False)
            await asyncio.sleep(0.1)  # Breve pausa para asegurar la actualización
            print(f"Antes de recargar: st_test = {config.st_test}")
            config.reload_config()
            print(f"Después de recargar: st_test = {config.st_test}")
            state = IDLE

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
        print("Iniciando.")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")








       