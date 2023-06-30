import socket
import psycopg2
from decimal import Decimal

try:
    conn = psycopg2.connect(user="sjpzdvmw", password="d5QoAfziB_lNBjSxGl_UC5cxPs1PM3LY",  host="silly.db.elephantsql.com", port="5432")
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
    message = '00010sinitexamv'
    sock.sendall(message.encode())
    print('Sent: {}'.format(message))

    # Receive the server's response
    response = sock.recv(1024).decode()
    print('Received: {}'.format(response))

    servicio = 'examv'
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
                rut_exam = question.rsplit(' ', 1)[0]
                print(rut_exam)
                cur.execute("""SELECT paciente_id, examenes.nombre, fecha, detalle FROM resultados_examenes, examenes, usuarios, pacientes WHERE usuarios.id = pacientes.usuario_id and pacientes.id = resultados_examenes.paciente_id and resultados_examenes.examen_id = examenes.id and usuarios.rut = %s """, [rut_exam,]) 
                res = cur.fetchall()
                if len(res) == 0:
                    tamanio_mensaje= 21 + len(rut_exam)
                    sizetosend = str(tamanio_mensaje).rjust(5, '0')
                    frase = sizetosend + 'examv' + ' ' + rut_exam + ' ' +  'exam_not_found'
                    print(frase)
                    sock.sendall(frase.encode())
                else:
                    values = []
                    arr =[]
                    for row in res:
                        values.extend(row)
                    print(len(values))
                    for i in range(0,len(values)):
                        arr.append('"'+ str(values[i])+ '"')
                    tamanio_mensaje= len(' '.join(arr)) + 7 + len(rut_exam)
                    sizetosend = str(tamanio_mensaje).rjust(5, '0')
                    frase = sizetosend + 'examv' + ' ' + rut_exam + ' '  + ' '.join(arr)
                    print(frase)
                    sock.sendall(frase.encode())

finally:
    # Close the socket
    sock.close()
