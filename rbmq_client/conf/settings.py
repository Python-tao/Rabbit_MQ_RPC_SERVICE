# __author__ = "XYT"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
全局配置文件
    mq_server_host，Rabbit_MQ服务器的ip。
    server_list，后端各个主机的列表。

'''


rbmq_client_conf = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'mq_server_host':'192.168.88.128',
    'server_host': 'localhost',
    'server_port': 9999,

}

server_list={
    'h1':'192.168.88.128',
    'h2':'192.168.88.129',
    'h3':'192.168.88.130',
}

