import socket
from termcolor import colored
import pyfiglet

def target_communication():
	message = target.recv(1024)
	print(message.decode())


if __name__ == "__main__":

	ascii_banner = colored(pyfiglet.figlet_format(f"\nC2 Server\n"),"magenta")
	print(ascii_banner)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("127.0.0.1", 5555))
	print(colored("[+] Listening  for Incomig Connections.", "yellow"))
	sock.listen(5)

	target, ip = sock.accept()
	print(f"[+] Target connected from {ip}","green")

	target_communication()
