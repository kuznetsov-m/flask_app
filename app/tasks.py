import json
import sys
import time

from app import create_app

from rq import get_current_job
from app import db
from app.models import User, Post, Task

app = create_app()
app.app_context().push()


# Установка хода выполнения задачи
def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification(
            'task_progress',
            {'task_id': job.get_id(), 'progress': progress}
        )
        if progress >= 100:
            task.complete = True
        db.session.commit()

def export_posts(user_id):
    try:
        # читать сообщения пользователей из базы данных
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)   # для отладки процесса
            i += 1
            _set_task_progress(100 * i // total_posts)

        # отправить письмо с данными пользователю
        # send_email('[flask_app] Your example app',
        #     sender=app.config['ADMINS'][0],
        #     recipients=[user.email],
        #     text_body=render_template('email/export_posts.txt', user=user),
        #     html_body=render_template('email/export_posts.html', user=user),
        #     attachments=[(
        #         'posts.json',
        #         'application/json',
        #         json.dumps({'posts': data}, indent=4)
        #     )],
        #     sync=True
        # )
        # временно результат будем выводить в консоль
        app.logger.info(json.dumps({'posts': data}, indent=2))
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
