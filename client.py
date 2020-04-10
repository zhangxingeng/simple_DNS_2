import socket
import sys
import os

host = sys.argv[1]
port = int(sys.argv[2])
def file_to_array(file_path):
    result = []
    with open(file_path, encoding='utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = str(line.rstrip().lower())
            result.append(line)
    return result





sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
sock.connect(server_address)

addrs = file_to_array('PROJ2-HNS.txt');
os.remove("RESOLVED.txt") 
cnt = 0
for addr in addrs:
    sock.send(addr.encode('utf-8'))
    msg = sock.recv(1024).decode('utf-8')
    if len(msg) == 0:
            print("Error.")
            sock.close()
            exit()
    with open('RESOLVED.txt', 'a+') as f:
        f.write('{}\n'.format(msg))
    
    #recv_data = sock.recv(200).decode('utf-8')
    #print(recv_data)
    #recv_tup = str_to_tup(recv_data)
    #print_tup(recv_tup)

sock.close()





















