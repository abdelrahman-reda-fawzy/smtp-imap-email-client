import tkinter as tk
from tkinter import ttk
from plyer import notification
import threading
import smtplib
import imaplib

from smtp import send_email
from imap import receive_latest_email


# -------------------
# WINDOW
# -------------------

root = tk.Tk()
root.title("Email Client")
root.geometry("780x700")
root.minsize(720, 640)
root.configure(bg="#0b1220")

FONT_TITLE = ("Segoe UI Semibold", 24)
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI Semibold", 10)
FONT_INPUT = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI Semibold", 11)

BG_COLOR = "#0b1220"
CARD_COLOR = "#131c2e"
PRIMARY = "#6366f1"
PRIMARY_HOVER = "#4f46e5"
SECONDARY = "#23304a"
SECONDARY_HOVER = "#2d3b59"
TEXT_COLOR = "#e2e8f0"
MUTED_TEXT = "#94a3b8"
FIELD_BG = "#0f172a"
FIELD_BORDER = "#24324b"


# -------------------
# VARIABLES
# -------------------

email_var = tk.StringVar()
password_var = tk.StringVar()

smtp_server = tk.StringVar(value="smtp.gmail.com")
imap_server = tk.StringVar(value="imap.gmail.com")

receiver_var = tk.StringVar()
subject_var = tk.StringVar()


style = ttk.Style()
style.theme_use("clam")
style.configure(
    "App.TEntry",
    fieldbackground=FIELD_BG,
    background=FIELD_BG,
    foreground=TEXT_COLOR,
    borderwidth=0,
    relief="flat",
    padding=12,
    insertcolor=TEXT_COLOR,
)


# -------------------
# UTILITIES
# -------------------

def clear():
    for w in root.winfo_children():
        w.destroy()


def card():
    shell = tk.Frame(
        root,
        bg=CARD_COLOR,
        highlightthickness=1,
        highlightbackground=FIELD_BORDER,
    )
    shell.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.84, relheight=0.86)

    frame = tk.Frame(shell, bg=CARD_COLOR, padx=42, pady=36)
    frame.pack(fill="both", expand=True)
    return frame


def rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command,
        width=260,
        height=52,
        bg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        text_color="white",
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.command = command
        self.default_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.shape = rounded_rectangle(
            self,
            2,
            2,
            width - 2,
            height - 2,
            22,
            fill=self.default_color,
            outline="",
        )
        self.label = self.create_text(
            width / 2,
            height / 2,
            text=text,
            fill=self.text_color,
            font=FONT_BUTTON,
        )

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, _event):
        self.command()

    def _on_enter(self, _event):
        self.itemconfig(self.shape, fill=self.hover_color)

    def _on_leave(self, _event):
        self.itemconfig(self.shape, fill=self.default_color)


def page_header(parent, title, subtitle):
    tk.Label(
        parent,
        text=title,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=FONT_TITLE,
    ).pack(anchor="w")
    tk.Label(
        parent,
        text=subtitle,
        bg=CARD_COLOR,
        fg=MUTED_TEXT,
        font=FONT_SUBTITLE,
    ).pack(anchor="w", pady=(6, 20))


def label(parent, text):
    tk.Label(
        parent,
        text=text,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=FONT_LABEL,
    ).pack(anchor="w", pady=(12, 6))


def entry(parent, var, show=None):
    e = ttk.Entry(parent, textvariable=var, font=FONT_INPUT, show=show, style="App.TEntry")
    e.pack(fill="x", ipady=8)
    return e


def primary_button(parent, text, cmd):
    b = RoundedButton(
        parent,
        text=text,
        command=cmd,
        width=320,
        height=54,
        bg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        text_color="white",
    )
    b.pack(pady=14)
    return b


def secondary_button(parent, text, cmd):
    b = RoundedButton(
        parent,
        text=text,
        command=cmd,
        width=220,
        height=50,
        bg_color=SECONDARY,
        hover_color=SECONDARY_HOVER,
        text_color=TEXT_COLOR,
    )
    b.pack(pady=(8, 0))
    return b


def text_area(parent, height):
    widget = tk.Text(
        parent,
        height=height,
        font=FONT_INPUT,
        bg=FIELD_BG,
        fg=TEXT_COLOR,
        relief="flat",
        bd=0,
        padx=14,
        pady=14,
        insertbackground=TEXT_COLOR,
        wrap="word",
    )
    widget.pack(fill="both", expand=True, pady=(0, 10))
    return widget


