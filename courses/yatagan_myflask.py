from socket import socket


class App(object):

  def __init__(self):
    self.handlers = {}

  def handle_request(self, conn):
    with conn:
      request = conn.recv(1024).decode('utf8')
      path = request.split()[1]
      handler = self.handlers.get(path, self.handle404)
      response = handler()
      conn.sendall(response.encode('utf8'))

  @staticmethod
  def handle404():
    return 'HTTP/1.1 404 Not Found\r\n\r\nNot Found'

  def route(self, path):
    def wrapper(fun):
      def handler():
        return 'HTTP/1.1 200 Ok\r\n\r\n' + fun()
      self.handlers[path] = handler
    return wrapper

  def start(self, port=2222):
    s = socket()
    with s:
      s.bind(('localhost', port))
      s.listen(0)
      while True:
        conn, addr = s.accept()
        self.handle_request(conn)

if '__main__' == __name__:
  a = App()

  @a.route("/")
  def main():
    return "hey"

  @a.route("/hello")
  def hello():
    return "hello world"

  a.start()