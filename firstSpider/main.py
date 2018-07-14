import os
import sys


dir_filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir_filename)
sys.path.append(dir_filename)

from firstSpider.Spider_main import SpiderMan

spider_main = SpiderMan()
spider_main.crawl("https://baike.baidu.com/view/284853.htm")