import os
import sys
from celery import Celery
from auto_worklab_chrome import auto_laudo
from analyze_covid import analyze_csv
import time
import pandas as pd

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def start_auto_laudo(self,table_name):
    table = analyze_csv(table_name)
    table[0]["Result"] = "POSITIVO"
    table[1]["Result"] = "NEGATIVO"
    table[2]["Result"] = "INCONCLUSIVO"

    table = pd.concat([table[0], table[1], table[2]]).sort_values(by="Sample")
    auto_laudo(table, validate=True)