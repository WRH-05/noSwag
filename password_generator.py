# password_generator.py - secure password generation utilities
import secrets
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, 
                         use_symbols=True, exclude_ambiguous=False):
        """Generate a secure random password"""
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
            
        character_set = self.lowercase
        
        if use_uppercase:
            character_set += self.uppercase
        if use_digits:
            character_set += self.digits
        if use_symbols:
            character_set += self.symbols
            
        if exclude_ambiguous:
            # Remove potentially ambiguous characters
            ambiguous = "0O1lI|"
            character_set = ''.join(c for c in character_set if c not in ambiguous)
        
        # Ensure password contains at least one character from each enabled set
        password = []
        
        # Add one character from each enabled set
        password.append(secrets.choice(self.lowercase))
        if use_uppercase:
            password.append(secrets.choice(self.uppercase))
        if use_digits:
            password.append(secrets.choice(self.digits))
        if use_symbols:
            password.append(secrets.choice(self.symbols))
            
        # Fill the rest with random characters from the full set
        for _ in range(length - len(password)):
            password.append(secrets.choice(character_set))
            
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def generate_passphrase(self, num_words=4, separator="-", capitalize=False):
        """Generate a passphrase using random words"""
        # Simple word list for demonstration
        words = [
            "apple", "beach", "chair", "dream", "eagle", "flame", "grape", "house",
            "ocean", "piano", "queen", "river", "storm", "tiger", "umbrella", "violet",
            "whale", "zebra", "brave", "calm", "dance", "earth", "forest", "golden",
            "happy", "island", "jungle", "knight", "light", "magic", "nature", "peace",
            "quick", "royal", "shine", "trust", "unity", "victory", "wisdom", "youth"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
            
        return separator.join(selected_words)
    
    def check_password_strength(self, password):
        """Analyze password strength"""
        score = 0
        feedback = []
        
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters (12+ recommended)")
            
        if any(c in self.lowercase for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")
            
        if any(c in self.uppercase for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")
            
        if any(c in self.digits for c in password):
            score += 1
        else:
            feedback.append("Include numbers")
            
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Include special characters")
            
        # Check for common patterns
        if password.lower() in ["password", "123456", "qwerty", "admin"]:
            score = 0
            feedback.append("Avoid common passwords")
            
        strength_levels = {
            0: "Very Weak",
            1: "Weak", 
            2: "Weak",
            3: "Fair",
            4: "Good",
            5: "Strong",
            6: "Very Strong"
        }
        
        strength = strength_levels.get(score, "Very Weak")
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }