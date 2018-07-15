import time
from multiprocessing.managers import BaseManager
from client.HtmlParser import HtmlParser
from client.HtmlDownload import HtmlDownloader


class SpiderWork(object):
    def __init__(self):
        # 初始化分布式进程中工作节点的连接工作
        # 第一步 ： 使用 BaseManager 注册用于获取 Queue 的方法名称

        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        # 第二步 ： 连接到服务器
        server_adde = '127.0.0.1'
        print('Connect to server %s ....' % server_adde)

        self.m = BaseManager(address=('127.0.0.1', 6969), authkey=b'666')
        # 从网络连接
        self.m.connect()

        # 第三步 ： 获取 Queue 对象
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()

        # 初始化网页下载器，解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作')
                        # 接着通知其他节点停止工作
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print('爬虫节点正在解析：%s' % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls": new_urls, "data": data})


            except EOFError:
                print('连接工作节点失败')
                return
            except Exception:
                print(Exception)
                print('Crawl fali')
            finally:
                time.sleep(1)


if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()

















