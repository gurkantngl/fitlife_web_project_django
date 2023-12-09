from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
import base64

def generate_key():
    return urlsafe_b64encode(os.urandom(32)).decode('utf-8')

def generate_iv():
    return os.urandom(16)

def encrypt(plain_text, key):
    key = urlsafe_b64decode(key)

    iv = generate_iv()

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    cipher_text = encryptor.update(plain_text.encode('utf-8')) + encryptor.finalize()

    tag = encryptor.tag

    return cipher_text, iv, tag

def decrypt(cipher_text, iv, tag, key):
    key = urlsafe_b64decode(key)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    return plain_text.decode('utf-8')


def encode(text):
    encodedText = base64.b64encode(text).decode('utf-8')
    return encodedText

def decode(text):
    decodedText = base64.b64decode(text).decode(text)
    return decodedText
    
key = generate_key()

plain_text = "Merhaba, dünya!"

cipher_text, iv, tag = encrypt(plain_text, key)
print("Şifrelenmiş metin:", cipher_text)



decrypted_text = decrypt(cipher_text, iv, tag, key)
print("Çözülmüş metin:", decrypted_text)

cipher_text = encrypt(plain_text, key)
print(type(encode(cipher_text)))
#print(type(decode()))