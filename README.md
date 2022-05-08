# О проекте
### Заметки
- Используется самореферентные отношения (self-referential relationship) «многие ко многим» для отслеживания подписчиков.
- `flask-moment` (Moment.js) - для решения задачи отображения даты и времени в нужной time zone для пользователя на клиенте
- Полнотекстовый поиск на основе `elasticsearch`


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
- добавить индекс в elasticsearch. Выполнить `Posts.reindex()`. Возможно перед этим потребуется вручную создать индекс `post`. 

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