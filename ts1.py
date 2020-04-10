import socket
import sys

port = int(sys.argv[1])

def read_dns_rec(addr):
    result = {}
    with open(addr, encoding = 'utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = line.rstrip() # get rid of trailing space
            elems = line.split(' ')
            if(str(elems[2]) == 'A'):
                result[elems[0]] = elems[1]
    return result


dic = read_dns_rec('PROJ2-DNSTS1.txt')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_binder = ('', port)
sock.bind(in_binder)
sock.listen(1)

csockid, _ = sock.accept()
new_msg = csockid.recv(1024).decode('utf-8')
while len(new_msg) != 0:
    search_result = dic.get(new_msg, '')
    if search_result != '':
        msg = '{} {} A'.format(new_msg, search_result)
        csockid.send(msg.encode('utf-8'))
    new_msg = csockid.recv(1024).decode('utf-8')
sock.close()
    