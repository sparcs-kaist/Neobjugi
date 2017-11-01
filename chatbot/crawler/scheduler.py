import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from multiprocessing import Process, Queue
import time
from spiders import AraSpider

class AraCrawlBot(object):
    def __init__(self):
        self.results = []

    def addItem(self,item):
        self.results.append(item)

    def run(self):
        process = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': 'crawler/result.json'
        })
        process.crawl(AraSpider)
        for crawler in process.crawlers:
            crawler.signals.connect(self.addItem, signals.item_passed)
        process.start()
        for res in self.results:
            print(res)

def run_spiders():
    def f(q):
        try:
            bot = AraCrawlBot()
            bot.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


while True:
    run_spiders()
    time.sleep(1200)
