# noSwag Password Manager

A secure, CLI-based password manager with email verification and strong encryption.

## Quick Start

### Prerequisites

1. **Install required Python packages:**
```bash
pip install cryptography python-dotenv
```

2. **Set up email credentials** (optional but recommended for account verification):

## Email Configuration Setup

### Option 1: Gmail App Password (RECOMMENDED)

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" or "Other" and enter "noSwag Password Manager"
4. Copy the generated 16-character password (like: `abcd efgh ijkl mnop`)

### Configure Your .env File

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
```

3. Save the file (it's already in `.gitignore` for security)

### Option 2: Google Service Account (ADVANCED)

For advanced users who prefer Gmail API over SMTP:

1. Create a [Google Cloud Project](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create a service account with Gmail send permissions
4. Download the JSON key file
5. Modify `auth_manager.py` to use Gmail API instead of SMTP

*Note: This requires additional code changes and dependencies.*

### Test Email Configuration
```bash
python -c "from auth_manager import AuthManager; auth = AuthManager(); print('✓ Email configured!' if auth.username else '✗ Email not configured')"
```

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

- `data.json` - Your encrypted password vault (created automatically after registration)
- `noSwag.py` - Main CLI application
- `.env` - Your email configuration (create from `.env.example`)
- `.env.example` - Template for email setup
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

### Email Issues
- **"Failed to send email" error:**
  - Check your Gmail app password is correct (16 characters, no spaces)
  - Ensure 2-Factor Authentication is enabled on your Gmail account
  - Verify your `.env` file has the correct format

- **"Email credentials not configured" warning:**
  - Make sure `.env` file exists in the project directory
  - Check that `EMAIL_ADDRESS` and `EMAIL_PASSWORD` are set correctly
  - Install python-dotenv: `pip install python-dotenv`

- **"Less secure app access" error:**
  - Use Gmail App Password instead of your regular Gmail password
  - Never use your regular Gmail password for applications

### Other Issues
- If email sending fails, you can still register (registration will work without email verification)
- Make sure all Python dependencies are installed: `pip install cryptography python-dotenv`
- If you forgot your master password, you'll need to delete `data.json` and start over (all data will be lost)