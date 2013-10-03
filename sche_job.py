#!/usr/bin/env python
#coding=utf-8

import schedule
import subprocess
import time


def job():
    output = subprocess.call('python manage.py crawler', shell=True)
    print output

schedule.every().day.at("23:30").do(job)
#schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(600) # secs
