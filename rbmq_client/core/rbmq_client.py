
import threading
import os
import sys

import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
from core import rbmq_rpc_method


'''
与sel服务器端对应的客户端,使用threading实现并发上传和下载文件的功能。
为了与threading搭配使用，把socket用另外一个类muilt_socket_client实现。


'''

user_data = {
    'account_id':None,
    'is_authenticated':True,
    'current_dir':None,
    'account_data':None
}




class RBMQClient(object):
    '''
    RBMQClient，主要作用：
    1.处理客户端的交互界面。
    2.设定客户端的各种命令。包括以下：
        interactive，与用户进行交互，
        help，命令帮助菜单。
        cmd_run，发送rpc命令到远程主机。。
        cmd_check_task，通过task_id取回命令的返回结果。。


    '''
    def __init__(self):
        '''
        host_list,后端主机的ip。
        task_dic，通过一个字典，把task_id与发送该消息的对象联系起来。

        '''
        self.host_list=settings.server_list
        self.task_dic={}
        pass
    def help(self):
        '''
        打印帮助信息的函数。
        '''
        msg = '''
使用方法：

>>:run "df -h" --hosts h1 h2 h3
task id :4533
>>:check_task 4533
bye
        '''
        print(msg)



    def cmd_check_task(self,*args):
        '''
        到RBMQ服务器上取回服务器端的命令返回结果。
        通过调用rpc_obj实例的comsume_res方法来取回。
            传入参数：
                task_id,消息的关联代码。
            返回参数：
                response，命令的返回结果。

        示例命令：check_task 4533
        :param args:
        :return:
        '''
        cmd_split = args[0].split()
        if len(cmd_split) >1:
            task_id=cmd_split[1]
            rpc_obj=self.task_dic[task_id]
            response=rpc_obj.comsume_res()
            print(response)
            # self.task_dic.pop[task_id]



        else:
            self.help()





    def cmd_run(self,*args):
        '''
        发送rpc命令到后端各主机列表。
        可以指明1个或者多个主机。
        命令的发送通过调用RbmqRpcClient类来实现。
            传入参数：
                cmd_name，需要在远程主机上运行的命令。
                h_name，后端各主机的ip地址。
            返回参数：
                返回task_id,用于标识本地发送的命令的关联码。

        实例命令：run "df -h" --hosts h1 h2 h3
        :param args:参数列表。
        :return:
        '''
        cmd_split = args[0].split()
        if '--hosts' in cmd_split:

            cmd_name=args[0].split('\"')[1]
            cmd_host=args[0].split('hosts ')[-1].split()
            read_host_list=[]
            for i in cmd_host:
                read_host_list.append(self.host_list[i])
            for h_name in read_host_list:
                send_cmd_rpc = rbmq_rpc_method.RbmqRpcClient(cmd_name,h_name)
                task_id=send_cmd_rpc.call()[0:4]
                self.task_dic[task_id]=send_cmd_rpc
            print("Task ID is:",self.task_dic.keys())




        else:
            self.help()







    def interactive(self):
        '''
        交互函数
        获取用户输入的命令字符串。
        通过反射获取对应的实例方法。
        然后运行该实例方法。把命令字符串交给该实例方法。

        '''
        print("你好，欢迎进入Crazy Rabbit_MQ RPC sys，请输入你的命令。。")
        while user_data['is_authenticated'] is True:
            cmd = input(">>").strip()
            if len(cmd) ==0:continue
            cmd_str = cmd.split()[0]
            if hasattr(self,"cmd_%s" % cmd_str):
                func = getattr(self,"cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()#运行帮助文档。











