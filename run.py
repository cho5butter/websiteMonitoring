from dotenv import load_dotenv
import os
import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from bs4 import BeautifulSoup
import requests
import yaml

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

def monitoring_pages():
    list_file_path = "target_pages_sample.yaml"

    if os.getenv('MONI_FILEPATH'):
        list_file_path = os.getenv('MONI_FILEPATH')

    print(list_file_path)

    with open(list_file_path, 'r') as yml:
        config = yaml.safe_load(yml)

    for url in config['Url']:
        print(url)
    
         

def analysis_html():
    load_url = "https://www.ymori.com/books/python2nen/test1.html"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    print(soup)

if __name__ == '__main__':
    load_dotenv()
    SMTP = os.environ['MONI_SMTP']
    print(SMTP)

    monitoring_pages()
    analysis_html()
    # from_email = os.environ['MONI_FROM']

    # # メール送信先
    # to_email = os.environ['MONI_TO']

    # subject = "メール件名"
    # message = "メール本文"
    # mime = createMIMEText(from_email, to_email, message, subject)
    # send_email(mime)