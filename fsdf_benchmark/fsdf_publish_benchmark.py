# import gevent.monkey;gevent.monkey.patch_all()
import time
from fsdf_benchmark.fsdf_consume_benchmark import task_fun

task_fun.clear()

for i in range(100000):
    if i == 0:
        print(time.strftime("%H:%M:%S"), '发布第一条')
    if i == 99999:
        print(time.strftime("%H:%M:%S"), '发布第100000条')
    task_fun.push(i)