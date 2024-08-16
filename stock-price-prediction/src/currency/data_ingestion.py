import pandas as pd 
from datetime import datetime
import yfinance as yf
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

def fetch_currency_data(symbols: list) -> pd.DataFrame:
    data = {}
    
    for symbol in symbols:
        currency_pair = yf.Ticker(symbol)
        hist = currency_pair.history(period= "1d")
        data[symbol] = hist

    return data


def save_currdb(data, db_config: dict):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency_prices (
                id SERIAL PRIMARY KEY,
                symbol VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                UNIQUE (symbol, date)
            )
        ''')

        # Iterate over the data and insert it into the table
        for symbol, df in data.items():
            for date, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO currency_prices (symbol, date, open, high, low, close)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (symbol, date) DO NOTHING
                ''', (
                    symbol,
                    date.strftime('%Y-%m-%d'),
                    float(row['Open']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Close']),
                ))

        conn.commit()

    except Exception as e:
        print(f"Failed to save data: {e}")

        conn.commit()
        logging.info("Data saved to PostgreSQL")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
    finally:
        if conn:
            conn.close()

def main():
    currency_pairs = ['USDNGN=X', 'GBPNGN=X']
    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'postgres',
        'password': 'first_go',
        'host': 'localhost',
        'port': '5432'
    }

    data = fetch_currency_data(currency_pairs)
    save_currdb(data, db_config)

if __name__ == "__main__":
    main()

