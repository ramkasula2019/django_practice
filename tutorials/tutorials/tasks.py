from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379')

@app.task(track_started=True)
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

## task inheritance
import celery 
class MyTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@app.task(base=MyTask)
def add_inherit(x, y):
    raise KeyError()