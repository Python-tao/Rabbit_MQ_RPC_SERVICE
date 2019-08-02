# 主题：rbmq_client

需求：
    基于Rabbit_MQ服务的用于向多个远程服务器发送RPC命令的客户端程序，提供命令行界面，支持向多个Rabbit_MQ队列发送
    命令，发送完命令后不等待命令的执行。
    后端个服务器接收队列中的命令后，在本地执行，并把执行结果返回给Rabbit_MQ。
    客户端运行check_task命令收取命令的执行结果。

#命令行格式
## run命令(已完成)
```
　　作用：向远程服务器发送RPC命令。
   格式：
        run "CMD_NAME" --hosts [HOST_LIST]
            "CMD_NAME",指明在RPC命令的名称。
            --hosts [HOST_LIST]，指明向哪些服务器发送rpc命令。
            
   示例：
        run "df -h" --hosts h1 h2 h3

```


## check_task命令(已完成)
```
    作用:
        向Rabbit_MQ收取RPC命令的执行结果。
    格式：
        check_task [RPM_CMD_ID]  
            [RPM_CMD_ID] ,指明要收取哪个RPC命令的返回结果。
           
    示例：
        check_task 4533   
```



# 使用的模块
```
    pika，  与Rabbit_MQ服务器连接的模块。
    uuid    生成一个随机的id。
    
```


# 目录结构
```
- bin 
    -run_client.py          程序启动入口
- conf
    -settinggs.py           全局配置文件，保存了Rabbit_MQ服务器的ip地址,后端各个主机的列表。   
-core                        核心代码
    -main.py                主函数.
    -rbmq_client.py         客户端的几个主功能函数。
    -rbmq_rpc_method.py     调用pika模块与Rabbit_MQ服务器进行交互的引擎。
readme.md                       readme文件
```