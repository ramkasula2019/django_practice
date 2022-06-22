from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379')

@app.task
def task_multiply(x, y):
    return x * y