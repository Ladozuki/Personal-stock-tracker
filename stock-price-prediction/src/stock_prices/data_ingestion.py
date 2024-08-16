import pandas as pd 
from datetime import datetime
import yfinance as yf
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

def fetch_stock_prices(symbols: list):
    data = {}
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        data[symbol] = hist
    return data

def save_to_db(data, db_config: dict):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume INTEGER,
            UNIQUE (symbol, date)
        )
        ''')
        for symbol, df in data.items():
            for date, row in df.iterrows():
                cursor.execute('''
                INSERT INTO prices (symbol, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, date) DO NOTHING
                ''', (
                    symbol,
                    date.strftime('%Y-%m-%d'),
                    float(row['Open']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Close']),
                   int( row['Volume'])
                ))
        conn.commit()
        logging.info("Data saved to PostgreSQL")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
    finally:
        if conn:
            conn.close()

def main():
    symbols = ["NIO", "BYDDF", "MANU", "F"]
    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'ladipo',
        'password': 'first_go',
        'host': 'localhost',
        'port': '5432'
    }

    data = fetch_stock_prices(symbols)
    if data:
        save_to_db(data, db_config)

if __name__ == "__main__":
    main()


            





