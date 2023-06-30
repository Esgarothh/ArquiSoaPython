import socket
import psycopg2
from decimal import Decimal

try:
    conn = psycopg2.connect(user="postgres", password="benjads1", database="mydatabase", host="localhost", port="5432")
    print("Conectado a la db")
    cur = conn.cursor()
except:
    print("error")

# Define the server's address and port
server_address = ('localhost', 5000)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    sock.connect(server_address)
    print('Connected to {}:{}'.format(*server_address))

    # Send a message
    message = '00010sinitrecet'
    sock.sendall(message.encode())
    print('Sent: {}'.format(message))

    # Receive the server's response
    response = sock.recv(1024).decode()
    print('Received: {}'.format(response))

    servicio = 'recet'

    # Listen for the specific response
    if response == '00012sinitOK{}'.format(servicio):

        while True:

            response = sock.recv(1024).decode()
            print('Received client response: {}'.format(response))
            longitud = int(response[:5])
            print("longitud:", longitud)

            service = response[5:10]
            len_question = longitud - 5
            question = response[11:]
            print("servicio:", service, "len:",
                  len_question, "question:", question)
            if service == servicio:

                rut = question
                cur.execute(
                    """SELECT receta_paciente, licencias_paciente FROM historiales_medicos WHERE rut_paciente = %s """,
                    [rut, ])
                res = cur.fetchall()
                if len(res) == 0:
                    frase = '00020' + 'recet' + ' ' + 'user_not_found'
                    sock.sendall(frase.encode())
                else:
                    values = []
                    arr = []
                    for row in res:
                        values.extend(row)
                    for i in range(0, len(values)):
                        arr.append(str(values[i]))
                    tamanio_mensaje = len(' '.join(arr)) + 7 + len(rut)
                    sizetosend = str(tamanio_mensaje).rjust(5, '0')
                    frase = sizetosend + 'recet' + ' ' + rut + ' ' + ' '.join(arr)
                    recetas = ', '.join(arr)
                    mensaje = "El usuario con rut: {}, tiene las siguientes recetas: \n {}".format(rut, recetas)
                    # frase = sizetosend + 'recet' + ' ' + rut + ' ' + ' '.join(arr) + mensaje
                    frase2 = sizetosend + 'recet x ' + mensaje


                    sock.sendall(frase2.encode())


finally:
    # Close the socket
    sock.close()
