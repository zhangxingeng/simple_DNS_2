import socket
import select
import sys
import time

port_in = int(sys.argv[1])
host_out_1 = sys.argv[2]
port_out1 = int(sys.argv[3])
host_out_2 = sys.argv[4]
port_out2 = int(sys.argv[5])

#create an incoming socket
in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_binder = ('', port_in)
in_sock.bind(in_binder)
in_sock.listen(1)

 # Create an outgoing socket
out_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_1_ip = socket.gethostbyname(host_out_1)
out_binder1 = (out_1_ip, port_out1)
out_sock1.connect(out_binder1)

out_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_2_ip = socket.gethostbyname(host_out_2)
out_binder2 = (out_2_ip, port_out2)
out_sock2.connect(out_binder2)

cli_conn, _ = in_sock.accept()
data = cli_conn.recv(1024)
    
while len(data) != 0:
    out_sock1.send(data)
    out_sock2.send(data)
    ins, _, _ = select.select([out_sock1, out_sock2], [], [], 5)
    if ins:
        income = ins[0]
        if income == out_sock1 or income == out_sock2:
            resp = income.recv(200)
        cli_conn.send(resp)
    
    if not ins:
        # timeout respond to client
        #print("time out at middle server.")
        cli_conn.send(('{} - Error:HOST NOT FOUND'.format(data.decode('utf-8'))).encode('utf-8'))
    data = cli_conn.recv(1024)
    
out_sock1.close()
out_sock2.close()
in_sock.close()
            
   
             
                










































