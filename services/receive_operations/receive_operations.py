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
            self.get_config_data()
            self.decode_message_info()
            self.verify_IP_control_system()
            self.change_configuration_by_operation()
            logging.info("Operacion REALIZADA: " + str(self.data))

        except Exception as e:
            logging.exception(str(e))

    def get_config_data(self):
        with open("/opt/device/config/config.json") as f:
            self.config_data = json.load(f)

    def decode_message_info(self):
        message = self.data
        message = message.decode("ISO-8859-1")
        message = json.loads(message)
        self.message = message

    def verify_IP_control_system(self):
        IP_received = self.message["ip_control_system"]
        IP_control_system = self.config_data["ip_control_system"]
        if str(IP_received) != str(IP_control_system):
            raise Exception("IP RECEIVED IS NOT CONTROL SYSTEM: " + str(IP_received))

    def normalize_data(self):
        data = self.message["data"]
        try:
            data = json.loads(data)
        except Exception as e:
            logging.exception(str(e))
        self.operation = data

    def change_configuration_by_operation(self):
        key_config = self.operation["key_config"]
        value_config = self.operation["value_config"]
        config_data = self.config_data
        config_data[key_config] = value_config
        with open("/opt/device/config/config.json", 'w') as config_file:
            json.dump(config_data, config_file)

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
