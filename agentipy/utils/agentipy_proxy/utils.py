import base64
import os

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from agentipy.constants import API_VERSION, BASE_PROXY_URL


def get_encryption_key():
    response = requests.post(f"{BASE_PROXY_URL}/{API_VERSION}/security/get-encryption-key")
    data = response.json()
    return data["requestId"], base64.b64decode(data["encryptionKey"]), base64.b64decode(data["iv"])

def encrypt_private_key(private_key: str):
    """Encrypts the private key using a one-time encryption key from the server."""
    request_id, encryption_key, iv = get_encryption_key()

    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padding_length = 16 - (len(private_key) % 16)
    padded_private_key = private_key + (chr(padding_length) * padding_length)

    encrypted = encryptor.update(padded_private_key.encode()) + encryptor.finalize()
    
    return {
        "requestId": request_id,
        "encryptedPrivateKey": base64.b64encode(encrypted).decode(),
    }
