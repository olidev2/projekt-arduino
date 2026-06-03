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
        for port in self.ports:
                print(f"port: {port}")
    def get_ports(self):
        return self.ports
    def has_ports(self):
        return self.any_ports
    def connect(self, port):
        if port in self.ports:
            try:
                self.connection = serial.Serial(port, 9600)
                time.sleep(2)  # czekam na stabilizacje polaczenia z arduino
                self.connection.write(b'W') # wysylamy sygnal testowy do arduino, 'W' trzeba w arduino odczytac i napisac instrukcje interpretacji tego za pomoca wbudowanego leda
                print("Wysłano sygnał testowy 'W' do Arduino!")
                print(f"Połączono z {port}")
            except serial.SerialException as e:
                print(f"Błąd połączenia: {e}")
        else:
            print(f"Port {port} nie jest dostępny")
    def getconnection(self):
        return self.connection
    def disconnect(self):
        if self.connection is not None and self.connection.is_open:
            
            self.connection.close() 
            print("Backend: Port został zamknięty i jest znowu wolny.")
            
        self.connection = None