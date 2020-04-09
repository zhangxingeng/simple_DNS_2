import threading
import time
import random
import socket
import select
#  from sys import argv


def ls_server(self_port, ts1_addr, ts2_addr, ts1_port, ts2_port):
    
    ls_socket = establish_socket('', self_port, True)
    ls_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ts1_socket = establish_socket(ts1_addr, ts1_port, False)
    ts2_socket = establish_socket(ts2_addr, ts2_port, False)
    ts1_socket.setblocking(0)
    ts2_socket.setblocking(0)
    
    while True:
        ls_socket.listen(1)
        csockid, _ = ls_socket.accept()
        req = csockid.recv(200)
        
        servers = [ts1_socket, ts2_socket]
        ins, outs, _ = select.select(servers, servers, [], 5)
        for sk in outs:
            sk.send(req)
            
        for sk in ins:
            csockid.send(sk.recv(200))
            break
        
        if not (ins):
            csockid.send('404'.encode('utf-8'))
        
    return 0;


def ts_server(record, self_port):
    dic = read_dns_rec(record)
    ts_socket = establish_socket('', self_port, True)
    
    while True:
        ts_socket.listen(1)
        csockid, _ = ts_socket.accept()

        req_dns = csockid.recv(200).decode('utf-8')
        search_result = dic.get(req_dns, '')
        if(search_result == ''):
            continue
        msg = msg = '{} {} A'.format(req_dns, search_result)
        csockid.send(msg.encode('utf-8'))

    ts_socket.close()
    exit()


def client(query_file, ls_addr, ls_port):
    addrs = read_cl_input(query_file);
    cs = establish_socket(ls_addr, ls_port, False)
    cs.setblocking(10)
    for addr in addrs:
        print(addr)
        cs.send(addr.encode('utf-8'))
        recv_data = cs.recv(200).decode('utf-8')
        print(recv_data)
        continue
        #recv_tup = str_to_tup(recv_data)
        #print_tup(recv_tup)

    cs.close()
    return 0;

"""Helping function for ts server"""


def read_dns_rec(addr):
    result = {}
    with open(addr, encoding='utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = line.rstrip()  # get rid of trailing space
            elems = line.split(' ')
            if(str(elems[2]) == 'A'):
                result[elems[0]] = elems[1]
    return result


"""Helping function for Client"""
def read_cl_input(addr):
    """formatiing a files with domain names into a list."""
    result = []
    with open(addr, encoding='utf-8') as fp:
        line_list = fp.readlines()
        for line in line_list:
            line = str(line.rstrip().lower())
            result.append(line)
    return result




def establish_socket(addr, port, is_server):
    """Bind to a client or connect to a server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    server_binding = (addr, port)

    if(is_server):
        sock.bind(server_binding)
    else:
        sock.connect(server_binding)
    return sock



def str_to_tup(data):
    """convert a string splitted by space into a tuple"""
    data = data.rstrip()  # get rid of trailing space
    elems = data.split(' ')
    return elems

def print_tup(tup):
    """print out a tuple with length of 2 or 3"""
    if(len(tup) == 2):
        print("{} {}".format(*tup))
    elif (len(tup) == 3):
        print("{} {} {}".format(*tup))
    else:
        exit("Problem with Tuple.")
          
          
def main():  
    addr_cl = addr_ls = addr_ts1 = addr_ts2 = socket.gethostbyname(socket.gethostname())
    
    port_cl = 50007
    port_ls = 50008
    port_ts1 = 50009
    port_ts2 = 51000
    
    file_ts1 = 'PROJ2-DNSTS1.txt'
    file_ts2 = 'PROJ2-DNSTS2.txt'
    file_cl = 'PROJ2-HNS.txt'
    #  ts_server(record, ls_addr, self_port):
    args_ls = (port_ls, addr_ts1, addr_ts2, port_ts1, port_ts2)
    args_ts1 = (file_ts1, port_ts1)
    args_ts2 = (file_ts2, port_ts2)
    args_cl = (file_cl, addr_ls, port_ls)
               
    thread_ls = threading.Thread(name = 'ls', target = ls_server, args = args_ls)
    thread_ts1 = threading.Thread(name = 'ts1', target = ts_server, args = args_ts1)
    thread_ts2 = threading.Thread(name = 'ts2', target = ts_server, args = args_ts2)
    thread_cl = threading.Thread(name = 'cl', target = client, args = args_cl)
    
    thread_ts1.start()
    time.sleep(random.random() * 5)
    thread_ts2.start()
    time.sleep(random.random() * 5)
    thread_ls.start()
    time.sleep(random.random() * 5)
    thread_cl.start()



 
if __name__ == "__main__":
    main()  
    
    
    
    