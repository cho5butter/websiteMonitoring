from tokenize import String
from unittest import expectedFailure
from charset_normalizer import detect
from dotenv import load_dotenv
import os
import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from bs4 import BeautifulSoup
import requests
from sympy import true
import yaml
import difflib

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

    list_file_path = "target_pages_sample.yaml"

    if os.getenv('MONI_FILEPATH'):
        list_file_path = os.getenv('MONI_FILEPATH')
    
    with open(list_file_path, 'r') as yml:
        config = yaml.safe_load(yml)

    detectUpdates = []

    os.makedirs('dist/', exist_ok=True)

    for url in config['Url']:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        body = soup.find('body')
        title = soup.find('title').text
        stringBody = str(body).replace(' ', '').replace('\n', '').replace('　', '').replace(' ','').replace('\r','')
        curl = 'dist/' + url.replace(':', '').replace('/', '').replace('.', '').replace('~', '')
        try:
            with open(curl) as f:
                reader = f.read()
            if (stringBody != reader):
                print('更新検知')
                res = difflib.context_diff(stringBody, reader)
                diff = {"title": title, "url": url}
                detectUpdates.append(diff)
        except FileNotFoundError:
            print("Generate File")
        writer = open(curl, 'w')
        writer.write(stringBody)
        writer.close()

    if not detectUpdates:
        print('更新はありませんでした')
        exit()

    msg = MIMEMultipart()
    msg['Subject'] = config['Mail']['Subject']
    msg['From'] = config['Mail']['From']
    msg['To'] = config['Mail']['To']
    print(','.join(config['Mail']['Bcc']))
    msg['Bcc'] = ','.join(config['Mail']['Bcc'])



    # from_email = os.environ['MONI_FROM']

    # # メール送信先
    # to_email = os.environ['MONI_TO']

    # subject = "メール件名"
    # message = "メール本文"
    # mime = createMIMEText(from_email, to_email, message, subject)
    # send_email(mime)