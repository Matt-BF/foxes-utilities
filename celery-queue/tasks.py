import os
import sys
from celery import Celery
from auto_worklab_chrome import auto_laudo
from analyze_covid import analyze_csv
import time
import chromedriver_binary

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def start_auto_laudo(self,table_name):
    table = analyze_csv(table_name)
    auto_laudo(table, headless=False, validate=True)