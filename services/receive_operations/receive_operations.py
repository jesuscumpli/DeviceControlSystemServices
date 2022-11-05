from socketserver import TCPServer, StreamRequestHandler
import socket
import logging

import sys
sys.path.append("/opt/controlSystem")

logging.basicConfig(level=logging.INFO)
import json

HOST, PORT = "localhost", 8888

class Handler(StreamRequestHandler):
    def handle(self):
        try:
            self.data = self.rfile.readline().strip()
            logging.info("DATOS RECIBIDOS DE <%s>: %s" % (self.client_address, self.data))
            self.normalize_data()
            logging.info("Operacion recibida: " + str(self.data))
            # TODO

        except Exception as e:
            logging.exception(str(e))

    def normalize_data(self):
        data = self.data
        try:
            data = data.decode()
        except:
            try:
                data = data.decode('ISO-8859-1')
            except:
                data = str(data)
        try:
            data = json.loads(data)
        except Exception as e:
            logging.exception(str(e))
        self.data = json.dumps(data)

class Server(TCPServer):
    SYSTEMD_FIRST_SOCKET_FD = 3

    def __init__(self, server_address, handler_cls):
        TCPServer.__init__(self, server_address, handler_cls, bind_and_activate=False)
        self.socket = socket.fromfd(self.SYSTEMD_FIRST_SOCKET_FD, self.address_family, self.socket_type)


if __name__ == "__main__":
    server = Server((HOST, PORT), Handler)
    print("Loading server")
    server.serve_forever()
    logging.info("Success")
    print("Successs")
