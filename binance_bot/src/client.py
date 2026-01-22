import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from src.utils import logger

class BinanceClient:
    def __init__(self, api_key, api_secret, base_url="https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key
        })

    def _sign(self, params):
        """
        Signs the request parameters using HMAC SHA256.
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def send_request(self, method, endpoint, params=None):
        """
        Sends a signed request to the Binance API.
        """
        if params is None:
            params = {}
            
        # Add timestamp
        params['timestamp'] = int(time.time() * 1000)
        
        # Sign
        params['signature'] = self._sign(params)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Sending {method} request to {endpoint} with params: {params}")
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request Error: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, time_in_force="GTC"):
        """
        Places a new order.
        """
        endpoint = "/fapi/v1/order"
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if price:
            params['price'] = price
            params['timeInForce'] = time_in_force
            
        return self.send_request('POST', endpoint, params)

    def get_account_info(self):
        """
        Retrieves account information.
        """
        endpoint = "/fapi/v2/account"
        return self.send_request('GET', endpoint)
