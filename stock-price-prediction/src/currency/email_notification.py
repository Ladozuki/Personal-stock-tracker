from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError
import smtplib
from datetime import datetime 
from sqlalchemy import create_engine
import pandas as pd

def fetch_currency_data(db_config: dict) -> pd.DataFrame:

    try: 

        connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

        engine = create_engine(connection_string)
    
    #    conn = psycopg2.connect(**db_config)
        df = pd.read_sql_query('SELECT symbol AS pair, date, open, high, low FROM currency_prices', engine)

        engine.dispose()
     
     #   conn.close()

    except Exception as e:
        print(f"Failed to fetch data: {e}")

        return pd.DataFrame() #returns empty dataframe on failure
    return df

def generate_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data available"
    
    html = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th>Stock Symbol</th>
                <th>Date</th>
                <th>Open Price</th>
                <th>High </th>
                <th>Low </th
            </tr>
        </thead>
        <tbody>
    """
    
    
    # Add rows to HTML table
    for index, row in df.iterrows():
        html += f"""
        <tr>
            <td>{row['pair']}</td>
            <td>{row['date']}</td>
            <td>{row['open']:.2f}</td>
            <td>{row['high']:.2f}</td>
            <td>{row['low']:.2f}</td>
        </tr>
        """
    
    # End HTML table
    html += """
        </tbody>
    </table>
    """
    
    return html


def send_email(subject: str, body: str, email_config: dict) -> None:

    msg = EmailMessage()
    msg['Subject'] = 'Daily Currency Update'
    msg['From'] = email_config['from']
    msg['To'] = email_config['to']


    msg.set_content(body, subtype = 'html')

    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
            server.login(email_config['from'], email_config['password'])
            server.send_message(msg)

        print('Email sent successfully!')
    except Exception as e:
        print(f"Failed to send email: {e}")
    except EmailNotValidError as e:
        print(f"Invalid email address: {e}")
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your username and password.")
    except smtplib.SMTPConnectError:
        print("SMTP Connect Error: Unable to connect to the email server.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")


def main():
    currency_pairs = ['USDNGN=X', 'GBPNGN=X']


    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'postgres',
        'password':'first_go',
        'host': 'localhost',
        'port': '5432'
    }
    
    df = fetch_currency_data(db_config)

    table_string = generate_table(df)
    today_date = datetime.now().strftime('%d-%m-%Y')
    
    body = f"""
    <html>
    <body>
        <p>Hi there,</p>
        <p>Here is your currency update for today, {today_date}.</p>
        {table_string}
        <p>For more detailed information and historical data, visit: <a href="http://example.com/your-web-interface">Your Web Interface</a></p>
        <p>This email is for informational purposes only .</p>
        <p><br>Labdvi</p>
    </body>
    </html>
    """

    email_config = {
        'from': 'armandomassimo@yahoo.com',
        'to': 'oo16774@alumni.bristol.ac.uk',
        'password': 'soxrjhiefcjpjqjg'

    }

    subject = f"Daily Currency Update - {today_date}"

    send_email(subject, body, email_config)

if __name__ == "__main__":
    main()







    


    



