#Author:xyt

import threading
import os

import sys
import pika
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings


class RbmqRpcClient(object):
    '''
    RbmqRpcClient类，用于执行与RabbitMQ服务器连接的操作。
    主要的结构：
        __init__构建函数，
            用于创建socket实例，以及连接rbmq服务器端。
        call函数，用于往RBMQ服务器上的某个队列发送消息。。
        comsume_res函数和on_response，用于接收消息。

    '''
    def __init__(self,cmd_name,host_name):
        #Rabbit_mq服务器的ip。
        self.mq_server_host=settings.rbmq_client_conf['mq_server_host']
        #需要在后端主机上运行RPC命令的名称。
        self.cmd_name=cmd_name
        #需要发往哪个队列，此处用主机ip作为队列名称。
        self.queue_name=host_name
        #创建套接字连接rbmq服务器。
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
            host=self.mq_server_host))
        #实例化一条通道。
        self.channel = self.connection.channel()
        #生成临时队列，此队列用于接收服务器端返回的消息。
        result = self.channel.queue_declare('',exclusive=True)
        #获取临时队列的名称，
        self.callback_queue = result.method.queue
        #消费服务端返回的消息的方法。
        # self.channel.basic_consume(
        #     on_message_callback=self.on_response,
        #     auto_ack=True,
        #     queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()



    def call(self):
        self.response = None
        #生成关联码，用于把发送的命令和返回的结果关联起来。
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                       routing_key=self.queue_name,
                       properties=pika.BasicProperties(
                       reply_to=self.callback_queue,
                       correlation_id=self.corr_id,
                       ),body=str(self.cmd_name))
        return self.corr_id
        # while self.response is None:
        #     self.connection.process_data_events()#非阻塞版本的start consumeing
        # else:
        #     return self.response

    def comsume_res(self):
        #消费服务端返回的消息的方法。
        self.channel.basic_consume(
            on_message_callback=self.on_response,
            auto_ack=True,
            queue=self.callback_queue)

        while self.response is None:
            self.connection.process_data_events()  # 非阻塞版本的start consumeing
        else:
            return self.response


