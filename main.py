import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def send_mail(sender : str,
              password:str,
              receiver:str,
              subject:str,
              body:str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(sender,password)
        server.send_message(msg)
        print('Send email')


send_mail(
    sender="operator0171@gmail.com",
    password= "hbau lxwb hmnf ihbv",
    receiver="jasurmavloniy24@gmail.com",
    subject="Salom!",
    body="Bu EmailMessage orqali yuborilgan xabar."
)



'''
Subject : For Business TOpic
Sender : me
to = ['1@gmail',]
body = 'balbalblbalbl'
login , password
'''