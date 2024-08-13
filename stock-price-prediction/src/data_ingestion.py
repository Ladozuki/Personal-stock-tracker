import pandas as pd 
from datetime import datetime
import yfinance as yf
import psycopg2



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
                               INSERT INTO prices (symbol, date, open, high,
                               low, close, volume )
                               VALUES (%s, %s, %s, %s, %s, %s, %s)
                               ON CONFLICT (symbol, date) DO NOTHING ''', (
                                   symbol,
                                date.strftime('%Y-%m-%d'),
                                row['Open'],
                                row['High'],
                                row['Low'],
                                row['Close'],
                                row['Volume']
                               ))
        conn.commit()
        conn.close()
        print(f"Data saved to PostgreSQL")
    except Exception as e:
        print(f"Failed to save data: {e}")


def main():
    symbols = ["NIO", "BYDDF", "MANU", "F"]

    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'lado',
        'password': 'first_go',
        'host': 'localhost',
        'port': '5432'
    }

    data = fetch_stock_prices(symbols)
    if data:
        save_to_db(data, db_config)


if __name__ == "__main__":
    main()


            





