from cryptography.fernet import Fernet
import os
from typing import Optional

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode()

# If no key provided, generate one (for testing only)
if not ENCRYPTION_KEY or ENCRYPTION_KEY == b"":
    ENCRYPTION_KEY = Fernet.generate_key()

cipher = Fernet(ENCRYPTION_KEY)


def encrypt_data(text: str) -> str:
    """Encrypt text using Fernet"""
    if not text:
        return text

    encrypted = cipher.encrypt(text.encode())
    return encrypted.decode()


def decrypt_data(token: str) -> str:
    """Decrypt token using Fernet"""
    if not token:
        return token

    try:
        decrypted = cipher.decrypt(token.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return token
