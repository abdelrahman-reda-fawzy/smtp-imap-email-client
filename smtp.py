import smtplib
from email.mime.text import MIMEText

def send_email(
    smtp_server,
    username,
    password,
    receiver_email,
    subject,
    body,
    sender_email=None
):

    SMTP_PORT = 587

    if sender_email is None:
        sender_email = username

    try:
        # Create email message
        message = MIMEText(body, "plain")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Send email
        with smtplib.SMTP(smtp_server, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email or password.")

    except smtplib.SMTPConnectError:
        print("Error: Unable to connect to the SMTP server.")

    except smtplib.SMTPException as e:
        print("SMTP error occurred:", e)

    except Exception as e:
        print("An unexpected error occurred:", e)