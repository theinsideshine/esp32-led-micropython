import machine
import neopixel
import uasyncio as asyncio

class Led:
    def __init__(self, pin_number, num_leds=1):
        """Inicializa los LEDs WS2812 en un pin y número de LEDs especificados."""
        self.pin = machine.Pin(pin_number, machine.Pin.OUT)
        self.num_leds = num_leds
        self.leds = neopixel.NeoPixel(self.pin, self.num_leds)
        self.off()

    def on(self, color=(255, 255, 255)):
        """Enciende el LED con el color especificado (RGB)."""
        for i in range(self.num_leds):
            self.leds[i] = color  # Establece el color
        self.leds.write()  # Aplica el color

    def off(self):
        """Apaga los LEDs."""
        for i in range(self.num_leds):
            self.leds[i] = (0, 0, 0)  # Apaga el LED (RGB: 0, 0, 0)
        self.leds.write()  # Aplica el apagado

    async def blink(self, t_blink, color=(255, 255, 255)):
        """Hace parpadear los LEDs con un intervalo determinado (ms) y color."""
        while True:
            self.on(color)  # Enciende los LEDs con el color
            await asyncio.sleep(t_blink / 1000.0)  # Espera el tiempo especificado
            self.off()  # Apaga los LEDs
            await asyncio.sleep(t_blink / 1000.0)  # Espera el tiempo especificado

    def set_color(self, color=(255, 255, 255)):
        """Establece un color a todos los LEDs sin necesidad de encenderlos o apagarlos."""
        for i in range(self.num_leds):
            self.leds[i] = color  # Establece el color deseado
        self.leds.write()  # Aplica el color a todos los LEDs


