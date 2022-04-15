from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# oauth
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

# # oAuth Setup
# from authlib.integrations.flask_client import OAuth

# oauth = OAuth(app)
# google = oauth.register(
#     name='google',
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
# )

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
# Если пользователь, который не выполнил вход в систему, пытается просмотреть защищенную страницу, Flask-Login автоматически перенаправляет пользователя в форму для входа и только после завершения процесса входа в систем перенаправляет на страницу, которую пользователь хотел просмотреть.
# Flask-Login должен знать, что такое функция просмотра, которая обрабатывает логины.
# Значение «login» выше является именем функции (или конечной точки) для входа в систему.
login.login_view = 'login'

from app import routes, models, errors