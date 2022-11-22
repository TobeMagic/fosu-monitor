from django.shortcuts import render, HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from datetime import datetime
from . import weibo_spider
import logging

logger = logging.getLogger(__name__)
# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')


# 注册定时任务并开始
def weibo_task():
    # 具体要执行的代码
    print('[APScheduler][Task](微博)-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    print("微博爬取任务开始")
    weibo_spider.run()


try:
    scheduler.add_job(weibo_task, 'interval', hours=6, replace_existing=True, id="微博", timezone='Asia/Shanghai',
                      args=())

    logger.info("微博定时任务启动...")
    scheduler.start()

except Exception as e:
    logger.error(e)
    # scheduler2.shutdown()
