import unittest
from unittest.mock import patch, MagicMock
import yfinance as yf
import psycopg2
import pandas as pd
from src.data_ingestion import fetch_stock_prices, save_data_to_db

class TestFetchStockPrices(unittest.TestCase):
    
    @patch('src.fetch_data.yf.Ticker')
    def test_fetch_stock_prices_success(self, mock_ticker):
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = pd.DataFrame({
            'Open': [150],
            'High': [155],
            'Low': [149],
            'Close': [154],
            'Volume': [1000]
        }, index=pd.to_datetime(['2024-08-14']))
        mock_ticker.return_value = mock_ticker_instance

        data = fetch_stock_prices('AAPL')
        self.assertIsNotNone(data)
        self.assertIn('Open', data[0])
        self.assertEqual(data[0]['Open'], 150)

    @patch('src.fetch_data.yf.Ticker')
    def test_fetch_stock_prices_failure(self, mock_ticker):
        mock_ticker.side_effect = Exception("API error")

        data = fetch_stock_prices('AAPL')
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
