"""Authentication utility functions"""
import logging

def setup_logger():
    """Set up logging configuration"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

logger = setup_logger()

def validate_credentials(credentials, username, password):
    """
    Validate user credentials
    Returns tuple (is_valid, error_message)
    """
    if not username or not password:
        return False, "Username and password are required"
    
    if username not in credentials:
        logger.info(f"Login attempt: Username '{username}' not found")
        return False, "Invalid credentials"
        
    if credentials[username] != password:
        logger.info(f"Login attempt: Invalid password for user '{username}'")
        return False, "Invalid credentials"
    
    logger.info(f"Login successful for user: {username}")
    return True, None