FROM python:3.11-slim-bookworm

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get dist-upgrade

RUN apt-get -y install gcc

RUN apt install -y default-libmysqlclient-dev

RUN pip install -r requirements.txt

CMD ["python3", "entrypoint.py"]