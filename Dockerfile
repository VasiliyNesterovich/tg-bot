FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="5680178586:AAF9_dsWvDyel2tfUg8dq_QI30x6Mrfl2s4"
#ENV TELEGRAM_ACCESS_ID=""

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]

