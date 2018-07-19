import os
import time
import asyncio
import requests
import aiohttp
from lxml import etree
from multiprocessing import Pool


class Spider(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        self.num = 1
        if '图片2' not in os.listdir('.'):
            os.mkdir('图片2')
        self.path = os.path.join(os.path.abspath('.'), '图片2')
        os.chdir(self.path)


    def download(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        return html

    def get_one_url(self, url):
        response = self.download(url)
        urls = response.xpath('//li[@class="wp-item"]//h3/a/@href')
        return urls

    def get_two_url(self, url):
        response = self.download(url)
        urls = response.xpath('//div[@id="picture"]//p//img/@src')
        return urls

    # def get_url(self, url):
    #     response = self.download(url)
    #
    #     if 'html' in url:
    #         response = self.download(url)
    #         urls = response.xpath('//li[@class="wp-item"]//h3/a/@href')
    #         return urls
    #     response = self.download(url)
    #     urls = response.xpath('//div[@id="picture"]//p//img/@src')
    #     return urls



    async def _get_img(self, url):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self.headers)
            content = await response.read()

            return content

    async def _download_img(self, img):
        content = await self._get_img(img)
        title = img.replace('/', '_').split('a_')[1]
        with open('data{}'.format(title), 'wb') as f:
            f.write(content)
            self.num += 1
            print('下载第 %s 张图片完成 ' % self.num)

    def run(self, url):

        urls = self.get_one_url(url)
        for url in urls:
            links = self.get_two_url(url)
            tasks = [asyncio.ensure_future(self._download_img(link)) for link in links]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))



def main():
    spider = Spider()
    start = time.time()
    pool = Pool(3)
    for i in range(73):
        url = 'http://www.meizitu.com/a/more_{}.html'.format(i)
        res = pool.apply_async(func=spider.run, args=(url, ))
    pool.close()
    pool.join()
    end = time.time()
    print("共花费 %s 秒" % (end - start))

if __name__ == '__main__':
    main()

