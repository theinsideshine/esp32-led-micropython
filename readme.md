ESP32 Web-Controlled LED Blink Project Project Overview This project demonstrates a modular architecture for the ESP32 using microPython,
 designed to support complex, non-blocking control systems. 
The system provides web-based control, data persistence, and serial output, compatible with JSON, text

quedo andado la el comienzo y el fin del ensayo con st_test
todo  cambiar  al nueva st

tener en cuenta que en el siguiente codifo le falta el update_confifg para st, que esta en la maquina por cambiar 


import uasyncio as asyncio
from wifi import connect_wifi
from server import start_server_with_config
from led import Led  # Importar la clase Led
from config import Config  # Importar la clase Config

# Estados de la máquina de estados para el parpadeo
ST_LOOP_INIT = 0
ST_LOOP_IDLE = 1
ST_LOOP_LED_ON = 2
ST_LOOP_LED_OFF = 3
ST_LOOP_END = 4

async def led_blink_loop(led, config):
    """Máquina de estados para controlar el parpadeo del LED."""
    st_loop = ST_LOOP_INIT
    led_blink_qty = 0  # Inicialización fuera del bucle

    while True:
        if st_loop == ST_LOOP_INIT:
            print("Estado: Inicializando...")
            # Verificar si `st_test` está activo
            if config.st_test:
                led_blink_qty = config.led_blink_quantity
                blink_time = config.led_blink_time
                st_loop = ST_LOOP_IDLE
            else:
                # Esperar brevemente antes de revisar de nuevo
                await asyncio.sleep(0.1)

        elif st_loop == ST_LOOP_IDLE:
            print(f"Estado: Preparado para parpadear {led_blink_qty} veces.")
            st_loop = ST_LOOP_LED_ON

        elif st_loop == ST_LOOP_LED_ON:
            print("Estado: LED ON")
            led.on(color=(0, 255, 0))  # Encender LED en verde
            await asyncio.sleep(blink_time / 1000.0)  # Convertir milisegundos a segundos
            st_loop = ST_LOOP_LED_OFF

        elif st_loop == ST_LOOP_LED_OFF:
            print("Estado: LED OFF")
            led.off()  # Apagar LED
            await asyncio.sleep(blink_time / 1000.0)
            led_blink_qty -= 1  # Reducir la cantidad de parpadeos restantes
            if led_blink_qty > 0:
                st_loop = ST_LOOP_LED_ON
            else:
                st_loop = ST_LOOP_END

        elif st_loop == ST_LOOP_END:
            print("Estado: Parpadeo completado. Regresando al estado inicial.")
            config.st_test = False  # Reiniciar `st_test`
            st_loop = ST_LOOP_INIT

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
    
    # Iniciar la máquina de estados del LED
    await led_blink_loop(led, config)

# Ejecutar el script
if __name__ == "__main__":
    try:
        print("Iniciando.")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")
