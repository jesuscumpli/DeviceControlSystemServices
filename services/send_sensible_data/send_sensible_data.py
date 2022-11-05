import logging
import sys

sys.path.append("/opt/device")
logging.basicConfig(level=logging.INFO)

from encryption.functions import *
from encryption.encryption import *
from encryption.config import *
import json
import random
import os
import time
from utils.generate_random_data import *
import socket, time, sys
import threading

MIN_SLEEP = 60
MAX_SLEEP = 60 * 3

f = open("/opt/device/config/config.json")
config_data = json.load(f)

def send_data(message):
    sensible_data = config_data["sensible_data"]
    ip_to_send = config_data["ip_control_system"]
    port_to_send = config_data["port_normal_listen_service"]
    if sensible_data:
        message = encrypt_message(message)
        port_to_send = config_data["port_sensible_listen_service"]
    else:
        message = message.encode()
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
            data_to_send = generate_random_data_by_type_device(config_data["type_device"])
            logging.info("DATA TO SEND: " + str(data_to_send))
            send_data(data_to_send)

        except Exception as e:
            logging.exception("EXCEPTION: " + str(e))

        random_sleep = random.randint(MIN_SLEEP, MAX_SLEEP)
        logging.info("Sleeping" + str(random_sleep) + " seconds...")
        time.sleep(random_sleep)

