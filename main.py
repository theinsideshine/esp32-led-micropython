import uasyncio as asyncio
from wifi import connect_wifi
from server import start_server_with_config
from led import Led  # Importar la clase Led
from config import Config  # Importar la clase Config

# Definición de los estados de la máquina de estados simulando enum
class State:
    ST_LOOP_INIT = 0
    ST_LOOP_IDLE = 1
    ST_LOOP_LED_ON = 2
    ST_LOOP_LED_OFF = 3
    ST_LOOP_END = 4

async def led_blink_loop(led, config):
    """Máquina de estados para controlar el parpadeo del LED."""
    st_loop = State.ST_LOOP_INIT  # Usamos la clase `State` para el estado inicial
    led_blink_qty = 0  # Inicialización fuera del bucle

    while True:
        if st_loop == State.ST_LOOP_INIT:
            #print("Estado: Inicializando...")
            # Verificar si `st_test` está activo
            if config.st_test:
                led_blink_qty = config.led_blink_quantity
                blink_time = config.led_blink_time
                led_color = config.led_color
                led.set_color(led_color)
                st_loop = State.ST_LOOP_IDLE
            else:
                # Esperar brevemente antes de revisar de nuevo
                await asyncio.sleep(0.1)

        elif st_loop == State.ST_LOOP_IDLE:
            print(f"Preparado para parpadear {led_blink_qty} veces.")
            print(f"Preparado para parpadear un tiempo de {blink_time} ms.")
            print(f"Preparado para parpadear con un color de {led_color}.")
            st_loop = State.ST_LOOP_LED_ON

        elif st_loop == State.ST_LOOP_LED_ON:
            print("Estado: LED ON")
            led.on()  
            await asyncio.sleep(blink_time / 1000.0)  # Convertir milisegundos a segundos
            st_loop = State.ST_LOOP_LED_OFF

        elif st_loop == State.ST_LOOP_LED_OFF:
            print("Estado: LED OFF")
            led.off()  # Apagar LED
            await asyncio.sleep(blink_time / 1000.0)
            led_blink_qty -= 1  # Reducir la cantidad de parpadeos restantes
            if led_blink_qty > 0:
                st_loop = State.ST_LOOP_LED_ON
            else:
                st_loop = State.ST_LOOP_END

        elif st_loop == State.ST_LOOP_END:
            print("Estado: Parpadeo completado. Regresando al estado inicial.")            
            config.update_config("st_test", False)
            await asyncio.sleep(0.1)  # Breve pausa para asegurar la actualización            
            config.reload_config()    # Este va por si desde el servidor se hicieron cambios
            print(f"Después de recargar: st_test = {config.st_test}")            
            st_loop = State.ST_LOOP_INIT

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










       