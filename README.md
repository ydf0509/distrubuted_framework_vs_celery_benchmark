# 测试分布式函数调度框架和celery的性能对比

```
测试方式为最严谨的控制变量法测试。
使用celery 和 function_scheduling_distributed_framework，分别测试发布10万条任务和消费10万条任务

不变的因素是  在代码本机安装的 redis + gevent 并发模型 + 执行最简单的 print + 相同cpu型号主频的机器 消费任务函数。
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


## 关于说celery每分钟执行百万次的反驳
```
从上面可以看到使用极其简单无意义的print 消息的函数作为消费函数，消费10万条任务，
耗时137秒，平均每秒celery能执行极限是700次，这是极限了。

如果celery的配置是设置为结果保存到redis并且开启消费成功后确认消费这两项配置，那么每秒执行次数还会降低到不足500。
task_ignore_result = False
task_reject_on_worker_lost = True #配置这两项可以随意停止
task_acks_late = True
```

```
即使按照实际生产线上的函数也是极其简单无意义的 print一下消息而已（可以肯定生产上实际情况下的消费函数远比print一个消息要复杂和耗cpu），
那么按照极限的700秒每次计算，消费100万条消息单核需要1400秒。那么假设你电脑是8核的，开启8个进程把cpu实用率用光
(要想8核都持续最高频运行，cpu需要使用每隔5秒注射液氮进行制冷散热，否则会降频，
8核火力全开的性能一般不会超过单核性能的8倍，例如因特尔是单核睿频5ghz，全核睿频只能3.8ghz且不可长时间持续)
那么在8核的机器上，至少需要耗时1400/8 = 175秒。在核和机器上执行最简单的 print 函数，也需要3分钟，那么即使是16核，也别想1分钟能运行100万次。

实际生产任务，如果发了一次requests直接请求本机nginx端口(直接请求本机nginx不转发到接口服务，排除了网速和服务端瓶颈，nginx可以支持万qps的)，
那么celery每秒执行次数远远达不到200次。所以说每分钟能执行100万次生产任务的人，他一定至少有10台8核以上的机器，而且消费函数里面的逻辑不能比对本机nginx发一次requests更复杂。
否则这人一定没精确测试过celery执行效率只是信口开河人云亦云。

```