from socketserver import TCPServer, StreamRequestHandler
import socket
import logging

import sys
sys.path.append("/opt/device")

logging.basicConfig(level=logging.INFO)
import json
from encryption.functions import *
from encryption.encryption import *
from encryption.config import *

HOST, PORT = "localhost", 8888

class Handler(StreamRequestHandler):
    def handle(self):
        self.ACK = "ERROR"
        try:
            self.data = self.rfile.readline().strip()
            logging.info("DATOS RECIBIDOS DE <%s>: %s" % (self.client_address, self.data))
            self.get_config_data()
            self.decode_message_info()
            self.verify_IP_control_system()
            self.verify_data()
            if self.config_data["encrypt_operation"]:
                self.decrypt_data()
            logging.info("MENSAJE DESENCRIPTADO: %s" % (self.data))
            self.normalize_data()
            self.change_configuration_by_operation()
            logging.info("Operacion REALIZADA: " + str(self.data))
            self.ACK = "OK"

        except Exception as e:
            logging.exception(str(e))
        # SEND ACK
        self.send_ACK()

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

    def verify_data(self):
        signature = self.message["signature"].encode("ISO-8859-1")
        public_key_objective = load_public_key("/opt/device/encryption/PUBLIC_KEY_CONTROL_SYSTEM")
        data = self.message["data"].encode("ISO-8859-1")
        verify_signature(signature, data, public_key_objective)

    def decrypt_data(self):
        public_key_objective = load_public_key("/opt/device/encryption/PUBLIC_KEY_CONTROL_SYSTEM")
        private_key = load_private_key("/opt/device/encryption/PRIVATE_KEY")
        public_key = load_public_key("/opt/device/encryption/PUBLIC_KEY")

        decryptor = Encryption(private_key, public_key)
        decrypted_msg = decryptor.decrypt(self.message["data"].encode("ISO-8859-1"), public_key_objective)
        self.data = decrypted_msg
        logging.info("DECRYPTED MESSAGE: " + str(decrypted_msg))

    def normalize_data(self):
        data = self.data
        try:
            data = json.loads(data)
        except Exception as e:
            logging.exception(str(e))
        self.operation = data

    def change_configuration_by_operation(self):
        for key_config, value_config in self.operation.items():
            config_data = self.config_data
            config_data[key_config] = value_config
            with open("/opt/device/config/config.json", 'w') as config_file:
                json.dump(config_data, config_file)

    def send_ACK(self):
        data = self.ACK
        data = data.encode("ISO-8859-1")
        self.wfile.write(data)


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
