import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from core import rbmq_client
from conf import settings

'''
主函数，生成了RBMQClient类的实例r，运行了实例r的交互函数interactive()。

'''

def run():

    r = rbmq_client.RBMQClient()
    r.interactive()

