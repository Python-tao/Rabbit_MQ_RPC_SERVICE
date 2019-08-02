import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from core import rbmq_server
from conf import settings

'''
主函数，生成了RBMQServer类的实例rpc，运行了实例rpc的交互函数interactive()。

'''

def run():

    rpc = rbmq_server.RBMQServer()
    rpc.interactive()

