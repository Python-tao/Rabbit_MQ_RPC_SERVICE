# __author__ = "XYT"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
全局配置文件
    mq_server_host，Rabbit_mq服务器的ip
    local_queue_name，消息队列名称，此处用后端服务器的ip地址作为队列名称，不同的后端主机应该配置不同的ip地址

'''


rbmq_server_conf = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'mq_server_host':'192.168.88.128',
    'local_queue_name':'192.168.88.128',
    'server_host': 'localhost',
    'server_port': 9999,

}





