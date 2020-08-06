
from time import time, sleep
import os
import threading
import serial



PREFIJOS_VALIDOS = ["USB", "ACM"]

def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    import glob
    # asumimos que la plataforma es linux
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
    # quitar AMA0 que es el GPIO de la RPi
    if '/dev/ttyAMA0' in ports:
        ports.remove('/dev/ttyAMA0')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# SERIE_PUERTO = serial_ports()[0] #"/dev/ttyUSB0" # "/dev/ttyACM0"
puertos_disponibles = serial_ports()
if not puertos_disponibles:
    print("ERROR no se encontro ningun puerto valido ")
    quit(1)
SERIE_PUERTO = puertos_disponibles[0] 
SERIE_BAUDRATE = 115200  # 19200  #57600  #




def escuchar_redis():
    #global grabando, test_filename_full, test_ciclos
     # while getattr(t, "seguir", True):
    while self.running:
        sleep(0.2)
  


class BridgeSerial:
    def __init__(self):
        self.running = True
        self.lock = threading.Lock()
        self.sample_rate = 0.05
        self.cb = self.print_msg
    
    def callback(self, cb):
        self.cb = cb

    def connect(self):
        try:
            self.ser = serial.Serial(SERIE_PUERTO, SERIE_BAUDRATE, timeout=0.5)
        except:
            print("ERROR no se pudo abrir el puerto {}".format(SERIE_PUERTO))
            self.running = False
            return
        print("Escuchando puerto {}".format(SERIE_PUERTO))
        while self.ser.inWaiting() > 0:
            _ = self.ser.read()  # vacia buffer
        self.th_main = threading.Thread(target=self.main)
        self.th_main.start()

    def wait(self):
        while self.running:
            if not self.th_main.isAlive():
                break
            sleep(1)

    def stop(self):
        with self.lock:
            self.running = False
        print("deteniendo...")
        if self.th_main.isAlive():
            self.th_main.join()
        self.ser.close()
        print("detenido")

    def print_msg(self, msg):
        print(msg, end='')

    def main(self):
        while self.running:
            sleep(self.sample_rate)
            hay_datos_serie = 0
            try:
                hay_datos_serie = self.ser.inWaiting()
            except:  # OSError: [Errno 5] Input/output error
                continue
            if hay_datos_serie > 0:
                response = self.ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
                # print("dato: ", response.decode('utf-8').strip())
                try:
                    response = response.decode('utf-8')
                except:
                    print("ERROR no se pudo decodificar mensaje ¿baudrate correcto?")
                    continue
                self.cb(response)  # dispara el callback con el mensaje


if __name__ == '__main__':
    bridge_serial = BridgeSerial()
    bridge_serial.connect()
    try:
        bridge_serial.wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    bridge_serial.stop()
