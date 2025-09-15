# crypto_manager.py - handles encryption and decryption of passwords
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoManager:
    def __init__(self, master_password=None, salt=None):
        """
        Initialize crypto manager with master password and salt.
        If salt is None, a new one will be generated.
        """
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = salt
            
        if master_password is not None:
            self.key = self._derive_key(master_password, self.salt)
            self.cipher = Fernet(self.key)
        else:
            self.key = None
            self.cipher = None

    def _derive_key(self, password, salt):
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def get_salt_b64(self):
        """Return base64 encoded salt for storage"""
        return base64.b64encode(self.salt).decode()

    def set_master_password(self, master_password):
        """Set or change the master password"""
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        """Encrypt data using the derived key"""
        if self.cipher is None:
            raise ValueError("Master password not set. Call set_master_password() first.")
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token):
        """Decrypt data using the derived key"""
        if self.cipher is None:
            raise ValueError("Master password not set. Call set_master_password() first.")
        return self.cipher.decrypt(token).decode()
