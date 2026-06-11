"""
Email Sender — CLI versiya (.env + SMTP)
Ishlatish:
    python send_email.py
    python send_email.py --to "test@gmail.com" --subject "Salom" --body "Xabar matni"
"""

import os
import sys
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("XATO: python-dotenv o'rnatilmagan.")
    print("O'rnatish: pip install python-dotenv")
    sys.exit(1)

# .env yuklash
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = "hbau lxwb hmnf ihbv"
SENDER_NAME = os.getenv("SENDER_NAME", "")


def check_env():
    missing = [k for k, v in {
        "SMTP_USER": SMTP_USER,
        "SMTP_PASSWORD": SMTP_PASS,
    }.items() if not v]
    if missing:
        print(f"XATO: .env da quyidagilar topilmadi: {', '.join(missing)}")
        sys.exit(1)


def send(to: str, subject: str, body: str, html: bool = False):
    check_env()

    from_display = f"{SENDER_NAME} <{SMTP_USER}>" if SENDER_NAME else SMTP_USER

    msg = MIMEMultipart()
    msg["From"]    = from_display
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if html else "plain", "utf-8"))

    print(f"→  {SMTP_HOST}:{SMTP_PORT} ga ulanilmoqda...")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to.split(","), msg.as_string())

        print(f"✓  Yuborildi → {to}")

    except smtplib.SMTPAuthenticationError:
        print("XATO: Login/Parol noto'g'ri.")
        print("Gmail bo'lsa: Google Account → Security → App passwords")
        sys.exit(1)
    except smtplib.SMTPException as e:
        print(f"XATO (SMTP): {e}")
        sys.exit(1)
    except OSError as e:
        print(f"XATO (Tarmoq): {e}")
        sys.exit(1)


def interactive():
    """Argument berilmasa interaktiv so'raydi."""
    print("─── Email Sender ───")
    to      = input("Kimga (To)    : ").strip()
    subject = input("Mavzu         : ").strip()
    print("Xabar (Enter x2 tugallash):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    body = "\n".join(lines).strip()

    if not to:
        print("XATO: 'Kimga' maydoni bo'sh bo'lmasligi kerak.")
        sys.exit(1)

    send(to, subject, body)


def main():
    parser = argparse.ArgumentParser(description="CLI Email Sender")
    parser.add_argument("--to",      help="Qabul qiluvchi email")
    parser.add_argument("--subject", help="Mavzu", default="")
    parser.add_argument("--body",    help="Xabar matni", default="")
    parser.add_argument("--html",    action="store_true", help="HTML format")
    args = parser.parse_args()

    if args.to:
        send(args.to, args.subject, args.body, html=args.html)
    else:
        interactive()


if __name__ == "__main__":
    main()