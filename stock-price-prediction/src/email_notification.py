import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

def send_email(subject, body, to_email):

    try:

        #Validate email
        valid = validate_email(to_email)
        to_email = valid.email
        

        #Email account credentials
        from_email = "armandomassimo@yahoo.com"
        password = "bhmwociuihyptzby"

        #Create the message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        #Attach message body
        msg.attach(MIMEText(body, 'plain'))

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
    subject = "Test Email"
    body = "The prices of interest are detailed below"
    to_email = "armandomassimo@yahoo.com"

    send_email(subject, body, to_email)


if __name__ == "__main__":
    main()