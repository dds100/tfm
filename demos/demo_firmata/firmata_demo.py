from pyfirmata import Arduino, util
import time

# Reemplaza por el puerto real de tu Arduino (ej: COM3 en Windows o /dev/ttyACM0 en Linux)
puerto = 'COM3'  # O '/dev/ttyACM0' en Linux
# puerto = '/dev/ttyACM0' # en Linux
placa = Arduino(puerto)
led_pin = 13
# read_pin = 'A0'


# Inicia el iterador
it = util.Iterator(placa)
it.start()

placa.analog[0].enable_reporting()


# Blink del LED en pin 13
print("Iniciando parpadeo en pin 13")
while True:
    placa.digital[led_pin].write(1)  # Encender
    time.sleep(1)
    placa.digital[led_pin].write(0)  # Apagar
    time.sleep(1)
    lectura = placa.analog[0].read()
    print(f'Tensión = {5*lectura:.2f} V')

