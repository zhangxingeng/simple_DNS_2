import socket
import select
import sys
import time

#create an incoming socket
in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_binder = ('localhost', 11123)
in_sock.bind(in_binder)
in_sock.listen(1)

 # Create an outgoing socket
out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
out_binder = ('localhost', 11133)
out_sock.connect(out_binder)
out_sock.setblocking(0)

inputs = [out_sock] # Sockets from which we expect to read
outputs = [out_sock]# Sockets to which we expect to write
message_queues = {}# Outgoing message queues (socket:Queue)

while True:
    cli_conn, _ = in_sock.accept()
    data = cli_conn.recv(1024)
    print("got new msg from client.")
    
    ins, outs, ecp = select.select(inputs, outputs, [], 5)
    
    if not (ins or outs or ecp):
        # timeout respond to client
        print("time out at middle server.")
        continue
    
    for s in outs:
        if s is out_sock:
            s.sendall(data);
            print("msg sent from middle server.")

    for s in ins:
        if s is out_sock:
            num_recv = 0
            while num_recv < 1024:
                msg = s.recv(1024)
                num_recv += len(msg)
            
            print("bounce back: {}".format(msg.decode('utf-8')))
            cli_conn.send(msg)
    
                
   
             
                










































