#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from apscheduler.scheduler import Scheduler
from tbbt_trans_crawler import crawl_tbbt

sched = Scheduler()

@sched.cron_schedule(day_of_week='mon-sun', hour=5)
def scheduled_job():
    print 'This job is run every day at 5am.'

sched.start()

while True:
    pass