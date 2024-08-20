import unittest
from unittest.mock import patch, MagicMock
import yfinance as yf
import psycopg2
from src.data_ingestion import save_data_to_db


class TestSaveToDB(unittest.TestCase):
    
    @patch('src.save_data.psycopg2.connect')
    def test_save_to_db(self, mock_connect):
        # Create fake connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        data = [{'symbol': 'NIO',  # Changed to match typical symbol case
                 'open': 150,
                 'high': 155,
                 'low': 149,
                 'close': 154,
                 'volume': 1000
        }]
        
        # Sample data 
        db_config = {
            'dbname': 'stock_prices_db',
            'user': 'lado',
            'password': 'first_go',
            'host': 'localhost',
            'port': '5432'
        }
        
        try:
            # Function to save data
            save_data_to_db(data, db_config)
            
            # Check connection and cursor were used correctly
            mock_connect.assert_called_once_with(
                dbname='stock_prices_db',
                user='lado',
                password='first_go',
                host='localhost',
                port='5432'
            )
            
            mock_cursor.execute.assert_called()
            
        except Exception as e:
            self.fail(f"save_data_to_db failed: {e}")
                
if __name__ == '__main__':
    unittest.main()
