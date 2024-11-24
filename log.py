import machine
import time

class Log:
    LOG_DISABLE = "DISABLE"
    LOG_MSG = "MESSAGE"
    LOG_CTRL_TAB = "TABULATED"
    LOG_CTRL_ARDUINO_PLOTTER = "ARDUINO_PLOTTER"

    def __init__(self, uart_num, baudrate, tx_pin, rx_pin):
        """Inicializa la UART y configura el nivel de log."""
        self.uart = machine.UART(uart_num, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
        self.uart.init(bits=8, parity=None, stop=1)
        self.level = self.LOG_MSG  # Nivel por defecto
        self.header_written = False  # Bandera para escribir encabezado

    def set_level(self, level):
        """Configura el nivel del log."""
        self.level = level
        self.header_written = False  # Reinicia el estado del encabezado

    def msg(self, fmt, *args):
        """Muestra mensajes de log."""
        if self.level == self.LOG_MSG:
            message = fmt.format(*args)
            self.uart.write(f"{int(time.ticks_ms())} {message}\n")

    def msg_ctrl(self, message):
        """Envía información de control por UART."""
        self.uart.write(f"{message}\n")

    def ctrl(self, raw, filtered, state, danger_point):
        """Loguea información de control en formato adecuado."""
        if self.level == self.LOG_CTRL_TAB:
            # Salida tabulada
            log_message = "{}\t{}\t{}\t{}\t{}".format(
                int(time.ticks_ms()), raw, filtered, state, danger_point
            )
            self.msg_ctrl(log_message)
        elif self.level == self.LOG_CTRL_ARDUINO_PLOTTER:
            # Salida para Arduino Plotter
            scaled_state = min(max(int(state * 1000 / 3), 0), 5000)  # Escala de estado
            plot_message = "raw:{}, filtered:{}, state:{}, danger:{}".format(
                raw, filtered, scaled_state, danger_point
            )
            self.msg_ctrl(plot_message)

