import socket
import time 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_binder = ('localhost', 11133)
sock.bind(in_binder)
sock.listen(1)

while True:
    csockid, _ = sock.accept()
    new_msg = csockid.recv(1024)
    time.sleep(0.1)
    amount_sent = 0
    csockid.send(new_msg)
    print("got from tserver.")