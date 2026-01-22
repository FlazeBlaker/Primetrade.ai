from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config

def place_market_order(symbol, side, qty):
    """
    Places a Market Order.
    """
    try:
        validate_inputs(symbol, side, qty)
        
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        logger.info(f"Placing Market Order: {side} {qty} {symbol}")
        response = client.place_order(symbol, side.upper(), 'MARKET', qty)
        
        logger.info(f"Market Order Placed: {response['orderId']}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place market order: {e}")
        return None

if __name__ == "__main__":
    # Test
    # Not auto-running to avoid API calls without keys
    pass
