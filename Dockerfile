FROM python:3.7-slim

ADD . /api

WORKDIR /api

RUN pip3 install -r requirements.txt

CMD ["python3","-u","api.py"]


