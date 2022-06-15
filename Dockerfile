FROM python:3
USER root

WORKDIR /home/

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN pip3 install charset-normalizer
RUN pip3 install python-dotenv
RUN pip3 install beautifulsoup4
RUN pip3 install requests
RUN pip3 install sympy
RUN pip3 install pyyaml

CMD ["python3", "run.py"]