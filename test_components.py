#!/usr/bin/env python3
# test_components.py - Test individual components

print("Testing noSwag Password Manager Components...")
print("-" * 40)

# Test CryptoManager
try:
    from crypto_manager import CryptoManager
    
    # Test basic encryption/decryption
    crypto = CryptoManager("test_password")
    original = "Hello, World!"
    encrypted = crypto.encrypt(original)
    decrypted = crypto.decrypt(encrypted)
    
    print(f"✓ CryptoManager: {original} -> encrypted -> {decrypted}")
    assert original == decrypted
    print("✓ CryptoManager encryption/decryption works")
    
except Exception as e:
    print(f"✗ CryptoManager failed: {e}")

# Test StorageManager
try:
    from storage_manager import StorageManager
    import os
    
    # Clean up any existing test file
    test_file = "test_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    storage = StorageManager(test_file)
    
    # Test user initialization
    result = storage.initialize_new_user("test@example.com", "test_password")
    print(f"✓ StorageManager: User initialization: {result}")
    
    # Test loading user data
    user_data = storage.load_user_data("test_password")
    print(f"✓ StorageManager: User data loaded: {user_data is not None}")
    
    # Test saving password
    storage.save_password("github.com", "testuser", "testpass123", "Test account")
    print("✓ StorageManager: Password saved")
    
    # Test retrieving password
    entry = storage.get_password("github.com")
    print(f"✓ StorageManager: Password retrieved: {entry['username'] == 'testuser'}")
    
    # Clean up
    os.remove(test_file)
    print("✓ StorageManager: Test cleanup completed")
    
except Exception as e:
    print(f"✗ StorageManager failed: {e}")

# Test PasswordGenerator
try:
    from password_generator import PasswordGenerator
    
    pg = PasswordGenerator()
    
    # Test password generation
    password = pg.generate_password(12)
    print(f"✓ PasswordGenerator: Generated 12-char password: {password}")
    
    # Test passphrase generation
    passphrase = pg.generate_passphrase(4)
    print(f"✓ PasswordGenerator: Generated passphrase: {passphrase}")
    
    # Test strength checking
    strength = pg.check_password_strength(password)
    print(f"✓ PasswordGenerator: Password strength: {strength['strength']}")
    
except Exception as e:
    print(f"✗ PasswordGenerator failed: {e}")

# Test AuthManager (without actually sending emails)
try:
    from auth_manager import AuthManager
    
    auth = AuthManager()
    
    # Test code generation
    code = auth.generate_verification_code()
    print(f"✓ AuthManager: Generated verification code: {code}")
    print(f"✓ AuthManager: Code length: {len(code) == 6}")
    
    # Test code verification
    auth.pending_codes["test@example.com"] = {
        "code": "123456",
        "timestamp": __import__('time').time()
    }
    
    result = auth.verify_code("test@example.com", "123456")
    print(f"✓ AuthManager: Code verification: {result}")
    
except Exception as e:
    print(f"✗ AuthManager failed: {e}")

print("-" * 40)
print("Component testing completed!")
print("\nTo test the full CLI application, run: python noSwag.py")