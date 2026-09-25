import cryptography
import os
import base64

def make_salt():
    salt_b = os.urandom(16)
    salt_s = base64.b64decode(salt_b).decode('utf-8')

def de_salt(sault_str: str):
    salted_bytes_back = base64.b64decode(sault_str.encode('utf-8'))
