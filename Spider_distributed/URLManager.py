import pickle
import hashlib


class UrlManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')  # 未爬取的 url 集合
        self.old_urls = self.load_progress('old_urls.txt')  # 爬取的 url 集合

    def has_new_url(self):
        """
        判断是否有未爬取的 url
        :return:
        """
        return self.new_url_size() != 0

    def get_new_url(self):
        """
        获取一个未爬取的 url
        :return:
        """
        new_url = self.new_urls.pop()

        # m = hashlib.md5()
        # m.update(new_url)
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        """
        将新的 url 添加到未爬取的 url 集合中
        :param url: 单个 url
        :return:
        """
        if url is None:
            return
        # m = hashlib.md5()
        # m.update(url.enocde('utf-8'))
        # url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """
        将新的 url 添加到未爬取的 url 集合中
        :param urls:
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):

        return len(self.new_urls)

    def old_url_size(self):

        return len(self.old_urls)

    def save_progress(self, path, data):
        """
        保存进度
        :param path: 文件路径
        :param data: 数据
        :return:
        """
        with open(path, 'wb', encoding='utf-8') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        """
        本地文件加载进度
        :param path:
        :return: 返回 set 集合
        """
        print('从文件加载进度： %s' % path)
        try:
            with open(path, 'rb', encoding='utf-8') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('无文件进度，创建： %s' % path)
        return set()


