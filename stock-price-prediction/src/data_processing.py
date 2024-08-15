import pandas as pd
import psycopg2 

def process_data_func(db_config: dict, processed_path: str):
    try:
        conn = psycopg2.connect(**db_config)
        df = pd.read_sql_query('SELECT * FROM prices', conn)
        df = df.dropna()
        df['date'] = pd.to_dateitime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month

        df.to_csv(processed_path, index = False)
        conn.close()

        print(f"Processed data saved to {processed_path}")
    except Exception as e:
        print(f"Data processing failed: {e}")


def main():
    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'lado',
        'password': 'first_go',
        'host': 'localhost',
        'port': '5432'
    }

    processed_path = '/Users/ladipo/Desktop/Stock_Price/stock-price-prediction/data'

    process_data_func(db_config, processed_path)

    if __name__ == "__main__":
        main()