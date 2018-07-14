from firstSpider.data_output import DataOutput
from firstSpider.html_parser import HtmlParser
from firstSpider.download_html import HtmlDownloader
from firstSpider.url_manager import URLManager


class SpiderMan(object):
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口 url
        self.manager.add_new_url(root_url)
        # 判断 url 管理器中是否有新的 url ，同时判断抓取了多少个 url
        while self.manager.has_new_url() and self.manager.old_url_size() < 100:
            try:
                # 从 url 管理器中获取新的 url
                new_url = self.manager.get_new_url()
                # HTML 下载器下载网页
                html = self.downloader.download(new_url)
                # HTML 解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                # 将抽取的 url 添加到 url 管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储到文件
                self.output.store_data(data)
                print("已经抓取 %s 个链接" % self.manager.old_url_size())
                # 数据存储器见文件输出为指定格式
                self.output.output_html()
            except:
                print("crawl failed")






