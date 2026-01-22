from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config

def place_limit_order(symbol, side, qty, price, time_in_force='GTC'):
    """
    Places a Limit Order.
    """
    try:
        validate_inputs(symbol, side, qty, price)
        
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        logger.info(f"Placing Limit Order: {side} {qty} {symbol} @ {price}")
        response = client.place_order(symbol, side.upper(), 'LIMIT', qty, price, time_in_force)
        
        logger.info(f"Limit Order Placed: {response['orderId']}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place limit order: {e}")
        return None
