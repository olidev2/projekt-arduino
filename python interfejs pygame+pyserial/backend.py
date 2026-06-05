import serial.tools.list_ports
import time

class Backend:
    def __init__(self):
        self.connection = None
        self.ports = []
        self.any_ports = False
        self.update_ports()

    def update_ports(self):
        self.ports = [ports.device for ports in serial.tools.list_ports.comports()]
        if self.ports:
            self.any_ports = True

    def get_ports(self):
        return self.ports

    def has_ports(self):
        return self.any_ports

    def connect(self, port):
        if port in self.ports:
            try:
                self.connection = serial.Serial(port, 9600, timeout=1)
                print(f"Backend: Połączono z {port}. Usypiam na 2s dla resetu Arduino...")
                time.sleep(2)
                return True
            except serial.SerialException as e:
                print(f"Backend: Błąd połączenia: {e}")
                self.connection = None
                return False
        else:
            print(f"Backend: Port {port} nie jest dostępny")
            return False

    def getconnection(self):
        return self.connection

    def disconnect(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close() 
            print("Backend: Port został zamknięty i jest znowu wolny.")
        self.connection = None

    def wyslij_komende(self, komenda):
        if self.connection is not None and self.connection.is_open:
            try:
                self.connection.write(komenda.encode())
            except Exception as e:
                print(f"Backend: Błąd wysyłania komendy: {e}")