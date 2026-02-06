"""
Security utilities for authentication, authorization, and encryption
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

from app.core.config import settings


# Password hashing - use argon2 instead of bcrypt to avoid 72-byte limit
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Data to encode in the token
    
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate JWT token
    
    Args:
        token: JWT token to decode
    
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


# Data Encryption using Fernet (symmetric encryption)
class DataEncryption:
    """Handle encryption and decryption of sensitive data"""
    
    def __init__(self):
        self.fernet = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        if not data:
            return data
        encrypted = self.fernet.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        if not encrypted_data:
            return encrypted_data
        try:
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")


# AES Encryption for file data
class AESEncryption:
    """AES-256 encryption for files and large data"""
    
    def __init__(self):
        self.key = settings.AES_ENCRYPTION_KEY.encode()[:32]  # Ensure 32 bytes for AES-256
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt bytes data using AES-256"""
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data to be multiple of 16 bytes
        padding_length = 16 - (len(data) % 16)
        padded_data = data + (bytes([padding_length]) * padding_length)
        
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt bytes data using AES-256"""
        iv = encrypted_data[:16]
        encrypted_content = encrypted_data[16:]
        
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        decrypted_padded = decryptor.update(encrypted_content) + decryptor.finalize()
        
        # Remove padding
        padding_length = decrypted_padded[-1]
        return decrypted_padded[:-padding_length]


# Initialize encryption instances
data_encryption = DataEncryption()
aes_encryption = AESEncryption()


def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data like API keys, passwords, etc."""
    return data_encryption.encrypt(data)


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    return data_encryption.decrypt(encrypted_data)


def encrypt_file_data(file_data: bytes) -> bytes:
    """Encrypt file data"""
    return aes_encryption.encrypt(file_data)


def decrypt_file_data(encrypted_data: bytes) -> bytes:
    """Decrypt file data"""
    return aes_encryption.decrypt(encrypted_data)


def generate_api_key() -> str:
    """Generate a random API key for external integrations"""
    return base64.urlsafe_b64encode(os.urandom(32)).decode()


def mask_sensitive_info(data: str, visible_chars: int = 4) -> str:
    """
    Mask sensitive information, showing only last few characters
    
    Args:
        data: String to mask
        visible_chars: Number of characters to keep visible
    
    Returns:
        Masked string
    """
    if not data or len(data) <= visible_chars:
        return "****"
    return "*" * (len(data) - visible_chars) + data[-visible_chars:]
