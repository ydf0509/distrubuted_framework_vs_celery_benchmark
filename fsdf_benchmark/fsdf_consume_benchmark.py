import gevent.monkey;gevent.monkey.patch_all()
import time
from function_scheduling_distributed_framework import task_deco,BrokerEnum,run_consumer_with_multi_process,ConcurrentModeEnum

@task_deco('dssf_benchmark',broker_kind=BrokerEnum.REDIS,qps=0,log_level=20,concurrent_mode=ConcurrentModeEnum.GEVENT,create_logger_file=True)
def task_fun(x):
    if x == 0:
        print(time.strftime("%H:%M:%S"),'消费第一条')
    if x == 99999:
        print(time.strftime("%H:%M:%S"),'消费第100000条')

if __name__ == '__main__':
    task_fun.consume()
    # run_consumer_with_multi_process(f,1)