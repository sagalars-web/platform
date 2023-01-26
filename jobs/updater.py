from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api
from .static_analysis import age_group_count, regional_distribution


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, 'cron', hour=23)
    scheduler.add_job(regional_distribution, 'cron', hour=5)
    scheduler.add_job(age_group_count, 'cron', hour=6)
    scheduler.start()
