import socket
import psycopg2
from dbb import BaseDeDatos
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
    message = '00010sinitexamr'
    sock.sendall(message.encode())
    print('Sent: {}'.format(message))

    # Receive the server's response
    response = sock.recv(1024).decode()
    print('Received: {}'.format(response))

    servicio = 'examr'
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
                rut_paciente = question.split()[0]
                rut_medico = question.split()[1]
                examen = question.split()[2]
                print(rut_paciente)
                print(rut_medico)
                print(examen)
                cur.execute("select pacientes.id from pacientes, usuarios where usuarios.id = pacientes.usuario_id and usuarios.rut =  %s", [rut_paciente,])
                pac_id = cur.fetchall()
                cur.execute("select medicos.id from medicos, usuarios where usuarios.id = medicos.usuario_id and usuarios.rut =  %s", [rut_medico,])
                med_id = cur.fetchall()
                pac_id = str(pac_id[0])[1:-1].replace(",", "")
                med_id = str(med_id[0])[1:-1].replace(",", "")
                cur.execute("""insert into solicitudes_examenes(medico_id, paciente_id, examen_id) values(%s, %s, %s) """, [med_id, pac_id, examen,])
                conn.commit()
                tamanio_mensaje = 18 + len(rut_paciente)
                sizetosend = str(tamanio_mensaje).rjust(5, '0')
                frase = sizetosend + 'examr' + ' ' + rut_paciente + ' ' +  'solicitud_creada'
                sock.sendall(frase.encode())
               

finally:
    # Close the socket
    sock.close()
