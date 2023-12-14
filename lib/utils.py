from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(master_password_hash):
    key = hashlib.sha256(master_password_hash.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_password(password, master_password_hash):
    key = generate_key(master_password_hash)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()
