# storage_manager.py - handles secure JSON file operations
import json
import os
import base64
from datetime import datetime
from crypto_manager import CryptoManager

class StorageManager:
    def __init__(self, file_path="data.json"):
        self.file_path = file_path
        self.crypto = None

    def initialize_new_user(self, email, master_password):
        """Initialize storage for a new user"""
        self.crypto = CryptoManager(master_password)
        
        # Create initial data structure
        initial_passwords = {"passwords": {}}
        encrypted_data = self.crypto.encrypt(json.dumps(initial_passwords))
        
        data = {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "salt": self.crypto.get_salt_b64(),
                "iterations": 100000
            },
            "user": {
                "email": email,
                "verified": True,
                "last_login": datetime.now().isoformat()
            },
            "encrypted_data": base64.b64encode(encrypted_data).decode()
        }
        
        # Create directory if it doesn't exist
        if os.path.dirname(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True

    def load_user_data(self, master_password):
        """Load and decrypt user data"""
        if not os.path.exists(self.file_path):
            return None
            
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            
            # Initialize crypto with stored salt
            salt = base64.b64decode(data["metadata"]["salt"])
            self.crypto = CryptoManager(master_password, salt)
            
            # Decrypt password data
            encrypted_data = base64.b64decode(data["encrypted_data"])
            decrypted_json = self.crypto.decrypt(encrypted_data)
            password_data = json.loads(decrypted_json)
            
            # Update last login
            data["user"]["last_login"] = datetime.now().isoformat()
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return {
                "user": data["user"],
                "passwords": password_data["passwords"]
            }
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def save_password(self, site, username, password, notes=""):
        """Add or update a password entry"""
        if self.crypto is None:
            raise ValueError("Storage not initialized. Load user data first.")
            
        # Load current data
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        # Decrypt existing passwords
        encrypted_data = base64.b64decode(data["encrypted_data"])
        decrypted_json = self.crypto.decrypt(encrypted_data)
        password_data = json.loads(decrypted_json)
        
        # Add new password
        password_data["passwords"][site] = {
            "username": username,
            "password": password,
            "notes": notes,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        
        # Re-encrypt and save
        new_encrypted_data = self.crypto.encrypt(json.dumps(password_data))
        data["encrypted_data"] = base64.b64encode(new_encrypted_data).decode()
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True

    def get_password(self, site):
        """Retrieve a password entry"""
        if self.crypto is None:
            raise ValueError("Storage not initialized. Load user data first.")
            
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        encrypted_data = base64.b64decode(data["encrypted_data"])
        decrypted_json = self.crypto.decrypt(encrypted_data)
        password_data = json.loads(decrypted_json)
        
        return password_data["passwords"].get(site)

    def list_sites(self):
        """List all stored sites"""
        if self.crypto is None:
            raise ValueError("Storage not initialized. Load user data first.")
            
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        encrypted_data = base64.b64decode(data["encrypted_data"])
        decrypted_json = self.crypto.decrypt(encrypted_data)
        password_data = json.loads(decrypted_json)
        
        return list(password_data["passwords"].keys())

    def delete_password(self, site):
        """Delete a password entry"""
        if self.crypto is None:
            raise ValueError("Storage not initialized. Load user data first.")
            
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        encrypted_data = base64.b64decode(data["encrypted_data"])
        decrypted_json = self.crypto.decrypt(encrypted_data)
        password_data = json.loads(decrypted_json)
        
        if site in password_data["passwords"]:
            del password_data["passwords"][site]
            
            # Re-encrypt and save
            new_encrypted_data = self.crypto.encrypt(json.dumps(password_data))
            data["encrypted_data"] = base64.b64encode(new_encrypted_data).decode()
            
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        return False

    def user_exists(self):
        """Check if user data file exists"""
        return os.path.exists(self.file_path)

    def get_user_email(self):
        """Get user email from storage"""
        if not os.path.exists(self.file_path):
            return None
            
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            
        return data["user"]["email"]