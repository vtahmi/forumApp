from celery import shared_task
import time


@shared_task
def add(x, y):
    return x + y


@shared_task
def slow_task():
    time.sleep(10)
    return "Task finished successfully"

