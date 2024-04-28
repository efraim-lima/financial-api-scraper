import unittest
from unittest.mock import patch
from flask import json
from app import create_app
from app.src.client import getQuote

# For run this module:
# python -m test /app/api/app.py



class TestStockAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.src.client.getQuote')
    def test_get_stock(self, mock_getQuote):
        # Mock the getQuote function to return a sample stock quote
        mock_getQuote.return_value = {
            'symbol': 'AAPL',
            'price': 120.50,
            'change': 1.25,
            'changePercent': 1.05,
            'volume': 1000000
        }

        # Test the GET '/stock' endpoint
        response = self.client.get('/stocks/stock?ticker=AAPL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_getQuote.return_value)

    @patch('app.src.client.getQuote')
    def test_post_stock(self, mock_getQuote):
        # Mock the getQuote function to return a sample stock quote
        mock_getQuote.return_value = {
            'symbol': 'AAPL',
            'price': 120.50,
            'change': 1.25,
            'changePercent': 1.05,
            'volume': 1000000
        }

        # Test the POST '/stock' endpoint
        response = self.client.post('/stocks/stock?ticker=AAPL&amount=10')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': '10 units of stock AAPL were added to your stock record'})

    @patch('app.src.client.getQuote')
    def test_get_specific_stock(self, mock_getQuote):
        # Mock the getQuote function to return a sample stock quote
        mock_getQuote.return_value = {
            'symbol': 'AAPL',
            'price': 120.50,
            'change': 1.25,
            'changePercent': 1.05,
            'volume': 1000000
        }

        # Test the GET '/stock/{stock_symbol}' endpoint
        response = self.client.get('/stocks/stock/AAPL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_getQuote.return_value)

if __name__ == '__main__':
    unittest.main()
