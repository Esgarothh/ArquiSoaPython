import subprocess


local_port = 5000


remote_host = '200.14.84.16'
remote_port = 5000

ssh_username = 'YOUR_USER'
ssh_host = '200.14.84.16'
ssh_port = 8080

# controlsocket
control_socket = f'/tmp/ssh-{ssh_username}@{ssh_host}-{ssh_port}-control'


ssh_command = f'ssh -M -S {control_socket} -L {local_port}:{remote_host}:{remote_port} -p {ssh_port} {ssh_username}@{ssh_host}'
ssh_process = subprocess.Popen(ssh_command, shell=True)


ssh_process.wait()