def infer_mail_servers(email_address):
    if "@" not in email_address:
        return None, None, "Enter a valid email address."

    domain = email_address.split("@", 1)[1].strip().lower()

    if domain in {"gmail.com", "googlemail.com"}:
        return "smtp.gmail.com", "imap.gmail.com", ""

    if domain in {"hotmail.com", "outlook.com", "live.com", "msn.com"}:
        return "smtp-mail.outlook.com", "outlook.office365.com", ""

    if domain in {"yahoo.com", "yahoo.co.uk", "yahoo.ca", "ymail.com"}:
        return "smtp.mail.yahoo.com", "imap.mail.yahoo.com", ""

    return None, None, f"Unsupported email domain: {domain}"


def authenticate_login(smtp_host, imap_host, username, password):
    if not username or not password:
        return False, "Email and password are required."

    try:
        with smtplib.SMTP(smtp_host, 587, timeout=12) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed. Check email or password."
    except smtplib.SMTPException:
        return False, "Unable to authenticate with SMTP server."
    except OSError:
        return False, "Cannot connect to SMTP server."

    try:
        with imaplib.IMAP4_SSL(imap_host, 993) as mail:
            mail.login(username, password)
            mail.logout()
    except imaplib.IMAP4.error:
        return False, "IMAP authentication failed. Check email or password."
    except OSError:
        return False, "Cannot connect to IMAP server."

    return True, "Login successful."


# -------------------
# LOGIN PAGE
# -------------------

def login_page():

    clear()
    frame = card()

    page_header(frame, "Email Client", "")

    label(frame,"Email")
    entry(frame,email_var)

    label(frame,"Password")
    entry(frame,password_var,"*")

    tk.Label(
        frame,
        text="",
        bg=CARD_COLOR,
        fg=MUTED_TEXT,
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    ).pack(fill="x", pady=(8, 2))

    login_status = tk.StringVar(value="")
    tk.Label(
        frame,
        textvariable=login_status,
        bg=CARD_COLOR,
        fg="#f87171",
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    ).pack(fill="x", pady=(8, 2))

    def login_action():
        smtp_host, imap_host, server_error = infer_mail_servers(email_var.get().strip())

        if server_error:
            login_status.set(server_error)
            return

        smtp_server.set(smtp_host)
        imap_server.set(imap_host)

        ok, message = authenticate_login(
            smtp_host,
            imap_host,
            email_var.get().strip(),
            password_var.get(),
        )

        if ok:
            login_status.set("")
            dashboard()
        else:
            login_status.set(message)

    primary_button(frame,"Login",login_action)


# -------------------
# DASHBOARD
# -------------------

def dashboard():

    clear()
    frame = card()

    page_header(frame, "Dashboard", "")

    primary_button(frame,"Send Email",send_page)
    primary_button(frame,"Check Inbox",inbox_page)

    secondary_button(frame,"Logout",login_page)


# -------------------
# SEND EMAIL PAGE
# -------------------

def send_page():

    clear()
    frame = card()

    page_header(frame, "Send Email", "")

    label(frame,"Recipient")
    entry(frame,receiver_var)

    label(frame,"Subject")
    entry(frame,subject_var)

    label(frame,"Body")

    body = tk.Text(
        frame,
        height=4,
        font=FONT_INPUT,
        bg=FIELD_BG,
        fg=TEXT_COLOR,
        relief="flat",
        bd=0,
        padx=14,
        pady=14,
        insertbackground=TEXT_COLOR,
        wrap="word",
    )
    body.pack(fill="x", pady=(0, 8))

    send_in_progress = False

    def send_action():
        nonlocal send_in_progress

        if send_in_progress:
            return

        send_in_progress = True
        send_email(
            smtp_server.get(),
            email_var.get(),
            password_var.get(),
            receiver_var.get(),
            subject_var.get(),
            body.get("1.0",tk.END)
        )
        root.after(1000, lambda: _reset_send_lock())

    def _reset_send_lock():
        nonlocal send_in_progress
        send_in_progress = False

    primary_button(frame, "Send Email", send_action)
    secondary_button(frame, "Back", dashboard)


# -------------------
# INBOX PAGE
# -------------------

def inbox_page():

    clear()
    frame = card()

    page_header(frame, "Latest Email", "")

    display = text_area(frame, 16)
    display.config(state="disabled")

    def load_email():

        subject,sender,body = receive_latest_email(
            imap_server.get(),
            email_var.get(),
            password_var.get()
        )

        if subject:

            display.config(state="normal")
            display.delete("1.0",tk.END)

            display.insert(tk.END,f"From: {sender}\n")
            display.insert(tk.END,f"Subject: {subject}\n\n")
            display.insert(tk.END,body)
            display.config(state="disabled")

            notification.notify(
                title=f"New Email from {sender}",
                message=subject,
                timeout=5
            )

    threading.Thread(target=load_email).start()

    primary_button(frame,"Refresh",lambda: threading.Thread(target=load_email).start())

    secondary_button(frame,"Back",dashboard)


# -------------------
# START
# -------------------

login_page()
root.mainloop()