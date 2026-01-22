from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config

def place_stop_limit_order(symbol, side, qty, price, stop_price, time_in_force='GTC'):
    """
    Places a Stop-Limit Order.
    Triggered when stop_price is hit, places a limit order at price.
    """
    try:
        validate_inputs(symbol, side, qty, price)
        if stop_price <= 0:
            raise ValueError("Stop Price must be positive.")
            
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        logger.info(f"Placing Stop-Limit: {side} {qty} {symbol} Trigger: {stop_price} Limit: {price}")
        
        endpoint = "/fapi/v1/order"
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'STOP',
            'quantity': qty,
            'price': price,
            'stopPrice': stop_price,
            'timeInForce': time_in_force
        }
        
        response = client.send_request('POST', endpoint, params)
        
        logger.info(f"Stop-Limit Order Placed: {response['orderId']}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place stop-limit order: {e}")
        return None
