import logging
import sys

sys.path.append("/opt/device")
logging.basicConfig(level=logging.INFO)

from encryption.functions import *
from encryption.encryption import *
from encryption.config import *
import json
from utils.generate_random_data import *
import socket, time

MIN_SLEEP = 60
MAX_SLEEP = 60 * 3

config_data = None

def send_data(data):
    sensible_data = config_data["sensible_data"]
    ip_to_send = config_data["ip_control_system_data"]
    port_to_send = config_data["port_normal_listen_service"]
    my_ip = config_data["IP_data"]

    if sensible_data:
        data = encrypt_message(data)
        port_to_send = config_data["port_sensible_listen_service"]
    else:
        data = data.encode("ISO-8859-1")

    private_key = load_private_key("/opt/device/encryption/PRIVATE_KEY")
    signature = firm_data(data, private_key)
    message = {"IP_data": my_ip, "data": data.decode("ISO-8859-1"), "signature": signature.decode("ISO-8859-1")}
    message = json.dumps(message)
    message = message.encode("ISO-8859-1")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_to_send, port_to_send))
        s.sendall(message)


def encrypt_message(message_decrypted):
    private_key = load_private_key("/opt/device/encryption/PRIVATE_KEY")
    public_key = load_public_key("/opt/device/encryption/PUBLIC_KEY")
    public_key_control_system = load_public_key("/opt/device/encryption/PUBLIC_KEY_CONTROL_SYSTEM")
    encryptor = Encryption(private_key, public_key)
    encrypted_msg = encryptor.encrypt(message_decrypted, public_key_control_system)
    return encrypted_msg


if __name__ == "__main__":
    logging.info("Initializing send sensible data service...")
    while True:
        try:
            logging.info("Generating new sample data...")
            with open("/opt/device/config/config.json") as f:
                config_data = json.load(f)
            data_to_send = generate_random_data_by_type_device(config_data["type_device"])
            data_to_send = json.dumps(data_to_send)
            logging.info("DATA TO SEND: " + str(data_to_send))
            send_data(data_to_send)

        except Exception as e:
            logging.exception("EXCEPTION: " + str(e))

        random_sleep = random.randint(MIN_SLEEP, MAX_SLEEP)
        logging.info("Sleeping" + str(random_sleep) + " seconds...")
        time.sleep(random_sleep)
