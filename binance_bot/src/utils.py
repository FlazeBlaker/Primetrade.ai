import logging
import sys
import os

# Setup Logging
def setup_logger(log_file='bot.log'):
    """
    Configures logging to file and console.
    """
    logger = logging.getLogger('BinanceBot')
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicates
    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()

def validate_inputs(symbol, side, qty, price=None):
    """
    Validates common order inputs.
    """
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
    
    if qty <= 0:
        raise ValueError(f"Quantity must be positive. Got {qty}")
        
    if price is not None and price <= 0:
        raise ValueError(f"Price must be positive. Got {price}")
        
    return True
