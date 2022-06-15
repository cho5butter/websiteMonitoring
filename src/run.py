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
import smtplib

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
            print("ファイル生成中")
        writer = open(curl, 'w')
        writer.write(stringBody)
        writer.close()

    if not detectUpdates:
        print('更新はありませんでした')
        exit()
    
    message = config['Mail']['Header']
    for index, update in enumerate(detectUpdates):
        message += str(index + 1) + ' - ' + update['title'] + '\n'
        message += '    ' + update['url'] + '\n\n'
    message += config['Mail']['Footer']

    msg = MIMEMultipart()
    msg['Subject'] = config['Mail']['Subject']
    msg['From'] = config['Mail']['From']
    msg['To'] = config['Mail']['To']
    msg['Bcc'] = ','.join(config['Mail']['Bcc'])
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    account = config['Mail']['Account']
    password = config['Mail']['Password']
    host = config['Mail']['Smtp']
    port = config['Mail']['Port']

    server = smtplib.SMTP(host, port)
    server.login(account, password)
    server.send_message(msg)
    server.quit()