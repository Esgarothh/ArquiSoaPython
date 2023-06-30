import socket
import psycopg2

def register(rut, password, role, email, phone, first_name, last_name):
    try:
        conn = psycopg2.connect(user="tu_usuario", password="tu_contraseña", host="localhost", port="5432", database="tu_basededatos")
        print("Conectado a la base de datos")
        cur = conn.cursor()

        # Verificar si el usuario ya existe en la base de datos
        cur.execute("SELECT rut FROM usuarios WHERE rut = %s", (rut,))
        result = cur.fetchone()
        if result is not None:
            return "El usuario ya existe"

        # Insertar el nuevo usuario en la base de datos
        cur.execute("INSERT INTO usuarios (rut, password, role, email, phone, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (rut, password, role, email, phone, first_name, last_name))
        conn.commit()

        return "Registro exitoso"
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return "Error al conectar a la base de datos"

def run_server():
    # Define the server's address and port
    server_address = ('localhost', 5000)

    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the server address
        sock.bind(server_address)
        print('Servidor iniciado en {}:{}'.format(*server_address))

        # Listen for incoming connections
        sock.listen(1)

        while True:
            print('Esperando conexión...')
            connection, client_address = sock.accept()
            print('Conexión establecida desde', client_address)

            # Receive the client's request
            request = connection.recv(1024).decode()
            print('Received: {}'.format(request))

            if request.startswith('register'):
                parameters = request.split(',')
                if len(parameters) == 7:
                    rut = parameters[1]
                    password = parameters[2]
                    role = parameters[3]
                    email = parameters[4]
                    phone = parameters[5]
                    first_name = parameters[6]
                    last_name = parameters[7]
                    print('rut:', rut)
                    print('password:', password)
                    print('role:', role)
                    print('email:', email)
                    print('phone:', phone)
                    print('first_name:', first_name)
                    print('last_name:', last_name)

                    # Perform registration
                    response = register(rut, password, role, email, phone, first_name, last_name)
                    print('Response:', response)

                    # Send the response back to the client
                    connection.sendall(response.encode())
                else:
                    connection.sendall("Parámetros incorrectos".encode())

            # Close the connection
            connection.close()
    except socket.error as e:
        print("Error en el servidor:", e)
    finally:
        # Close the socket
        sock.close()
