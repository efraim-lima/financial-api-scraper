import unittest
from app.src.client import getQuote
from app.api.stock import getStock

class TestGetStock(unittest.TestCase):

    def test_valid_stock_symbol(self):
        """Test that getStock returns correct symbol and quote for a valid stock_symbol."""
        symbol, quote = getStock('AAPL')
        self.assertEqual(symbol, 'AAPL')
        self.assertIsInstance(quote, dict)
        self.assertTrue('symbol' in quote)
        self.assertTrue('price' in quote)

    def test_invalid_stock_symbol(self):
        """Test that getStock returns an error for an invalid stock_symbol."""
        with self.assertRaises(Exception) as context:
            getStock('INVALID')
        self.assertTrue(str(context.exception).startswith('Missing "stock_symbol" parameter'))

    def test_non_standard_quote_format(self):
        """Test that getStock returns an error for a non-standard quote format."""
        with self.assertRaises(Exception) as context:
            getQuote('AAPL', non_standard_format=True)
        self.assertTrue(str(context.exception).startswith('Invalid stock symbol'))

    def test_cache_hit(self):
        """Test that getStock returns cached data for a valid stock_symbol."""
        # Assuming that getQuote returns cached data for the first request
        symbol, cached_quote = getQuote('AAPL')
        cached_data = json.dumps(cached_quote)
        redis_conn.set(symbol, cached_data, ex=30)
        symbol, quote = getStock(symbol)
        self.assertEqual(cached_quote, quote)

    def test_cache_miss(self):
        """Test that getStock fetches data from external source if not cached."""
        # Assuming that getQuote returns cached data for the first request
        symbol, cached_quote = getQuote('AAPL')
        cached_data = json.dumps(cached_quote)
        redis_conn.set(symbol, cached_data, ex=30)
        redis_conn.delete(symbol)
        symbol, quote = getStock(symbol)
        # Assuming that getQuote fetches data from external source if not cached
        self.assertNotEqual(cached_quote, quote)


if __name__ == '__main__':
    unittest.main()
