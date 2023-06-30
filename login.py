import socket
import threading
from dbb import BaseDeDatos

class LoginService:
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
        # En este ejemplo, asumiremos que la solicitud es un intento de inicio de sesión
        credentials = payload.split()
        if len(credentials) != 2:
            return "Invalid request"

        username = credentials[0]
        password = credentials[1]

        self.conectarbase()
        user_data = self.database.get_user_by_username(username)

        if user_data is None:
            return "User not found"

        stored_password = user_data.get('password')

        if stored_password == password:
            return "Login successful"
        else:
            return "Invalid password"

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
service_name = "login"

service = LoginService(bus_host, bus_port, service_name)
service.initialize()

# Mantén el servicio en ejecución (por ejemplo, con un loop infinito)
while True:
    pass
