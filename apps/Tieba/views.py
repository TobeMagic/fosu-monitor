from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from datetime import datetime
from .baidu_spider import async_collect_baidu
import logging

logger = logging.getLogger(__name__)

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def baidu_task():
    print("[Apscheduler][Task](贴吧)--{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
    print('贴吧爬取任务开始')
    async_collect_baidu()


try:
    scheduler.add_job(baidu_task, trigger='interval', hours=10, id='贴吧', timezone='Asia/Shanghai',
                      replace_existing=True)

    logger.info("贴吧收集定时任务启动...")
    scheduler.start()

except Exception as e:
    logger.error(e)
    # scheduler.shutdown()
