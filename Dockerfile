FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5739568300:AAEfr1V8gMIgVR0MHCb3TIHK7U3TGwTXdyQ"
#ENV TELEGRAM_ACCESS_ID=""

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]

