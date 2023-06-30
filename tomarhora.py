import socket
import psycopg2

try:
    conn = psycopg2.connect(user="postgres", password="xxxx", database="mydatabase", host="localhost", port="5432")
    print("Conectado a la base de datos")
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)

# Define the server's address and port
server_address = ('localhost', 5000)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    sock.connect(server_address)
    print('Connected to {}:{}'.format(*server_address))

    # Send a message
    message = '00012sinitbooking'
    sock.sendall(message.encode())
    print('Sent: {}'.format(message))

    # Receive the server's response
    response = sock.recv(1024).decode()
    print('Received: {}'.format(response))

    servicio = 'booking'

    # Listen for the specific response
    if response == '00012sinitOK{}'.format(servicio):
        while True:
            response = sock.recv(1024).decode()
            print('Received client response: {}'.format(response))
            length = int(response[:5])
            service = response[5:10]
            question = response[11:]
            print("service:", service, "length:", length, "question:", question)
            if service == servicio:
                if question == 'rut':
                    # El usuario ha ingresado su RUT, obtener las horas disponibles
                    rut = input("Ingrese su RUT: ")
                    cur.execute("SELECT hour FROM availability WHERE reserved = FALSE")
                    available_hours = cur.fetchall()
                    if len(available_hours) == 0:
                        message = 'No hay horas disponibles.'
                    else:
                        message = "Horas disponibles:\n"
                        for hour in available_hours:
                            message += hour[0] + "\n"

                    # Construye y envía la respuesta al cliente
                    response_message = "{:05d}{}{}".format(len(message), servicio, message)
                    sock.sendall(response_message.encode())

                elif question.startswith('hora'):
                    # El usuario ha seleccionado una hora, actualizar el estado de reserva
                    selected_hour = question.split()[1]
                    cur.execute("UPDATE availability SET reserved = TRUE WHERE hour = %s", [selected_hour])
                    conn.commit()
                    message = "¡Hora reservada con éxito!"

                    # Construye y envía la respuesta al cliente
                    response_message = "{:05d}{}{}".format(len(message), servicio, message)
                    sock.sendall(response_message.encode())

finally:
    # Close the socket
    sock.close()
    # Close the database connection
    if conn is not None:
        conn.close()
