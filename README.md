# Email Sender

Gmail (yoki boshqa SMTP) orqali email yuborish uchun kichik dastur. Ham terminaldan, ham oddiy oyna (tkinter) orqali ishlaydi.

## O'rnatish

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Sozlash

`.env` faylga o'z ma'lumotlaringizni yozing:

```
SMTP_USER=sizning@gmail.com
SMTP_PASSWORD=app parol
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=Ismingiz
```

Gmail uchun oddiy parol emas, **App Password** kerak bo'ladi:
Google Account → Security → App passwords.

## Ishlatish

Oyna (GUI):

```bash
python3 gui.py
```

Terminaldan:

```bash
python3 email_sender.py --to "kimdir@gmail.com" --subject "Salom" --body "Xabar matni"
```

Argumentsiz ishga tushirsangiz, o'zi so'rab boradi:

```bash
python3 email_sender.py
```

## Eslatma

`.env` ichida login/parol bor, shuning uchun uni hech qayerga commit qilmang (`.gitignore` da turibdi).
