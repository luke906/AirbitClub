from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date

import sys

import time

class Schedule_Manager():

    # 클래스 생성시 스케쥴러 데몬을 생성합니다.
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.block_sched = BlockingScheduler()

        self.job_id=''
        print("Schedule_Manager start")

    # 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
    def __del__(self):
        pass
        #self.shutdown()

    # 모든 job들을 종료시켜주는 함수입니다.
    def shutdown(self):
        print("stop all scheduler")
        self.sched.shutdown(wait=True)


    # 특정 job을 종료시켜줍니다.
    def kill_scheduler(self, job_id):
        try:
            print("stop scheduler: %s" % job_id)
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print("fail to stop scheduler: %s" % err)
            return

    def hello(self, type, job_id):
        print("%s scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

    def shutdown_schedule(self):
        self.sched.shutdown()


    # 스케쥴러입니다. 스케쥴러가 실행되면서 hello를 실행시키는 쓰레드가 생성되어집니다.
    # 그리고 다음 함수는 type 인수 값에 따라 cron과 interval 형식으로 지정할 수 있습니다.
    # 인수값이 cron일 경우, 날짜, 요일, 시간, 분, 초 등의 형식으로 지정하여,
    # 특정 시각에 실행되도록 합니다.(cron과 동일)
    # interval의 경우, 설정된 시간을 간격으로 일정하게 실행실행시킬 수 있습니다.
    def start_scheduler_interval(self, function, job_id, interval_time=5, args_value=None):

        #print("Scheduler Start")
        self.sched.add_job(function,
                         'interval',
              seconds=interval_time,
                          id=job_id,
                   args=[args_value])

        self.sched.start()

    def start_scheduler_cron(self, function, day_of_week, hour, minute, start_idex, end_index):

        # Runs from Monday to Friday at 5:30 (am) until 2014-05-30 00:00:00
        #sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')
        self.block_sched.add_job(function, 'cron', day_of_week=day_of_week, hour=hour, minute=minute, args=(start_idex, end_index))
        self.block_sched.start()
