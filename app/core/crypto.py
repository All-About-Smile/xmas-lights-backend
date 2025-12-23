import base64

from cryptography.fernet import Fernet


class CryptoService:
    def __init__(self, secret_key: str):
        key = base64.urlsafe_b64encode(secret_key.encode().ljust(32)[:32])
        self.fernet = Fernet(key)

    def encrypt(self, plain_text: str) -> str:
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        return self.fernet.decrypt(encrypted_text.encode()).decode()

    def is_encrypted(value: str) -> bool:
        return value.startswith("gAAAA")
