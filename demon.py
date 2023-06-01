import socket

# Define the server's address and port
server_address = ('localhost', 5000)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    sock.connect(server_address)
    print('Connected to {}:{}'.format(*server_address))

    # Send a message
    message = '00010sinitdemon'
    sock.sendall(message.encode())
    print('Sent: {}'.format(message))

    # Receive the server's response
    response = sock.recv(1024).decode()
    print('Received: {}'.format(response))

    servicio = 'demon'
    # Listen for the specific response
    if response == '00012sinitOK{}'.format(servicio):
        while True:
            response = sock.recv(1024).decode()
            print('Received client response: {}'.format(response))
            longitud = int(response[:5])
            print("longitud:", longitud)
            service = response[5:10]
            len_question = longitud-5
            question = response[11:]
            print("servicio:", service, "len:",
                  len_question, "question:", question)
            if service == servicio:
                print('hre')
                variables = question.split(' ')
                a = variables[0]
                b = variables[1]
                res = int(a)+int(b)
                espacios = 5
                symbols = 2  # + , =
                len_enviar = espacios+len(a)+len(b)+symbols + len(str(res))
                ceros = 5-len(str(len_enviar))
                frase = '0'*ceros+str(len_enviar) + servicio + \
                    "{} + {} = {}".format(a, b, res)
                result = '00017sumar 2 + 3 = 5'
                sock.sendall(frase.encode())


finally:
    # Close the socket
    sock.close()
