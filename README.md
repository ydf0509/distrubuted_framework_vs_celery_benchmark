# 测试分布式函数调度框架和celery的性能对比

```
测试方式为最严谨的控制变量法测试。
使用celery 和 function_scheduling_distributed_framework，分别测试发布10万条任务和消费10万条任务

不变的因素是  在代码本机安装的 redis + gevent 并发模型 + 执行最简单的 print 消费任务函数。
变化的因素是  celery框架 和 function_scheduling_distributed_framework

```

## 测试方法
```
分别
1.1启动celery消费脚本 celery_benchmark/celery_publish_benchmark.py ，测试celery发布性能，
查看控制台的打印，第一条和最后一条的发布时间间隔

1.2启动celery 发布脚本 celery_benchmark/celery_consume_benchmark.py ，测试celery消费性能
查看控制台的打印，第一条和最后一条的消费时间间隔


2.1 启动 fsdf_benchmark/fsdf_publish_benchmark.py，测试分布式函数调度框架发布性能
查看控制台的打印，第一条和最后一条的发布时间间隔

启动 fsdf_benchmark/fsdf_consume_benchmark.py，测试分布式函数调度框架消费性能
查看控制台的打印，第一条和最后一条的消费时间间隔
```

## 测试结果
```
celery 发布10万条耗时 137秒。
celery 消费10万条耗时 350秒

function_scheduling_distributed_framework 发布10万条耗时7秒
function_scheduling_distributed_framework 消费10万条耗时12秒。
```

## 测试结论
```
在使 相同的redis中间件，相同的gevent并发模式 ，
分布式函数掉地框架发布性能超过celery近20倍
分布式函数掉地框架消费性能超过celery近30倍
```

## 造成具体性能差异原因，在分布式函数调度框架的readme已近说了。
