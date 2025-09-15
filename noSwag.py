# CLI password manager - noSwag
import getpass
import os
import re
from storage_manager import StorageManager
from auth_manager import AuthManager
from password_generator import PasswordGenerator

class noSwagPasswordManager:
    def __init__(self):
        self.storage = StorageManager()
        self.auth = AuthManager()
        self.password_gen = PasswordGenerator()
        self.current_user = None
        self.is_authenticated = False

    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def get_master_password(self, prompt="Enter master password: "):
        """Get master password securely"""
        return getpass.getpass(prompt)

    def register_new_user(self):
        """Register a new user with email verification"""
        print("\n=== noSwag Password Manager Registration ===")
        
        # Get email
        while True:
            email = input("Enter your email address: ").strip()
            if self.is_valid_email(email):
                break
            print("Please enter a valid email address.")
        
        # Check if user already exists
        if self.storage.user_exists():
            existing_email = self.storage.get_user_email()
            if existing_email == email:
                print("An account with this email already exists. Please login instead.")
                return False
            else:
                print("A different user account already exists on this system.")
                return False
        
        # Send verification email
        print(f"Sending verification code to {email}...")
        if not self.auth.send_verification_email(email):
            print("Failed to send verification email. Please check your email settings.")
            return False
        
        # Get verification code
        max_attempts = 3
        for attempt in range(max_attempts):
            code = input("Enter the 6-digit verification code from your email: ").strip()
            if self.auth.verify_code(email, code):
                print("Email verified successfully!")
                break
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"Invalid code. {remaining} attempts remaining.")
                else:
                    print("Too many failed attempts. Please restart registration.")
                    return False
        
        # Get master password
        while True:
            password1 = self.get_master_password("Create a master password: ")
            if len(password1) < 8:
                print("Master password must be at least 8 characters long.")
                continue
            
            password2 = self.get_master_password("Confirm master password: ")
            if password1 == password2:
                break
            print("Passwords don't match. Please try again.")
        
        # Initialize user storage
        print("Setting up your secure vault...")
        if self.storage.initialize_new_user(email, password1):
            print("Registration completed successfully!")
            print("You can now login and start storing passwords.")
            return True
        else:
            print("Failed to create user storage.")
            return False

    def login_user(self):
        """Login existing user"""
        print("\n=== noSwag Password Manager Login ===")
        
        if not self.storage.user_exists():
            print("No user account found. Please register first.")
            return False
        
        email = self.storage.get_user_email()
        print(f"Logging in as: {email}")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            master_password = self.get_master_password()
            
            user_data = self.storage.load_user_data(master_password)
            if user_data is not None:
                self.current_user = user_data
                self.is_authenticated = True
                print("Login successful!")
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"Invalid master password. {remaining} attempts remaining.")
                else:
                    print("Too many failed attempts. Exiting for security.")
                    return False
        
        return False

    def add_password(self):
        """Add a new password entry"""
        if not self.is_authenticated:
            print("Please login first.")
            return
        
        print("\n=== Add New Password ===")
        site = input("Website/Service name: ").strip()
        if not site:
            print("Site name cannot be empty.")
            return
        
        username = input("Username/Email: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        
        choice = input("Generate password (g) or enter manually (m)? [g/m]: ").lower()
        
        if choice == 'g':
            # Generate password
            length = input("Password length (default 12): ").strip()
            length = int(length) if length.isdigit() else 12
            
            use_symbols = input("Include symbols? [Y/n]: ").lower() != 'n'
            exclude_ambiguous = input("Exclude ambiguous characters (0O1lI)? [y/N]: ").lower() == 'y'
            
            password = self.password_gen.generate_password(
                length=length,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            print(f"Generated password: {password}")
        else:
            password = getpass.getpass("Enter password: ")
            if not password:
                print("Password cannot be empty.")
                return
        
        notes = input("Notes (optional): ").strip()
        
        try:
            self.storage.save_password(site, username, password, notes)
            print(f"Password for {site} saved successfully!")
        except Exception as e:
            print(f"Error saving password: {e}")

    def get_password(self):
        """Retrieve a password"""
        if not self.is_authenticated:
            print("Please login first.")
            return
        
        print("\n=== Get Password ===")
        site = input("Website/Service name: ").strip()
        
        try:
            entry = self.storage.get_password(site)
            if entry:
                print(f"\nSite: {site}")
                print(f"Username: {entry['username']}")
                print(f"Password: {entry['password']}")
                if entry.get('notes'):
                    print(f"Notes: {entry['notes']}")
                print(f"Created: {entry.get('created', 'Unknown')}")
            else:
                print(f"No password found for '{site}'.")
        except Exception as e:
            print(f"Error retrieving password: {e}")

    def list_passwords(self):
        """List all stored sites"""
        if not self.is_authenticated:
            print("Please login first.")
            return
        
        try:
            sites = self.storage.list_sites()
            if sites:
                print(f"\n=== Stored Passwords ({len(sites)} total) ===")
                for i, site in enumerate(sorted(sites), 1):
                    print(f"{i}. {site}")
            else:
                print("No passwords stored yet.")
        except Exception as e:
            print(f"Error listing passwords: {e}")

    def delete_password(self):
        """Delete a password entry"""
        if not self.is_authenticated:
            print("Please login first.")
            return
        
        print("\n=== Delete Password ===")
        site = input("Website/Service name: ").strip()
        
        try:
            # Check if entry exists
            entry = self.storage.get_password(site)
            if not entry:
                print(f"No password found for '{site}'.")
                return
            
            # Confirm deletion
            print(f"Found entry for '{site}' (username: {entry['username']})")
            confirm = input("Are you sure you want to delete this entry? [y/N]: ").lower()
            
            if confirm == 'y':
                if self.storage.delete_password(site):
                    print(f"Password for '{site}' deleted successfully.")
                else:
                    print("Failed to delete password.")
            else:
                print("Deletion cancelled.")
        except Exception as e:
            print(f"Error deleting password: {e}")

    def generate_password_only(self):
        """Generate a password without storing it"""
        print("\n=== Password Generator ===")
        
        length = input("Password length (default 12): ").strip()
        length = int(length) if length.isdigit() and int(length) > 0 else 12
        
        use_uppercase = input("Include uppercase letters? [Y/n]: ").lower() != 'n'
        use_digits = input("Include numbers? [Y/n]: ").lower() != 'n'
        use_symbols = input("Include symbols? [Y/n]: ").lower() != 'n'
        exclude_ambiguous = input("Exclude ambiguous characters (0O1lI)? [y/N]: ").lower() == 'y'
        
        try:
            password = self.password_gen.generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
                exclude_ambiguous=exclude_ambiguous
            )
            
            print(f"\nGenerated password: {password}")
            
            # Show strength analysis
            strength = self.password_gen.check_password_strength(password)
            print(f"Strength: {strength['strength']} (Score: {strength['score']}/6)")
            
            # Option to generate passphrase
            passphrase_choice = input("\nGenerate a passphrase instead? [y/N]: ").lower()
            if passphrase_choice == 'y':
                num_words = input("Number of words (default 4): ").strip()
                num_words = int(num_words) if num_words.isdigit() else 4
                
                passphrase = self.password_gen.generate_passphrase(num_words=num_words)
                print(f"Generated passphrase: {passphrase}")
                
        except Exception as e:
            print(f"Error generating password: {e}")

    def show_help(self):
        """Show help message"""
        print("\n=== noSwag Password Manager Commands ===")
        print("  help, h     - Show this help message")
        print("  register, r - Register a new account")
        print("  login, l    - Login to your account")
        print("  add, a      - Add a new password")
        print("  get, g      - Get a stored password")
        print("  list, ls    - List all stored sites")
        print("  delete, del - Delete a password")
        print("  generate    - Generate a password without storing")
        print("  logout      - Logout from current session")
        print("  exit, quit  - Exit the program")

    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.is_authenticated = False
        print("Logged out successfully.")

    def main_loop(self):
        """Main program loop"""
        print("Welcome to noSwag - Secure CLI Password Manager!")
        print("Type 'help' for available commands.")
        
        if self.storage.user_exists():
            print(f"Existing user found: {self.storage.get_user_email()}")
            print("Type 'login' to access your passwords.")
        else:
            print("No existing user found. Type 'register' to create an account.")
        
        while True:
            try:
                if self.is_authenticated:
                    prompt = f"noSwag ({self.current_user['user']['email']})> "
                else:
                    prompt = "noSwag> "
                
                command = input(prompt).strip().lower()
                
                if command in ['help', 'h']:
                    self.show_help()
                elif command in ['register', 'r']:
                    self.register_new_user()
                elif command in ['login', 'l']:
                    self.login_user()
                elif command in ['add', 'a']:
                    self.add_password()
                elif command in ['get', 'g']:
                    self.get_password()
                elif command in ['list', 'ls']:
                    self.list_passwords()
                elif command in ['delete', 'del']:
                    self.delete_password()
                elif command == 'generate':
                    self.generate_password_only()
                elif command == 'logout':
                    self.logout()
                elif command in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit properly.")
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    """Entry point"""
    try:
        app = noSwagPasswordManager()
        app.main_loop()
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()