from dotenv import load_dotenv
import os

import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

def createMIMEText(from_email, to, message, subject, filename=""):
    # MIMETextを作成
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    return msg

def send_email(msg):
    account = os.environ['MONI_ACCOUNT']
    password = os.environ['MONI_PASS']

    host = os.environ['MONI_SMTP']
    port = os.environ['MONI_PORT']

    # サーバを指定する
    # server = SMTP(host, port)
    context = ssl.create_default_context()
    server = SMTP_SSL(host, port, context=context)

    # ログイン処理
    server.login(account, password)

    # メールを送信する
    server.send_message(msg)
    
    # 閉じる
    server.quit()

if __name__ == '__main__':
    load_dotenv()
    SMTP = os.environ['MONI_SMTP']
    print(SMTP)

    from_email = os.environ['MONI_FROM']

    # メール送信先
    to_email = os.environ['MONI_TO']

    subject = "メール件名"
    message = "メール本文"
    mime = createMIMEText(from_email, to_email, message, subject)
    send_email(mime)