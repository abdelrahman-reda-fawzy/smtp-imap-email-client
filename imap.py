import imaplib
import email

def receive_latest_email(
    imap_server,
    username,
    password
):

    IMAP_PORT = 993

    try:
        # Connect to IMAP server
        with imaplib.IMAP4_SSL(imap_server, IMAP_PORT) as mail:
            mail.login(username, password)

            # Select inbox
            mail.select("inbox")

            # Search for all emails
            status, messages = mail.search(None, "ALL")

            email_ids = messages[0].split()

            if not email_ids:
                print("No emails found.")
                return None, None, None

            # Fetch latest email
            latest_email_id = email_ids[-1]
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

            # Parse email
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg["Subject"]
            sender = msg["From"]

            body = ""

            # Get email body
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            return subject, sender, body

    except imaplib.IMAP4.error:
        print("Error: Authentication failed. Check your email or password.")
        return None, None, None

    except ConnectionError:
        print("Error: Unable to connect to the IMAP server.")
        return None, None, None

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None, None, None