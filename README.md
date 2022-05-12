# О проекте
## Заметки
- Используется самореферентные отношения (self-referential relationship) «многие ко многим» для отслеживания подписчиков.
- `flask-moment` (Moment.js) - для решения задачи отображения даты и времени в нужной time zone для пользователя на клиенте
- Полнотекстовый поиск на основе `elasticsearch`

## Стек технологий
- Flask (pytho web framework)
- Poetry (python packaging and dependency manager)
- postgreSQL (database)
- Elasticsearch (search engine)
- Gunicorn (HTTP server)
- Heroku (web hosting)
- Docker (container virtualization)

### elasticsearch
Весь код, который взаимодействует с индексом Elasticsearch в модуле app/search.py.
Идея состоит в том, чтобы сохранить весь код Elasticsearch в этом модуле. Остальная часть приложения будет использовать функции в этом новом модуле для доступа к индексу и не будет иметь прямого доступа к Elasticsearch. Это важно, потому что если однажды я решу, что мне больше не нравится Elasticsearch и соберусь переключиться на другой движок, все, что мне нужно сделать, это перезаписать функции в этом одном модуле, и приложение будет продолжать работать по-прежнему.

# Настройка приложения (переменные окружения)
Общие настройки:
```
SECRET_KEY=""
FLASK_ENV="development" / "production"
APP_SETTINGS="config.DevelopmentConfig" / "config.ProductionConfig"
FLASK_DEBUG= "1" / "0"
```

БД:
```
DATABASE_URL="postgresql://localhost/flask_app"
```

Для получения сообщений о сбоях на email:
```
MAIL_SERVER="smtp.googlemail.com"
MAIL_PORT="587"
MAIL_USE_TLS="1"
MAIL_USERNAME="email@gmail.com"
MAIL_PASSWORD="pass"
```

Elasticsearch
```
ELASTICSEARCH_URL=http://localhost:9200
```

# deployment
[Готовый образ в Docker Hub](https://hub.docker.com/repository/docker/kuznetsov1024/flask_app)

## Docker
Развертывание контейнера:   
```
# Создание образа
docker build -t flask_app:latest .

# Создание и запук контейнера
# --name <name>                создать контейнер с именем
# -d                           фоновый режим
# -p                           проброс порта
# -e <VAR_NAME>=<VAR_VALUE>    задать переменную окружения
# название образа
docker run --name flask_app_container -d -p 8000:5000 -e SECRET_KEY="1234" -e APP_SETTINGS="config.DevelopmentConfig" -e FLASK_DEBUG="1" -e  flask_app:latest
```
Логи flask_app приложения
```
# docker logs <container_name>
docker logs flask_app_flask_app_1
```

### docker-compose
```
docker-compose up --build -d
```
Для подключения к БД, например, для отладки:
```
docker exec -it flask_app_db_1 bash

psql -U postgres
```

# Остальное
- для добавления в индекс elasticsearch. Выполнить `Posts.reindex()`. Возможно перед этим потребуется вручную создать индекс `post`.
- Для работы через `flask shell` нужно определить в виртуальном окружении `FLASK_APP=flask_app.py`
- psql. для запроса данных из таблицы пользователей нужно взять название таблицы в "": `select * from "user";`
Без кавычек получится запрос к таблице с пользователями postgres.
## Cсылки
[Flask курс](https://habr.com/ru/post/346306/)
[elasticsearch docker-compose official doc](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
[elasticsearch docker-compose](https://levelup.gitconnected.com/docker-compose-made-easy-with-elasticsearch-and-kibana-4cb4110a80dd)
[flask + postgres docker-compose](https://levelup.gitconnected.com/dockerizing-a-flask-application-with-a-postgres-database-b5e5bfc24848)