import uasyncio as asyncio
from wifi import connect_wifi
from server import start_server_with_config
from led import Led  # Clase para manejar el LED
from config import Config  # Clase para manejar la configuración
from log import Log  # Clase del logger

# Definición de los estados de la máquina de estados simulando enum
class State:
    ST_LOOP_INIT = 0
    ST_LOOP_IDLE = 1
    ST_LOOP_LED_ON = 2
    ST_LOOP_LED_OFF = 3
    ST_LOOP_END = 4
    ST_MODE_RUN_DEMO1 = 5  # Modo adicional

async def run_demo_serial_plotter(logger, led):
    """Simulación del modo demo que imprime valores al logger."""
    print("Ejecutando demo serial plotter...")
    logger.msg("Iniciando demo serial plotter")
    danger_point = 2500

    for raw in range(5000):
        filtered = raw + 500
        state = 1 if filtered > danger_point else 0
        logger.ctrl(raw, filtered, state, danger_point)    
    

async def led_blink_loop(led, config):
    """Máquina de estados para controlar el parpadeo del LED."""
    st_loop = State.ST_LOOP_INIT
    led_blink_qty = 0  # Cantidad de parpadeos
    logger = Log(uart_num=1, baudrate=115200, tx_pin=17, rx_pin=18)
    await asyncio.sleep(0.1)  # Espera breve para inicializar UART

    while True:
        if st_loop == State.ST_LOOP_INIT:
            if config.st_test:
                led_blink_qty = config.led_blink_quantity
                blink_time = config.led_blink_time
                led_color = config.led_color
                led.set_color(led_color)
                logger.set_level(config.log_level)
                st_loop = State.ST_LOOP_IDLE
            elif config.st_mode == "DEMO":
                st_loop = State.ST_MODE_RUN_DEMO1
                logger.set_level(config.log_level)
            else:
                await asyncio.sleep(0.1)

        elif st_loop == State.ST_LOOP_IDLE:
            logger.msg(f"Preparado para parpadear {led_blink_qty} veces con {blink_time} ms.")
            st_loop = State.ST_LOOP_LED_ON

        elif st_loop == State.ST_LOOP_LED_ON:
            logger.msg("LED encendido")
            led.on()
            await asyncio.sleep(blink_time / 1000.0)
            st_loop = State.ST_LOOP_LED_OFF

        elif st_loop == State.ST_LOOP_LED_OFF:
            logger.msg("LED apagado")
            led.off()
            await asyncio.sleep(blink_time / 1000.0)
            led_blink_qty -= 1
            st_loop = State.ST_LOOP_LED_ON if led_blink_qty > 0 else State.ST_LOOP_END

        elif st_loop == State.ST_LOOP_END:
            logger.msg("Ensayo terminado")
            config.update_config("st_test", False)
            st_loop = State.ST_LOOP_INIT

        elif st_loop == State.ST_MODE_RUN_DEMO1:
            await run_demo_serial_plotter(logger, led)
            config.update_config("st_mode", "OFF")  # Cambiar el modo si es necesario
            st_loop = State.ST_LOOP_INIT

        await asyncio.sleep(0.1)

async def main():
    # Conectar a Wi-Fi
    connect_wifi()

    # Crear instancia de configuración
    config = Config()
    config.initialize_config()

    # Iniciar el servidor en una tarea asíncrona
    asyncio.create_task(start_server_with_config(config))

    # Crear instancia del LED
    led = Led(pin_number=48, num_leds=1)

    # Iniciar la máquina de estados
    await led_blink_loop(led, config)

if __name__ == "__main__":
    try:
        print("Iniciando sistema...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")
