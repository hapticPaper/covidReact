from apscheduler.schedulers.blocking import BlockingScheduler
import os, requests, datetime
from frontend.db_loader.lite_loader import *

DB_PATH = 'frontend/data/db/'
DB_FILE = 'covid.sqlite'
os.makedirs(DB_PATH, exist_ok=True)


IMG_PATH = 'frontend/'

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=20)
def updateSqlite():
    results = fetchCountyData()
    print(f'results: {results[:2]}')
    getUsTotals()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')
updateSqlite()
sched.start()