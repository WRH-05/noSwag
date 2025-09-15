# noSwag Password Manager Setup Instructions

## Prerequisites

1. Install required Python packages:
```bash
pip install cryptography
```

2. Set up email credentials for verification codes (optional but recommended):
   - Copy `.env.example` to `.env`
   - Follow the Gmail setup instructions in the file
   - Add your actual email and app password

## Getting Started

### First Time Setup

1. Run the password manager:
```bash
python noSwag.py
```

2. Register a new account:
   - Type `register` or `r`
   - Enter your email address
   - Check your email for verification code
   - Enter the 6-digit code
   - Create a secure master password

3. Login and start using:
   - Type `login` or `l`
   - Enter your master password
   - Use `help` to see all available commands

## Available Commands

- `help` - Show all commands
- `register` - Create new account with email verification
- `login` - Login to your account
- `add` - Add a new password (with option to generate secure passwords)
- `get` - Retrieve a stored password
- `list` - List all stored sites
- `delete` - Remove a password entry
- `generate` - Generate secure passwords without storing
- `logout` - Logout from current session
- `exit` - Close the application

## Security Features

- **Master Password**: Single password that encrypts all your data
- **PBKDF2 Key Derivation**: Industry-standard password hashing
- **Fernet Encryption**: AES 128 encryption for your password data
- **Email Verification**: Confirms account ownership during registration
- **Salt Usage**: Prevents rainbow table attacks
- **Secure Password Generation**: Multiple options for creating strong passwords

## File Structure

- `data.json` - Your encrypted password vault (created after registration)
- `noSwag.py` - Main CLI application
- `storage_manager.py` - Handles encrypted file operations
- `crypto_manager.py` - Encryption/decryption logic
- `auth_manager.py` - Email verification system
- `password_generator.py` - Secure password generation

## Important Notes

- **Backup your data.json file** - It contains all your passwords
- **Remember your master password** - It cannot be recovered if lost
- Your master password never leaves your computer
- All passwords are encrypted before being stored
- Email verification is optional but recommended for account recovery

## Troubleshooting

- If email sending fails, check your .env configuration
- Make sure you're using a Gmail app password, not your regular password
- Run without email verification if needed (registration will still work)
- Check that all Python dependencies are installed