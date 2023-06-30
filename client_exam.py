import socket

# Define the server's address and port
server_address = ('localhost', 5000)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    sock.connect(server_address)
    #print('Conectado a {}:{}'.format(*server_address))

    while True:
        # Read message from keyboard input
        print("view : Ver examenes; requ: Crear solicitud ")
        opt = input("Ingresar opcion: ").split("\n")[0]
        if opt == "view":
            rut = input("Ingresar rut: ").split("\n")[0]
            tamanio_mensaje = len(rut) + 7
            sizetosend = str(tamanio_mensaje).rjust(5, '0')
            frase = sizetosend + 'examv' + ' ' + rut
            print(frase)
        elif opt == "requ":
            rutpac = input("Ingresar rut paciente: ").split("\n")[0]
            rutmed = input("Ingresar rut médico: ").split("\n")[0]
            examreq = input("Ingresar examen: ").split("\n")[0]
            tamanio_mensaje = len(rutpac) + len(rutmed) + len(examreq) + 9
            sizetosend = str(tamanio_mensaje).rjust(5, '0')
            frase = sizetosend + 'examr' +  ' ' + rutpac + ' ' + rutmed + ' ' + examreq
            print(frase)
        # Send the message
        sock.sendall(frase.encode())
        
        print('Sent: {}'.format(frase))

        # Receive the server's response
        response = sock.recv(1024).decode()
        print('Respuesta: {}'.format(response[13:]))


finally:
    # Close the socket
    #sock.close()
    print("")
