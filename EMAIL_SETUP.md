# Setup Instructions for noSwag Password Manager Email Configuration

## Quick Setup (Gmail App Password - RECOMMENDED)

### Step 1: Install Optional Dependencies
```bash
pip install python-dotenv
```
(This allows loading .env files automatically)

### Step 2: Set Up Gmail App Password
1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" or "Other" and enter "noSwag Password Manager"
4. Copy the generated 16-character password (like: `abcd efgh ijkl mnop`)

### Step 3: Configure Your .env File
1. Open the `.env` file in this directory
2. Replace `your-email@gmail.com` with your Gmail address
3. Replace `your-16-character-app-password` with the app password from step 2
4. Save the file

### Example .env file:
```
EMAIL_ADDRESS=john.doe@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
```

### Step 4: Test the Setup
Run the application and try registering a new account:
```bash
python noSwag.py
```

---

## Alternative: Google Service Account (ADVANCED)

If you prefer using Gmail API with a service account:

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API

### Step 2: Create Service Account
1. Go to IAM & Admin > Service Accounts
2. Create new service account
3. Download JSON key file
4. Grant necessary permissions

### Step 3: Update Code (Advanced Users Only)
You would need to modify `auth_manager.py` to use Gmail API instead of SMTP.
This requires additional dependencies and more complex setup.

---

## Troubleshooting

**"Failed to send email" error:**
- Check your Gmail app password is correct
- Ensure 2FA is enabled on your Gmail account
- Verify your .env file has the correct format

**"Email credentials not configured" warning:**
- Make sure .env file exists in the project directory
- Check that EMAIL_ADDRESS and EMAIL_PASSWORD are set
- Install python-dotenv: `pip install python-dotenv`

**"Less secure app access" error:**
- Use App Password instead of regular Gmail password
- Never use your regular Gmail password for apps