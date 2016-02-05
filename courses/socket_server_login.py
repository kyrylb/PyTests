from socket import socket
from time import sleep
from threading import Thread
from datetime import datetime
from urllib import parse
from urllib import urlparse

s = socket()
s.bind(('localhost', 2222))
s.listen(0)

f = open('users', 'r')
lines = f.read().split()

def handle_request(conn):
    with conn:
        request = conn.recv(1024)

        path = request.decode('utf8').split()[1]

        if path == '/':
            body = """\
                    <html>
                        <header>
                            <title>server</title>
                        </header>
                        <body>
                            <form action="/login">
                                <input name="username"><br>
                                <input name="password"><br>
                                <input type="submit">
                            </form>
                        </body>
                    </html>
                """

            conn.sendall(('HTTP/1.1 200 Ok\r\n\r\n'+ body).encode('utf8'))

        elif path.startswith('/login'):
            #answer = 'string' in lines
            #urlib.parse.parse_qs
            print('login:', request)

            urlparse
            print(parse.parse_qs(path))
            conn.sendall(('HTTP/1.1 200 Ok\r\n\r\nWelcome').encode('utf8'))
        else:
            conn.sendall(('HTTP/1.1 404 No\r\n\r\n').encode('utf8'))


while True:
    conn, addr = s.accept()
    handle_request(conn)
