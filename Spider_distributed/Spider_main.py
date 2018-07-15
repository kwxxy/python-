import time
import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support, Process
from Spider_distributed.URLManager import UrlManager
from Spider_distributed.DataOutPut import DataOutput




class NodeManager(object):

    def Start_Manager(self, url_q, result_q):
        """
        创建一个分布式管理器
        :param url_q: 队列
        :param result_q: 队列结果
        :return:
        """
        # 创建两个队列并放在网络上，利用 register 方法， callable 参数关联 queue 对象
        # 将 queue 对象放在网络中
        BaseManager.register('get_task_queue', callable=lambda : url_q)
        BaseManager.register('get_result_queue', callable=lambda :result_q)
        # 绑定端口，设置口令 ‘baike’，相当于对象初始化
        manager = BaseManager(address=('127.0.0.1', 6969), authkey=b'666')
        # 返回 manager 对象
        return manager


    def url_manager_proc(self, url_q, conn_q, root_url):

        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while url_manager.has_new_url():
                # 从 url 管理器获取新的 url
                new_url = url_manager.get_new_url()
                # 将新的 url 发送给工作节点
                url_q.put(new_url)
                print('old_url = ', url_manager.old_url_size())
                # 加一个判断条件，爬取 2000 个链接后就关闭，并保存进度
                if url_manager.old_url_size() > 20:
                    # 通知爬虫节点工作结束
                    url_q.put('end')
                    print('控制节点发起结束通知')
                    # 关闭管理节点，同时保存 set 状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
                # 将从 result_solve_proc 获取到的 url 添加到 url 管理器
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException :
                time.sleep(0.1)


    def result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get()
                    if content['new_urls'] == 'end':
                        # 分析进程 接收通知后结束
                        print('分析进程,接收通知后结束')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])    # url 为 set 类型
                    store_q.put(content['data'])        # 解析出来的数据为 dict 类型
                else:
                    time.sleep(0.1)
            except BaseException:
                time.sleep(0.1)


    def store_proc(self, store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程,接收通知后结束')
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)





