import os
import sys
sys.path.insert(1, "../")

import pandas as pd
from celery import Celery
from flask_app.scripts.auto_worklab_chrome import auto_laudo
import time

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def start_auto_laudo(self,result_table, chromedriver_path):
    time.sleep(60)
    return "Done"
    #auto_laudo(result_table, chromedriver_path, headless=False, validate=True)