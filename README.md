# noSwag Password Manager

A secure, CLI-based password manager with email verification and strong encryption.

## Installation Options

### Option 1: Standalone Executable (Recommended for End Users)

Download the pre-built `noswag.exe` executable - no Python installation required!

1. **Download** `noswag.exe` from the releases
2. **Create a folder** for noSwag (e.g., `C:\noSwag\`)
3. **Place the executable** in the folder
4. **Add to PATH** for global access (optional)

**Requirements:**
- Windows 10/11 (64-bit)
- No Python installation needed
- No additional dependencies required

**Setup:**
```bash
# Create folder
mkdir C:\noSwag
cd C:\noSwag

# Place noswag.exe in this folder
# Create .env file with your email settings (see Email Configuration below)

# Test it works
noswag.exe
```

**Add to PATH (optional):**
1. Add `C:\noSwag` to your system PATH
2. Open new terminal and type: `noswag`

### Option 2: Run from Source (For Developers)

If you want to run from Python source code:

#### Prerequisites

1. **Install required Python packages:**
```bash
pip install cryptography python-dotenv
```

2. **Set up email credentials** (optional but recommended for account verification)

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

### Using the Executable (noswag.exe)

1. **Create your configuration:**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your Gmail credentials (see Email Configuration above)

2. **Run noSwag:**
   ```bash
   noswag.exe    # or just "noswag" if added to PATH
   ```

3. **Register a new account:**
   - Type `register`
   - Enter your email address
   - Check your email for verification code
   - Enter the 6-digit code
   - Create a secure master password

4. **Start using:**
   - Type `login` to access your vault
   - Use `help` to see all available commands

### Using Python Source Code

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

## Building Your Own Executable

Want to build the executable yourself? We've included `build_executable.py` for this purpose.

### Prerequisites for Building

1. **Install build dependencies:**
```bash
pip install pyinstaller cryptography python-dotenv
```

2. **Fix potential conflicts (Anaconda users):**
```bash
conda remove pathlib    # Remove obsolete pathlib package that conflicts with PyInstaller
```

### Build Process

1. **Run the build script:**
```bash
python build_executable.py
```

2. **Wait for completion** (2-5 minutes)

3. **Find your executable:**
   - Location: `dist/noswag.exe`
   - Size: ~20-30 MB (includes Python runtime and all dependencies)

### Build Script Features

The `build_executable.py` script includes:
- ✅ **Dependency checking** - Verifies all required files and packages
- ✅ **Conflict detection** - Checks for pathlib conflicts (common with Anaconda)
- ✅ **Auto-bundling** - Includes all Python modules and dependencies
- ✅ **Testing** - Validates the built executable works correctly
- ✅ **Size reporting** - Shows final executable size

### Troubleshooting Build Issues

**"pathlib package is obsolete" error:**
```bash
conda remove pathlib
# or
pip uninstall pathlib
```

**Missing dependencies:**
```bash
pip install --upgrade pyinstaller cryptography python-dotenv
```

**Build fails:**
1. Ensure all `.py` files are in the same directory
2. Check that Python 3.7+ is installed
3. Try building in a clean virtual environment

### Distribution

After building, you can distribute just the executable:
- ✅ **Share `noswag.exe`** - Others can use without Python
- ✅ **Include `.env.example`** - For email setup guidance  
- ✅ **Include `README.md`** - For instructions
- ❌ **Don't include your `.env`** - Contains your credentials!
- ❌ **Don't include your `data.json`** - Contains your encrypted passwords!

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

### For Executable Users:
- `noswag.exe` - The standalone executable (includes all Python code)
- `.env` - Your email configuration (create from `.env.example`)
- `data.json` - Your encrypted password vault (created automatically after registration)

### For Developers (Source Code):
- `noSwag.py` - Main CLI application
- `storage_manager.py` - Handles encrypted file operations
- `crypto_manager.py` - Encryption/decryption logic
- `auth_manager.py` - Email verification system
- `password_generator.py` - Secure password generation
- `build_executable.py` - Script to build standalone executable
- `.env.example` - Template for email setup
- `.gitignore` - Protects sensitive files from version control

### Important Files:
- **`.env`** - Keep this secure! Contains your email credentials
- **`data.json`** - Keep this safe! Contains your encrypted passwords  
- Both files are automatically excluded from Git for security

## Important Notes

- **Backup your data.json file** - It contains all your encrypted passwords
- **Remember your master password** - It cannot be recovered if lost
- **Keep your .env file secure** - It contains your email credentials
- Your master password never leaves your computer
- All passwords are encrypted before being stored
- Email verification is optional but recommended for account recovery
- The executable is portable and works on any Windows system without Python
- Your credentials are NOT hardcoded into the executable - they remain in your `.env` file

## Portable Setup

Create a portable noSwag installation:

```
📁 MyPortableNoSwag/
├── noswag.exe          # The executable (no secrets inside)
├── .env                # Your email configuration  
└── data.json           # Your encrypted passwords (created when you register)
```

You can move this folder anywhere and noSwag will work perfectly!

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