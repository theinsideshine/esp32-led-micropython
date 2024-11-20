import machine
import neopixel
import uasyncio as asyncio

class Led:
    COLORS = {
        "ROJO": (255, 0, 0),
        "AMARILLO": (255, 255, 0),
        "VERDE": (0, 255, 0),
        "BLANCO": (255, 255, 255),
        "AZUL": (0, 0, 255),
        "CIAN": (0, 255, 255),
        "MAGENTA": (255, 0, 255),
        "NARANJA": (255, 165, 0),
        "VIOLETA": (238, 130, 238),
        "GRIS": (169, 169, 169),
        "NEGRO": (0, 0, 0),  # Apagado
    }

    def __init__(self, pin_number, num_leds=1):
        """Inicializa los LEDs WS2812 en un pin y número de LEDs especificados."""
        self.pin = machine.Pin(pin_number, machine.Pin.OUT)
        self.num_leds = num_leds
        self.leds = neopixel.NeoPixel(self.pin, self.num_leds)
        self.current_color = (255, 255, 255)  # Color por defecto
        self.off()

    def on(self):
        """Enciende los LEDs con el último color establecido."""
        for i in range(self.num_leds):
            self.leds[i] = self.current_color  # Usa el color actual
        self.leds.write()  # Aplica el color

    def off(self):
        """Apaga los LEDs."""
        for i in range(self.num_leds):
            self.leds[i] = (0, 0, 0)  # Apaga el LED (RGB: 0, 0, 0)
        self.leds.write()  # Aplica el apagado

    def set_color(self, color):
        """Establece el color para el LED.
        
        Si el color es un nombre predefinido ('ROJO', 'AMARILLO', etc.), se usa el color asociado.
        De lo contrario, se espera que sea una tupla RGB.
        """
        if isinstance(color, str) and color.upper() in self.COLORS:
            self.current_color = self.COLORS[color.upper()]
        elif isinstance(color, tuple) and len(color) == 3:
            self.current_color = color
        else:
            raise ValueError("Color inválido. Use un nombre predefinido o una tupla RGB (r, g, b).")

    async def blink(self, t_blink):
        """Hace parpadear los LEDs con un intervalo determinado (ms) usando el último color."""
        while True:
            self.on()  # Enciende los LEDs con el color actual
            await asyncio.sleep(t_blink / 1000.0)  # Espera el tiempo especificado
            self.off()  # Apaga los LEDs
            await asyncio.sleep(t_blink / 1000.0)  # Espera el tiempo especificado



