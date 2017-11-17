from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.blocking import BlockingScheduler

import time

class Schedule_Manager(object):

    # 클래스 생성시 스케쥴러 데몬을 생성합니다.
    def __init__(self):
        self.sched = BlockingScheduler()
        self.job_id=''

    # 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
    def __del__(self):
        self.shutdown()

    # 모든 job들을 종료시켜주는 함수입니다.
    def shutdown(self):
        print("stop all scheduler")
        self.sched.shutdown()


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

    # 스케쥴러입니다. 스케쥴러가 실행되면서 hello를 실행시키는 쓰레드가 생성되어집니다.
    # 그리고 다음 함수는 type 인수 값에 따라 cron과 interval 형식으로 지정할 수 있습니다.
    # 인수값이 cron일 경우, 날짜, 요일, 시간, 분, 초 등의 형식으로 지정하여,
    # 특정 시각에 실행되도록 합니다.(cron과 동일)
    # interval의 경우, 설정된 시간을 간격으로 일정하게 실행실행시킬 수 있습니다.
    def start_scheduler(self, function, type, job_id, interval_time=5, args_value=None, day_interval=None, hour=None, sec=None):

        #print("Scheduler Start")
        if type == 'interval':
            self.sched.add_job(function,
                                        type,
                                        seconds=interval_time,
                                        id=job_id,
                                        args=[args_value])
        elif type == 'cron':
            self.sched.add_job(function,
                                        type,
                                        day_of_week=day_interval,
                                        hour=hour,
                                        second=sec,
                                        id=job_id,
                                        args=[args_value])

        self.sched.start()
