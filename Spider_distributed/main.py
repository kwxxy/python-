import os
import sys

from multiprocessing import Queue
from multiprocessing import freeze_support, Process

dir_filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_filename)

from Spider_distributed.Spider_main import NodeManager

if __name__ == '__main__':

    # 初始化 4 个队列
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()

    # 创建分布式管理器
    node = NodeManager()
    manager = node.Start_Manager(url_q, result_q)

    # 创建 url 管理进程，数据提取进程，数据存储进程
    url_manager = Process(target=node.url_manager_proc, args=(url_q, conn_q, 'https://baike.baidu.com/item/%E6%90%9C%E7%B4%A2%E7%AD%96%E7%95%A5'))
    result_solve = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q))
    store = Process(target=node.store_proc, args=(store_q, ))

    # 启动 3 个进程 和分布式管理器
    url_manager.start()
    result_solve.start()
    store.start()
    s = manager.get_server()
    s.serve_forever()