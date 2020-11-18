from time import sleep
import threading
import serial
import glob
import sys


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        # remove AMA0 (Raspberry Pi GPIO)
        if '/dev/ttyAMA0' in ports:
            ports.remove('/dev/ttyAMA0')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class BridgeSerial:
    def __init__(self):
        self.running = True
        self.lock = threading.Lock()
        self.sample_rate = 0.02
        self.cb = self._print_msg
        self.ser = None
        self.th_main = None

    def set_callback(self, cb):
        self.cb = cb

    def connect(self, port=None, baudrate=57600, verbose=False):
        self.verbose = verbose
        if port is None:
            puertos_disponibles = serial_ports()
            if not puertos_disponibles:
                print("ERROR no ports found. Use -p to specify a port")
                quit(1)
            port = puertos_disponibles[0]
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.5)
        except Exception as e:
            print("ERROR couln't open port {}".format(port))
            self.running = False
            return
        print("Listen port {} at {} bauds".format(port, baudrate))
        while self.ser.inWaiting() > 0:
            _ = self.ser.read()  # vacia buffer
        self.th_main = threading.Thread(target=self.main)
        self.th_main.start()

    def write(self, msg):
        if self.verbose:
            if type(msg) is str:
                print("   <== " + msg.strip())
            else:
                print("   <== " + msg.decode().strip())
        if type(msg) is str:
            msg = msg.encode()
        # TODO en modo json mejor no enviar fin de linea
        # if msg[-1] != b'\n':
        #     msg+=b'\n'
        self.ser.write(msg)

    def wait(self):
        while self.running:
            if not self.th_main.is_alive():
                break
            sleep(1)

    def stop(self):
        with self.lock:
            self.running = False
        print("stopping...")
        if self.th_main.is_alive():
            self.th_main.join()
        self.ser.close()
        print("stopped")

    def main(self):
        while self.running:
            sleep(self.sample_rate)
            try:
                hay_datos_serie = self.ser.inWaiting()
            except OSError:  # OSError: [Errno 5] Input/output error
                continue
            if hay_datos_serie > 0:
                response = self.ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
                # print("dato: ", response.decode('utf-8').strip())
                try:
                    response = response.decode('utf-8')
                except UnicodeDecodeError:
                    print("ERROR couldn't decode message. Check baudrate")
                    continue
                if self.verbose:
                    print("==>    " + response.strip())
                self.cb(response)  # dispara el callback con el mensaje

    @staticmethod
    def _print_msg(msg):
        print(msg, end='')


if __name__ == '__main__':
    bridge_serial = BridgeSerial()
    bridge_serial.connect()
    try:
        bridge_serial.wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    bridge_serial.stop()
