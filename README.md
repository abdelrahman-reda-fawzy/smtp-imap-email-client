# SMTP–IMAP Email Client

## Overview

This project implements a simple email client using Python. The application allows users to send emails and retrieve emails from their inbox using standard email protocols.

SMTP (Simple Mail Transfer Protocol) is used to send emails, while IMAP (Internet Message Access Protocol) is used to retrieve emails from the mail server.

The application can send an email to a recipient and retrieve the latest email from the inbox, displaying the sender, subject, and message body.

## How to Install and Run the Application

Follow the steps below to install and run the application.

### 1. Clone the Repository

First, clone the GitHub repository:

```bash
git clone https://github.com/abdelrahman-reda-fawzy/smtp-imap-email-client.git
```

### 2. Install Dependencies

Install the required library used for desktop notifications:

```bash
pip install plyer
```

### 3. Run the Application

Run the main program:

```bash
python main.py
```

## Application Usage

### 1. Login Page

When the application starts, a login page appears where the user must enter:

- Email address
- Email password

### 2. Dashboard

After logging in, the dashboard appears. The user can choose between two options:

- Send Email
- Check Inbox

### 3. Send Email

If the user selects **Send Email**, they must enter:

- Recipient email address
- Email subject
- Email body

The application then sends the email using the SMTP protocol.

### 4. Check Inbox

If the user selects **Check Inbox**, the application retrieves the latest email from the inbox using IMAP.

The user receives a notification showing:

- Email sender
- Email subject

The body of the latest email is also displayed inside the application.

## Important Note for Gmail Users

If you are using a Gmail account, you must enable Two-Factor Authentication (2FA) and create an App Password. Gmail does not allow applications to log in using the normal account password.

Follow these steps:

1. Enable Two-Factor Authentication (2FA) on your Google account.
2. Go to your Google Account settings.
3. Open the **Security** section.
4. Select **App Passwords**.
5. Generate a new App Password for the application.
6. Use the generated App Password in the application instead of your normal Gmail password.
