#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import urlparse
import multiprocessing
import cPickle
from Queue import Queue
from threading import Thread,RLock
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko)'}
domainlink = 'http://www.87fuli.com'

def contgo(func):
    def doctors(*args,**kwargs):
        count = 5
        while True:
            try:
                return func(*args,**kwargs)
            except Exception as e:
                count -= 1
                if not count:
                    return None
    return doctors

@contgo
def getmaxpage():
    url = 'http://www.87fuli.com/type/5.html'
    mainpage = requests.get(url,headers=headers,timeout = 5)
    mainpage.encoding = 'utf-8'
    a = int(BeautifulSoup(mainpage.content,"html.parser").find(name='div',attrs={'id':'page','class':'pages'}).find_all(name='span')[1].text.split(u'页')[0])
    return a

@contgo
def get_page_html(maxpage):
    mainurl = 'http://www.87fuli.com/type/5/'
    result = []
    for i in range(1,int(maxpage)+1):
        url = mainurl+str(i)+'.html'
        gopage = requests.get(url,headers = headers,timeout = 5)
        gopage.encoding = 'utf-8'
        page_a_link = BeautifulSoup(gopage.text,"html.parser").find_all(name='a',attrs={'class':'link-hover','href':True,'title':True})
        for iap in page_a_link:
            # result.append([domainlink+iap['href'],iap['title']])
            result.append([iap['href'], iap['title']])
            print iap['title'],iap['href']
    return result

@contgo
def get_true_link(url):
    pagehtml = requests.get(url,headers = headers,timeout = 5)
    pagehtml.encoding = 'utf-8'
    getlink = BeautifulSoup(pagehtml.text,"html.parser").find(name='iframe')['src']
    moviedomainlink = urlparse.urlparse(getlink).scheme +'://' + urlparse.urlparse(getlink).netloc
    a = requests.get(getlink,headers=headers,timeout = 5)
    link = BeautifulSoup(a.text,"html.parser").video['src']
    # endreq = requests.get(moviedomainlink+link,headers = headers,stream = True,timeout = 5)
    endreq = requests.get(link, headers=headers, stream=True, timeout=5)
    return endreq.url

@contgo
def get_avideo_url(url):
    pagehtml = requests.get(url,headers = headers,timeout = 5)
    pagehtml.encoding = 'utf-8'
    Flink = BeautifulSoup(pagehtml.text,"html.parser").find(name='div',attrs={'id':'stab81','class':'playlist clearfix'}).find_all(name='a')
    # result = [get_true_link(domainlink+ i['href']) for i in Flink]
    result = [get_true_link(i['href']) for i in Flink]
    return result

# get_avideo_url('http://www.87fuli.com/show/13936.html')
# print get_true_link('http://www.87fudd---li.com/play/1038/1/1.html')
# print get_avideo_url('http://www.87fuli.com/show/1038.html')
# exit()
def save_data(data,filename):
    with open(filename,'wb') as savfilename:
        cPickle.dump(data,savfilename)

def load_data(filename):
    with open(filename,'rb') as datafile:
        data = cPickle.load(datafile)
        return data

class thrun(object):
    def __init__(self,data):
        self.threanum = 10
        self.result = data
        self.queue = Queue()
        self.lockes = RLock()

    def getdata(self):
        while True:
            self.lockes.acquire()
            if self.queue.empty():
                break
            i = self.queue.get()
            self.lockes.release()

            self.result[i]['source'] = get_avideo_url(self.result[i]['introduce'])

    def run(self):
        for i in self.result:
            self.queue.put(i)
        allth = []
        for i in range(self.threanum):
            th = Thread(target=self.getdata)
            th.daemon = True
            th.start()
            allth.append(th)

        for i in allth:
            i.join()


if __name__ == '__main__':
    result = {}
    maxpage = getmaxpage()
    print u'共：',str(maxpage)+u'页'
    allvideo = get_page_html(maxpage)
    print u'获取所有电影链接'
    for i in range(len(allvideo)):
        trueurl = get_avideo_url(allvideo[i][0])
        print allvideo[i][1],allvideo[i][0],trueurl
        result[i] = {'title':allvideo[i][1],'introduce':allvideo[i][0],'source':trueurl}
    save_data(result,'log/87fuli')