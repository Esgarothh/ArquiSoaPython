import socket
import psycopg2

def login(rut, password):
    try:
        conn = psycopg2.connect(user="sjpzdvmw", password="d5QoAfziB_lNBjSxGl_UC5cxPs1PM3LY", host="silly.db.elephantsql.com", port="5432")
        print("Conectado a la base de datos")
        cur = conn.cursor()

        cur.execute("SELECT rut FROM usuarios WHERE rut = %s AND password = %s", (rut, password))
        result = cur.fetchone()

        if result is not None:
            return "Inicio de sesión exitoso"
        else:
            return "Credenciales inválidas"
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

            if len(request) == 22 and request.startswith('00016login'):
                rut = request[16:22]
                password = request[22:]
                print('rut:', rut)
                print('password:', password)

                # Perform login
                response = login(rut, password)
                print('Response:', response)

                # Send the response back to the client
                connection.sendall(response.encode())

            # Close the connection
            connection.close()
    except socket.error as e:
        print("Error en el servidor:", e)
    finally:
        # Close the socket
        sock.close()


if __name__ == '__main__':
    run_server()