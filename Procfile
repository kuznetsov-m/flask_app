web: flask db upgrade; gunicorn flask_app:app
worker: rq worker flask_app-tasks