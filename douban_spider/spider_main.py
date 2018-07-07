# coding=utf-8
from url_manager import UrlManager
from html_downloader import HtmlDownloader
from html_parser import HtmlParser
from html_outputer import HtmlOutputer
import exceptions
# multi-thread
from threading import Thread, Event
from Queue import Queue


class DownloadThread(Thread):
    def __init__(self, url, queue):
        Thread.__init__(self)
        self.url = url
        self.downloader = HtmlDownloader()
        self.queue = queue

    def download(self, url):
        return self.downloader.download(url)

    def run(self):
        html_cont = self.download(self.url)
        self.queue.put((self.url, html_cont))
        print 'Download...%s' % self.url


class HandleThread(Thread):
    def __init__(self, url_manager, dqueue, hqueue, event):
        Thread.__init__(self)
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()
        self.url_manager = url_manager
        self.dqueue = dqueue
        self.hqueue = hqueue
        self.event = event

    def handle(self, page_url, html_cont):
        new_urls, new_data = self.parser.parse(page_url, html_cont)
        self.url_manager.add_new_urls(new_urls)
        self.outputer.collect_data(new_data)

    def run(self):
        count = 1
        while True:
            try:
                page_url, html_cont = self.dqueue.get()
                # if page_url == 'finished':
                #     break
                if not self.url_manager.has_new_url():
                    self.handle(page_url, html_cont)
                    if self.url_manager.has_new_url():
                        self.event.set()
                else:
                    self.handle(page_url, html_cont)

                print 'handle %d successful' % count
                if count == 10:
                    self.hqueue.put('finished')
                    self.outputer.output_excel()
                    break
                self.hqueue.put('continue')
                count += 1
            except exceptions as e:
                print 'handle fail for ', e


if __name__ == '__main__':
    root_url = 'https://movie.douban.com/subject/1292052/'  # No.1
    url_manager = UrlManager()

    dq = Queue()
    hq = Queue()
    event = Event()

    url_manager.add_new_url(root_url)

    ht = HandleThread(url_manager, dq, hq, event)
    ht.start()

    while url_manager.has_new_url():
        new_url = url_manager.get_new_url()
        dt = DownloadThread(new_url, dq)
        dt.start()
        if not url_manager.has_new_url():
            event.wait(timeout=10)
        if hq.get() == 'finished':
            break

# 总结：多个download线程下载，一个handle线程处理
# d1->h1->d2->h2

# h wait d
# d2 wait h
# h2 wait d2
# d3 wait d2

# 此时不止将download和handle放在不同的线程中失去了意义，连download的多线程都无法实现，多线程实质上没有生效
# 如果想通过创建多个download线程实现并行下载，应该尽量不在循环创建线程的调度程序中加入Queue.get(), 如果队列中没有数据，会等待
# 也应该尽量不在调度程序中加入Event.wait(), 它会阻塞程序的运行，导致无法顺畅地循环生成download线程，从而导致并行下载无法实现

# download依赖handle生产的url, handle依赖download生产的html_cont, 这种相互依赖的模式不适用于多个生产者（多个download线程），
# 一个消费者（handle线程）的模型
