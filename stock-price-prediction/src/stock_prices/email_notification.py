import smtplib #Library used to send emails using Simple Mail Transfer Protocol
from email_validator import validate_email, EmailNotValidError
from email.message import EmailMessage
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
from sqlalchemy import create_engine


def fetch_stock_data(db_config: dict) -> pd.DataFrame:

    try: 

        connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

        engine = create_engine(connection_string)
    
    #    conn = psycopg2.connect(**db_config)
        df = pd.read_sql_query('SELECT symbol, date, close, high, low FROM prices', engine)

        engine.dispose()
     
     #   conn.close()

    except Exception as e:
        print(f"Failed to fetch data: {e}")

        return pd.DataFrame() #returns empty dataframe on failure
    return df

    
    #convert DF to PrettyTable string
def generate_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data available"

    # today_date = datetime.now().strftime('%Y-%m-%d')
    # df_today = df[df['date'] == today_date]

      # Calculate yesterday's date
    # yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # df_yesterday = df[df['date'] == yesterday_date]


    # Round numerical columns to 2 decimal places
    # df_today = df_today.round({'close': 2, 'high': 2, 'low': 2})
    
    html = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th>Stock Symbol</th>
                <th>Date</th>
                <th>Close Price</th>
                <th>High Price</th>
                <th>Low Price</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Add rows to HTML table
    for index, row in df.iterrows():
        html += f"""
        <tr>
            <td>{row['symbol']}</td>
            <td>{row['date']}</td>
            <td>{row['close']:.2f}</td>
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



def send_email(subject: str, body: str, to_email: str) -> None:

    try:

        #Validate email
        valid = validate_email(to_email)
        to_email = valid.email
        

        #Email account credentials
        from_email = "armandomassimo@yahoo.com"
        password = "soxrjhiefcjpjqjg"

        #Create the message
        msg = EmailMessage()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject


        msg.set_content(body, subtype = 'html')

        
    #msg['From'] = email_config['from']
    #msg['To'] = email_config['to']

    # email_config = {
        #'from': 'your-email@yahoo.com',
    #     'password': 'your_password',
    #     'to': 'recipient@example.com'
    # }

        #Set up the server and send the email
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
            server.starttls()
            server.login(from_email, password) 
            server.send_message(msg)
            server.quit()

        print("Email sent succesfully!")

    except EmailNotValidError as e:
        print(f"Invalid email address: {e}")
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your username and password.")
    except smtplib.SMTPConnectError:
        print("SMTP Connect Error: Unable to connect to the email server.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def main():

    db_config = {
        'dbname': 'stock_prices_db',
        'user': 'postgres',
        'password': 'first_go',
        'host': 'localhost',
        'port': '5432'
    }

    df= fetch_stock_data(db_config)

    #Generate html table for today
    table_html = generate_table(df)

    today_date = datetime.now().strftime('%Y-%m-%d')
    subject = f"Daily Stock Update - {today_date}"
    to_email = "armandomassimo@yahoo.com"
    
    body = f"""
    <html>
    <body>
        <p>Hi there,</p>
        <p>Here is your stock update for today, {today_date}.</p>
        {table_html}
        <p>For more detailed information and historical data, visit: <a href="http://example.com/your-web-interface">Your Web Interface</a></p>
        <p>This email is for informational purposes only and does not constitute financial advice.</p>
        <p>Best regards,<br>Your Company</p>
    </body>
    </html>
    """

    send_email(subject, body, to_email)


if __name__ == "__main__":
    main()