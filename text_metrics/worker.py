from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost', include=['text_metrics.modules.tasks'])

if __name__ == '__main__':
    app.start()
