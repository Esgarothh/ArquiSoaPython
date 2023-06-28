import socket
import threading
from dbb import BaseDeDatos


class SoAService:
    def __init__(self, bus_host, bus_port, service_name):
        self.bus_host = bus_host
        self.bus_port = bus_port
        self.service_name = service_name
        self.is_running = False
        self.database = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.bus_host, self.bus_port))

    def initialize(self):
        length = self._calculate_length()
        init_string = "{:05d}{}{}".format(length, "sinit", self.service_name)
        response = self._send_to_bus(init_string)
        print("response is", response)
        if response == '00012sinitOK{}'.format(self.service_name):
            self.start_daemon()

    def conectarbase(self):
        self.database = BaseDeDatos()
        self.database.connect()
        datatest = self.database.get_test(123)
        for row in datatest:
            print(row)
        self.database.close()

    def _calculate_length(self):
        # Implementa tu lógica para calcular el largo del payload + nombre del servicio
        # Aquí asumiremos que el payload y el nombre del servicio son estáticos
        payload = "example_payload"
        length = len(payload) + len(self.service_name)
        return length

    def _send_to_bus(self, message):
        self.sock.sendall(message.encode())
        response = self.sock.recv(1024).decode()
        return response

    def _handle_message(self, message):
        length = int(message[:5])
        expected_length = length + len(self.service_name)
        if len(message) < expected_length:
            # Esperar a recibir los caracteres restantes
            return

        print(message)
        # Procesar el mensaje completo
        payload = message[5:expected_length]
        response = self.responder_a_bus(payload)
        response_string = "{:05d}{}{}".format(
            len(response), self.service_name, response)
        self.sock.sendall(response_string.encode())

    def responder_a_bus(self, payload):
        # Implementa tu lógica para procesar la solicitud del bus y generar una respuesta
        # En este ejemplo, asumiremos que la solicitud es una suma de dos números separados por un espacio
        numbers = payload.split()[1:]
        print("respuesta de base de datos:")
        self.conectarbase()
        if len(numbers) != 2:
            print(payload)
            return "Invalid request"
        try:
            num1 = int(numbers[0])
            num2 = int(numbers[1])
            result = num1 + num2
            return str(result)
        except ValueError:
            return "Invalid numbers"

    def _listen_to_bus(self):

        while self.is_running:
            message = self.sock.recv(1024).decode()
            print("message")
            self._handle_message(message)

    def start_daemon(self):
        self.is_running = True
        thread = threading.Thread(target=self._listen_to_bus)
        thread.start()

    def stop_daemon(self):
        self.is_running = False


bus_host = "localhost"
bus_port = 5000
service_name = "demon"

service = SoAService(bus_host, bus_port, service_name)
service.initialize()

# Mantén el servicio en ejecución (por ejemplo, con un loop infinito)
while True:
    pass
