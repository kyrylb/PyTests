from socket import socket
from time import sleep
from threading import Thread
from datetime import datetime
import importlib

s = socket()
s.bind(('localhost', 2222))
s.listen(0)

def handle_request(conn):
    with conn:
        request = conn.recv(1024)
        print('request:', request)
        header = "HTTP/1.1 200 Ok"

        try:
            path = request.decode('utf8').split()[1]
            module_name = path[1:]
            module = importlib.import_module(module_name)
            functions = dir(module)

            ul = '<ul>'
            for f in functions:
                ul += '<li>%s</li>' % f
            ul += '</ul>'

            time = datetime.now()
            body = '<html><head><title>server</title></head><body> <br>%s  %s<body></html>' % (time, ul)

            conn.sendall((header + '\r\n\r\n' + body).encode('utf8'))
        except:
            conn.sendall("HTTP/1.1 500 No such module".encode('utf8'))

while True:
    conn, addr = s.accept()
    handle_request(conn)