# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import redis
import unittest
from unittest.mock import patch
from app.src.client import getQuote
from app.api.stock import getStock
import importlib

# Import the create_app function dynamically from main.py
main_module = importlib.import_module('app.api.main')
create_app = main_module.create_app

# Create a redis connection object
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

# Create a test client for the Flask app
app = create_app()
client = app.test_client()

class TestGetStock(unittest.TestCase):
    @patch('app.api.stock.getQuote')
    def test_valid_stock_symbol(self, mock_get_quote):
        symbol = "AAPL"
        mock_get_quote.return_value = {
            'status': 'OK',
            'from': '2024-04-26',
            'symbol': symbol,
            'open': 169.88,
            'high': 171.34,
            'low': 169.18,
            'close': 169.3,
            'volume': 44014087.0,
            'afterHours': 169.6,
            'preMarket': 169.99
        }
        quote = getStock(symbol)
        self.assertEqual(symbol, 'AAPL')
        self.assertIsInstance(quote, str)
        self.assertTrue('symbol' in quote)

    @patch('app.api.stock.getQuote')
    def test_invalid_stock_symbol(self, mock_get_quote):
        mock_get_quote.side_effect = Exception('Missing "stock_symbol" parameter')
        with self.assertRaises(Exception) as context:
            getStock('INVALID')
        self.assertTrue(str(context.exception).startswith('Missing "stock_symbol" parameter'))

    @patch('app.api.stock.getQuote')
    def test_cache_hit(self, mock_get_quote):
        """Test that get_stock returns cached data for a valid stock_symbol."""
        symbol = "AAPL"
        expected_dict = {
            'status': 'OK',
            'from': '2024-04-26',
            'symbol': symbol,
            'open': 169.88,
            'high': 171.34,
            'low': 169.18,
            'close': 169.3,
            'volume': 44014087.0,
            'afterHours': 169.6,
            'preMarket': 169.99
        }
        mock_get_quote.return_value = expected_dict
        cached_data = json.dumps(expected_dict)
        redis_conn.set(symbol, cached_data, ex=30)
        quote = getStock(symbol)
        self.assertEqual(expected_dict, json.loads(quote))
        self.assertEqual(symbol, 'AAPL')

    @patch('app.api.stock.getQuote')
    def test_update_stock(self, mock_get_quote):
        amount = 10
        symbol = "AAPL"
        response = client.post(f'/stock/{symbol}', json={'amount': amount})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), f'{amount} stocks of {symbol} purchased!')

if __name__ == '__main__':
    print("Starting get_stock test...")
    unittest.main()
