from app import app, db
from app.models import User, Post

# позволяет настроить «shell context», который представляет собой список других имен для предварительного импорта
# создает контекст оболочки, который добавляет экземпляр и модели базы данных в сеанс оболочки
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}