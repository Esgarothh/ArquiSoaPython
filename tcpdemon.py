import socket

# Local port to connect
local_port = 5000

# Connect to the local port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('200.14.84.16', local_port))

# Send and receive data
s.send(b'Hello, server!')
response = s.recv(1024)
print(response.decode())

# Close the connection
s.close()


#$ export NNTPSERVER=localhost
#$ tin -r -p 12345


import subprocess

# Local port to forward
local_port = 8888

# Remote host and port to connect through SSH tunnel
remote_host = '200.14.84.16'
remote_port = 5000

# SSH server details
ssh_username = 'sebastian.arroyo'
ssh_host = '200.14.84.16'
ssh_port = 22

# Enable ControlMaster and specify a control socket path
control_socket = f'/tmp/ssh-{ssh_username}@{ssh_host}-{ssh_port}-control'

# Establish SSH tunnel with ControlMaster
ssh_command = f'ssh -M -S {control_socket} -L {local_port}:{remote_host}:{remote_port} -p {ssh_port} {ssh_username}@{ssh_host}'
ssh_process = subprocess.Popen(ssh_command, shell=True)

# Wait for the SSH tunnel to establish
ssh_process.wait()


