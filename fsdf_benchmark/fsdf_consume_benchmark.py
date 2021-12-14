import gevent.monkey;gevent.monkey.patch_all()
import time
from function_scheduling_distributed_framework import task_deco,BrokerEnum,ConcurrentModeEnum

@task_deco('dssf_benchmark',broker_kind=BrokerEnum.REDIS,log_level=20,concurrent_mode=ConcurrentModeEnum.GEVENT,)
def task_fun(x):
    if x == 0:
        print(time.strftime("%H:%M:%S"),'消费第一条')
    if x == 99999:
        print(time.strftime("%H:%M:%S"),'消费第100000条')

if __name__ == '__main__':
    # task_fun.consume()
    task_fun.multi_process_consume(10)
