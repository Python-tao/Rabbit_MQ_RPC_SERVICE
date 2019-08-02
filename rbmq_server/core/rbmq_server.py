
import threading,socket
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
from core import rbmq_rpc_method


'''
在后端服务器上运行的服务端程序，用于接收发送过来的rpc命令，然后再本地运行，再把
运行的结果，返回到RBMQ服务器。


'''

user_data = {
    'account_id':None,
    'is_authenticated':True,
    'current_dir':None,
    'account_data':None
}




class RBMQServer(object):
    '''
    RBMQServer类，主要作用：
    1.从RMMQ服务器上收取RPC命令。
    2.在本地主机上运行该命令。
    3.把命令的执行结果返回给主机。
        interactive，仅为入口程序，调用RbmqRpcServer类。
        help,并无作用。




    '''
    def __init__(self):
        #RBMQ服务器的地址。
        self.mq_server_host=settings.rbmq_server_conf['mq_server_host']
        #本地主机对应的队列名称。
        self.local_queue_name=settings.rbmq_server_conf['local_queue_name']

    def help(self):
        '''
        打印帮助文档的函数。
        '''
        msg = '''
使用方法：

bye
        '''
        print(msg)




    def interactive(self):
        '''
        交互函数
        获取用户输入的命令字符串。
        通过反射获取对应的实例方法。
        然后运行该方法。把命令字符串交给该实例方法。

        '''
        print("你好，欢迎进入Crazy Rabbit_MQ RPC Server，正在接收命令。。。")
        while True:
            rpc_server=rbmq_rpc_method.RbmqRpcServer(self.mq_server_host,self.local_queue_name)
            rpc_server.start()













