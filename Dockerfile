FROM python:3.9.12-buster

RUN adduser user

WORKDIR /home/flask_app

############################
# poetry
ENV POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /home/flask_app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
############################
# project files

COPY app app
COPY migrations migrations
COPY flask_app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flask_app.py

RUN chown -R user:user ./

############################

USER user

EXPOSE 5000

CMD [ "./boot.sh" ]