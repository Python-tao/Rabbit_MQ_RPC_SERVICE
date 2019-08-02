#Author:xyt

import threading,socket
import os
import json
import sys
import pika
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings


class RbmqRpcServer(object):
    '''
    RbmqRpcServer类，用于与Rabbit MQ服务器连接的相关操作。
    主要的结构：
        __init__构建函数，用于创建socket实例，以及连接RBMQ服务器端。
        start，从MQ服务器上收消息。
        on_request，收到消息后运行此回调函数。
        cmd_run，在本地运行shell命令的函数。



    '''
    def __init__(self,mq_server_host,queue_name):
        #收消息的队列名称。
        self.queue_name=queue_name
        #创建socket连接RBMQ服务器。
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=mq_server_host))

        self.channel = connection.channel()
        # 声明队列，用于接收客户端发过来的消息。
        self.channel.queue_declare(queue=queue_name)

    def cmd_run(self,cmd_name):
        '''
        在本地主机上运行客户端发过来的命令。
        并且把命令的执行结果返回。
        :param cmd_name: 客户端发送过来的命令。
        :return:cmd_res,命令的执行结果。
        '''
        cmd_res = os.popen(cmd_name).read()
        return cmd_res


    #首次收到消息后的回调函数。
    def on_request(self,ch, method, props, body):
        '''
        1.在本地运行shell命令。
        2.把命令的返回结果，发送到RBMQ上的对应的队列中。
        :param ch: 与RBMQ建立的通道对象
        :param method: 收到的消息的相关信息。
        :param props: 收到的消息的相关自定义属性。
        :param body: 收到的消息的实际内容。
        :return:
        '''
        #收到的消息都是bytes格式，需要先解码。
        cmd_name = body.decode()
        print(" [.] Command Name is (%s)" % cmd_name)
        response =self.cmd_run(cmd_name)
        ch.basic_publish(exchange='',
          routing_key=props.reply_to,
          properties=pika.BasicProperties(
         correlation_id=props.correlation_id),
          body=response.encode())
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def start(self):

        self.channel.basic_qos(prefetch_count=1)#负载均衡。
         # 消费消息。
        self.channel.basic_consume(
             on_message_callback=self.on_request,
             queue=self.queue_name)
        print(" [x]正在等待RPC命令请求。。")
        self.channel.start_consuming()