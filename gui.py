
import os
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).parent
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass  


FONT_FAMILY = "Google Sans"
FONT        = (FONT_FAMILY, 12)
FONT_BOLD   = (FONT_FAMILY, 12, "bold")
FONT_TITLE  = (FONT_FAMILY, 20, "bold")
FONT_SMALL  = (FONT_FAMILY, 10)


BG       = "#f5f6f8"
CARD     = "#ffffff"
ACCENT   = "#1a73e8"
ACCENT_H = "#1765cc"
TEXT     = "#202124"
MUTED    = "#5f6368"
BORDER   = "#dadce0"
OK_CLR   = "#188038"
ERR_CLR  = "#d93025"



def send_email(host, port, user, password, sender_name, to, subject, body, html=False):
    """Email yuboradi. Xato bo'lsa Exception ko'taradi."""
    from_display = f"{sender_name} <{user}>" if sender_name else user

    msg = MIMEMultipart()
    msg["From"]    = from_display
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if html else "plain", "utf-8"))

    recipients = [r.strip() for r in to.split(",") if r.strip()]

    with smtplib.SMTP(host, int(port), timeout=20) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, recipients, msg.as_string())

    return recipients



class EmailSenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Sender")
        self.configure(bg=BG)
        self.geometry("680x720")
        self.minsize(560, 640)

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=CARD)
        style.configure("Bg.TFrame", background=BG)
        style.configure("TLabel", background=CARD, foreground=TEXT, font=FONT)
        style.configure("Muted.TLabel", background=CARD, foreground=MUTED, font=FONT_SMALL)
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=FONT_TITLE)
        style.configure("Sub.TLabel", background=BG, foreground=MUTED, font=FONT_SMALL)

        style.configure("TEntry", fieldbackground="#ffffff", bordercolor=BORDER,
                        relief="flat", padding=8, font=FONT)
        style.configure("TCheckbutton", background=CARD, foreground=TEXT, font=FONT)

        style.configure("Accent.TButton", background=ACCENT, foreground="#ffffff",
                        font=FONT_BOLD, borderwidth=0, focuscolor=ACCENT, padding=(20, 12))
        style.map("Accent.TButton",
                  background=[("active", ACCENT_H), ("disabled", "#a9c7f5")])

    def _build_ui(self):
       
        header = ttk.Frame(self, style="Bg.TFrame")
        header.pack(fill="x", padx=24, pady=(22, 8))
        ttk.Label(header, text="Email Sender", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="SMTP orqali e-mail yuborish",
                  style="Sub.TLabel").pack(anchor="w", pady=(2, 0))

        # Karta
        card = ttk.Frame(self, style="TFrame")
        card.pack(fill="both", expand=True, padx=24, pady=(8, 16))
        card.columnconfigure(0, weight=1)

        pad = {"padx": 20}

        
        self.var_user = tk.StringVar(value=os.getenv("SMTP_USER", os.getenv("EMAIL", "")))
        self.var_pass = tk.StringVar(value=os.getenv("SMTP_PASSWORD", os.getenv("PASSWORD", "")))
        self.var_host = tk.StringVar(value=os.getenv("SMTP_HOST", "smtp.gmail.com"))
        self.var_port = tk.StringVar(value=os.getenv("SMTP_PORT", "587"))
        self.var_name = tk.StringVar(value=os.getenv("SENDER_NAME", ""))

        row = 0
        ttk.Label(card, text="Account (SMTP user)").grid(row=row, column=0, sticky="w", pady=(20, 4), **pad)
        row += 1
        self.e_user = ttk.Entry(card, textvariable=self.var_user)
        self.e_user.grid(row=row, column=0, sticky="ew", **pad)
        row += 1

        
        ttk.Label(card, text="App parol").grid(row=row, column=0, sticky="w", pady=(14, 4), **pad)
        row += 1
        pass_wrap = ttk.Frame(card, style="TFrame")
        pass_wrap.grid(row=row, column=0, sticky="ew", **pad)
        pass_wrap.columnconfigure(0, weight=1)
        self.e_pass = ttk.Entry(pass_wrap, textvariable=self.var_pass, show="•")
        self.e_pass.grid(row=0, column=0, sticky="ew")
        self.show_pass = tk.BooleanVar(value=False)
        ttk.Checkbutton(pass_wrap, text="Ko'rsatish", variable=self.show_pass,
                        command=self._toggle_pass).grid(row=0, column=1, padx=(10, 0))
        row += 1

        
        ttk.Label(card, text="SMTP host / port / yuboruvchi nomi").grid(
            row=row, column=0, sticky="w", pady=(14, 4), **pad)
        row += 1
        hp = ttk.Frame(card, style="TFrame")
        hp.grid(row=row, column=0, sticky="ew", **pad)
        hp.columnconfigure(0, weight=3)
        hp.columnconfigure(1, weight=1)
        hp.columnconfigure(2, weight=2)
        ttk.Entry(hp, textvariable=self.var_host).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Entry(hp, textvariable=self.var_port, width=7).grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ttk.Entry(hp, textvariable=self.var_name).grid(row=0, column=2, sticky="ew")
        row += 1

        ttk.Separator(card, orient="horizontal").grid(
            row=row, column=0, sticky="ew", pady=18, **pad)
        row += 1

    
        ttk.Label(card, text="Kimga (To)").grid(row=row, column=0, sticky="w", pady=(0, 4), **pad)
        row += 1
        self.var_to = tk.StringVar()
        ttk.Entry(card, textvariable=self.var_to).grid(row=row, column=0, sticky="ew", **pad)
        row += 1
        ttk.Label(card, text="Bir nechta manzilni vergul bilan ajrating",
                  style="Muted.TLabel").grid(row=row, column=0, sticky="w", padx=20, pady=(3, 0))
        row += 1

       
        ttk.Label(card, text="Mavzu").grid(row=row, column=0, sticky="w", pady=(14, 4), **pad)
        row += 1
        self.var_subject = tk.StringVar()
        ttk.Entry(card, textvariable=self.var_subject).grid(row=row, column=0, sticky="ew", **pad)
        row += 1

        # Xabar matni
        head = ttk.Frame(card, style="TFrame")
        head.grid(row=row, column=0, sticky="ew", pady=(14, 4), **pad)
        head.columnconfigure(0, weight=1)
        ttk.Label(head, text="Xabar").grid(row=0, column=0, sticky="w")
        self.html_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(head, text="HTML format", variable=self.html_var).grid(row=0, column=1, sticky="e")
        row += 1

        card.rowconfigure(row, weight=1)
        self.txt_body = tk.Text(card, height=8, wrap="word", font=FONT,
                                relief="solid", borderwidth=1, padx=10, pady=10,
                                highlightthickness=1, highlightbackground=BORDER,
                                highlightcolor=ACCENT)
        self.txt_body.grid(row=row, column=0, sticky="nsew", padx=20)
        row += 1

        
        bottom = ttk.Frame(card, style="TFrame")
        bottom.grid(row=row, column=0, sticky="ew", padx=20, pady=16)
        bottom.columnconfigure(0, weight=1)

        self.status = ttk.Label(bottom, text="", style="Muted.TLabel")
        self.status.grid(row=0, column=0, sticky="w")

        self.send_btn = ttk.Button(bottom, text="Yuborish →",
                                   style="Accent.TButton", command=self._on_send)
        self.send_btn.grid(row=0, column=1, sticky="e")

    
    def _toggle_pass(self):
        self.e_pass.config(show="" if self.show_pass.get() else "•")

    def _set_status(self, text, color=MUTED):
        self.status.config(text=text, foreground=color)

    def _on_send(self):
        user = self.var_user.get().strip()
        password = self.var_pass.get().strip()
        host = self.var_host.get().strip()
        port = self.var_port.get().strip()
        name = self.var_name.get().strip()
        to = self.var_to.get().strip()
        subject = self.var_subject.get().strip()
        body = self.txt_body.get("1.0", "end").strip()
        html = self.html_var.get()

        
        if not user or not password:
            messagebox.showwarning("Maydon bo'sh", "Hisob va parolni kiriting.")
            return
        if not to:
            messagebox.showwarning("Maydon bo'sh", "'Kimga' maydonini to'ldiring.")
            return
        if not body:
            if not messagebox.askyesno("Bo'sh xabar", "Xabar matni bo'sh. Baribir yuboraymi?"):
                return

        self.send_btn.config(state="disabled")
        self._set_status("Yuborilmoqda…", MUTED)

        threading.Thread(
            target=self._send_worker,
            args=(host, port, user, password, name, to, subject, body, html),
            daemon=True,
        ).start()

    def _send_worker(self, host, port, user, password, name, to, subject, body, html):
        try:
            recipients = send_email(host, port, user, password, name, to, subject, body, html)
            self.after(0, self._on_success, recipients)
        except smtplib.SMTPAuthenticationError:
            self.after(0, self._on_error,
                       "Login yoki parol noto'g'ri. Gmail uchun App Password ishlating.")
        except smtplib.SMTPException as e:
            self.after(0, self._on_error, f"SMTP xatosi: {e}")
        except OSError as e:
            self.after(0, self._on_error, f"Tarmoq xatosi: {e}")
        except Exception as e:
            self.after(0, self._on_error, f"Xato: {e}")

    def _on_success(self, recipients):
        self.send_btn.config(state="normal")
        self._set_status(f"✓  Yuborildi → {', '.join(recipients)}", OK_CLR)

    def _on_error(self, message):
        self.send_btn.config(state="normal")
        self._set_status("✕  Yuborilmadi", ERR_CLR)
        messagebox.showerror("Xato", message)


if __name__ == "__main__":
    EmailSenderApp().mainloop()
