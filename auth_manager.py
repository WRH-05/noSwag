import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import os
import time

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

class AuthManager:
    def __init__(self):
        # Load email config from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.pending_codes = {}  # Store verification codes temporarily
        
        if not self.username or not self.password:
            print("Warning: Email credentials not configured.")
            print("Please create a .env file with EMAIL_ADDRESS and EMAIL_PASSWORD.")
            print("See .env.example for setup instructions.")

    def send_email(self, to_email, subject, body):
        """Send email with verification code"""
        if not self.username or not self.password:
            print("Email credentials not configured. Cannot send verification email.")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        
    def generate_verification_code(self, length=6):
        """Generate secure random verification code"""
        return ''.join(secrets.choice('0123456789') for _ in range(length))

    def send_verification_email(self, email):
        """Send verification code to email and store it temporarily"""
        code = self.generate_verification_code()
        self.pending_codes[email] = {
            "code": code,
            "timestamp": time.time()
        }
        
        subject = "noSwag Password Manager - Verification Code"
        body = f"""
        Welcome to noSwag Password Manager!
        
        Your verification code is: {code}
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        """
        
        return self.send_email(email, subject, body)

    def verify_code(self, email, input_code):
        """Verify the entered code against stored code"""
        if email not in self.pending_codes:
            return False
            
        stored_data = self.pending_codes[email]
        stored_code = stored_data["code"]
        timestamp = stored_data["timestamp"]
        
        # Check if code has expired (10 minutes)
        if time.time() - timestamp > 600:
            del self.pending_codes[email]
            return False
            
        # Check if code matches
        if input_code == stored_code:
            del self.pending_codes[email]  # Clear used code
            return True
            
        return False

    def cleanup_expired_codes(self):
        """Remove expired verification codes"""
        current_time = time.time()
        expired_emails = [
            email for email, data in self.pending_codes.items()
            if current_time - data["timestamp"] > 600
        ]
        
        for email in expired_emails:
            del self.pending_codes[email]
