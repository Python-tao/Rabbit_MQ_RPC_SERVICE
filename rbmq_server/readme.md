# 主题：rbmq_server

需求：
    基于Rabbit_MQ服务的用于向客户端响应RPC命令的服务端程序，支持向不同Rabbit_MQ队列接收
    命令，在本地执行完命令后，把命令返回结果发送到指定的Rabbit_MQ队列。





# 使用的模块
```
    pika，  与Rabbit_MQ服务器连接的模块。
    uuid    生成一个随机的id。
    
```


# 目录结构
```
- bin 
    -run_server.py          程序启动入口
- conf
    -settinggs.py           全局配置文件，保存了Rabbit_MQ服务器的ip地址,当前服务器的ip。   
-core                        核心代码
    -main.py                主函数.
    -rbmq_server.py         客户端的几个主功能函数。
    -rbmq_rpc_method.py     调用pika模块与Rabbit_MQ服务器进行交互的引擎。
readme.md                   readme文件
```