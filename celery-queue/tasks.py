import os
import sys
sys.path.insert(1, "../")
from celery import Celery
print(sys.path())
from ..flask_app.scripts.auto_worklab_chrome import auto_laudo
from ..flask_app.scripts.analyze_covid import analyze_csv
import time

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def start_auto_laudo(self,table_name, chromedriver_path):
    table = analyze_csv(table_name)
    auto_laudo(table, chromedriver_path, headless=False, validate=True)