try:
    from config.config import *
except:
    from encryption.config import *
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256


def generate_and_save_keys(filename_private_key=FILENAME_PRIVATE_KEY, filename_public_key=FILENAME_PUBLIC_KEY):
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    public_key_bytes = public_key.exportKey()
    private_key_bytes = private_key.exportKey()

    with open(filename_private_key, "wb") as binary_file:
        binary_file.write(private_key_bytes)

    with open(filename_public_key, "wb") as binary_file:
        binary_file.write(public_key_bytes)

    return public_key_bytes

def generate_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return private_key, public_key

def load_public_key(filename_public_key=FILENAME_PUBLIC_KEY):
    with open(filename_public_key, "rb") as file:
        public_key_bytes = file.read()
    public_key = RSA.importKey(public_key_bytes)
    return public_key

def load_public_key_from_bytes(public_key_bytes):
    public_key = RSA.importKey(public_key_bytes)
    return public_key

def load_private_key(filename_private_key=FILENAME_PRIVATE_KEY):
    with open(filename_private_key, "rb") as file:
        private_key_bytes = file.read()
    private_key = RSA.importKey(private_key_bytes)
    return private_key

def firm_data(data, private_key):
    hash = SHA256.new(data)
    signer = PKCS115_SigScheme(private_key)
    signature = signer.sign(hash)
    return signature

def verify_signature(signature, data, public_key):
    hash = SHA256.new(data)
    verifier = PKCS115_SigScheme(public_key)
    try:
        verifier.verify(hash, signature)
    except:
        raise Exception("Error decrypting message: Signature incorrect!")
