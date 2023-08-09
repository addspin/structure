from celery import Celery

app = Celery('task', broker='redis://localhost:6379/0')

if __name__ == '__main__':
    app.start()