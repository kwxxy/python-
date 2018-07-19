import os
import time
import requests
import asyncio
import aiohttp
from lxml import etree
from selenium import webdriver


class Spider(object):
    def __init__(self):
        if '图片' not in os.listdir('.'):
            os.mkdir('图片')
        self.path = os.path.join(os.path.abspath('.'), '图片')
        os.chdir(self.path)
        self.num = 1
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.llq = webdriver.Chrome(chrome_options=chrome_options)


    async def __get_content(self, link):
        async with aiohttp.ClientSession() as session:
            contents = []
            for i in range(len(link)):
                response = await session.get(link[i])
                content = await response.read()
                contents.append(content)
            return contents

    def __start_source(self, url):
        self.llq.get(url)
        response = self.llq.page_source
        return etree.HTML(response)

    def __get_img_links(self, page):
        url = 'http://jandan.net/ooxx/page-{}#comments'.format(page)
        html = self.__start_source(url)
        urls_titles = html.xpath('//ol//li//div[@class="text"]')
        url_tit = []
        for url_title in urls_titles:
            urls = url_title.xpath('p//img//@src')
            titles = url_title.xpath('span[@class="righttext"]/a/text()')
            url_tit.append(list(zip(titles, [urls])))
        return url_tit

    async def __download_img(self, img):
        contents = await self.__get_content(img[0][1])
        for i in range(len(contents)):
            with open(img[0][0] + '{}.jpg'.format(i), 'wb') as f:
                f.write(contents[i])
                print('下载第 %s 张图片完成 ' % self.num)
                self.num += 1

    def run(self):
        start = time.time()
        for i in range(1, 49):
            links = self.__get_img_links(i)
            tasks = [asyncio.ensure_future(self.__download_img(link)) for link in links]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()
        print("共花费 %s 秒" % (end - start))


def main():


    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()




