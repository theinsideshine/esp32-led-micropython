import json

class Config:
    MAGIC_NUMBER = 201
    LED_BLINK_TIME_DEFAULT = 1010
    LED_BLINK_QUANTITY_DEFAULT = 3
    ST_TEST_DEFAULT = 0
    ST_MODE_DEFAULT = 0
    LED_COLOR_DEFAULT = "VERDE"  # Nuevo campo por defecto
    CONFIG_FILE = "config.json"

    def __init__(self):
        self.led_blink_time = None
        self.led_blink_quantity = None
        self.st_test = None
        self.st_mode = None
        self.led_color = None  # Nuevo campo

    def initialize_config(self):
        """Verifica consistencia y carga la configuración inicial."""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if data.get("magic_number") != self.MAGIC_NUMBER:
                    print("Número mágico no coincide. Configurando valores por defecto...")
                    self.set_defaults()
                else:
                    print("Número mágico coincide. Cargando valores de configuración...")
                    self._load_values(data)
        except (OSError, ValueError):
            print("No se encontró archivo de configuración o está corrupto. Configurando valores por defecto...")
            self.set_defaults()

    def set_defaults(self):
        self.led_blink_time = self.LED_BLINK_TIME_DEFAULT
        self.led_blink_quantity = self.LED_BLINK_QUANTITY_DEFAULT
        self.st_test = self.ST_TEST_DEFAULT
        self.st_mode = self.ST_MODE_DEFAULT
        self.led_color = self.LED_COLOR_DEFAULT  # Asignar el valor por defecto
        self.save_config()
        print("Configuración por defecto establecida y guardada.")

    def save_config(self):
        data = {
            "magic_number": self.MAGIC_NUMBER,
            "led_blink_time": self.led_blink_time,
            "led_blink_quantity": self.led_blink_quantity,
            "st_test": self.st_test,
            "st_mode": self.st_mode,
            "led_color": self.led_color  # Guardar el nuevo campo
        }
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f)

    def update_config(self, key, value):
        setattr(self, key, value)
        self.save_config()

    def reload_config(self):
        """Recarga la configuración desde el archivo JSON."""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self._load_values(data)
                print("Configuración recargada.")
        except (OSError, ValueError):
            print("Error recargando configuración. Usando valores actuales.")

    def _load_values(self, data): #Para agregar campos no es necesario chequear el numero magico
        self.led_blink_time = data.get("led_blink_time", self.LED_BLINK_TIME_DEFAULT)
        self.led_blink_quantity = data.get("led_blink_quantity", self.LED_BLINK_QUANTITY_DEFAULT)
        self.st_test = data.get("st_test", self.ST_TEST_DEFAULT)
        self.st_mode = data.get("st_mode", self.ST_MODE_DEFAULT)
        self.led_color = data.get("led_color", self.LED_COLOR_DEFAULT)  # Cargar el nuevo campo

