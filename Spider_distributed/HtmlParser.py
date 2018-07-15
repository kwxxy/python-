from urllib.parse import urljoin
from lxml import etree

class HtmlParser(object):
    def parser(self, page_url, html_context):
        """
        用于解析网页内容，抽取 url 和数据
        :param page_url: 下载页面的 url
        :param html_context: 下载的网页内容
        :return: 返回 url 和数据
        """
        if page_url is None or html_context is None:
            return
        soup = etree.HTML(html_context)
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        """
        抽取新的 url 集合
        :param page_url: 下载页面的 url
        :param soup:
        :return:  返回新的 url 集合
        """
        new_urls = set()

        # 抽取符合要求的 a 标签
        links = soup.xpath('//div[@class="main-content"]//a[@target="_blank"]')              #find('div', class_='lemma-summary')

        for link in links:
            try:
                # 提取 href 属性
                new_url = link.xpath('@href')[0]
                # 拼接完整地址
                new_full_url = urljoin(page_url, new_url)
                if "item" in new_full_url:
                    new_urls.add(new_full_url)
                    print(new_full_url)
            except:
                continue
        return new_urls

    def _get_new_data(self, page_url, soup):
        """
        抽取有效的数据
        :param page_url:
        :param soup:
        :return:
        """
        data = {}
        data['url'] = page_url
        title = soup.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')                  #find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title
        summary = soup.xpath('//div[@class="para"]/text()')                           #find('div', class_='lemma-summary')
        data['summary'] = summary
        return data


