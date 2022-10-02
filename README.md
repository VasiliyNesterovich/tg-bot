В переменных окружения надо проставить API токен бота.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile, а также в команде запуска укажите локальную директорию с проектом вместо `local_project_path`. SQLite база данных будет лежать в папке проекта `db/finance.db`.

```
docker build -t tg ./
docker run -d --name tg -v /local_project_path/db:/home/db tg
```

Чтобы войти в работающий контейнер:

```
docker exec -ti tg bash
```

Войти в контейнере в SQL шелл:

```
docker exec -ti tg bash
sqlite3 /home/db/finance.db
```