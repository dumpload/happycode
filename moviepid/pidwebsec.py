import requests
from bs4 import BeautifulSoup
import urlparse
import multiprocessing
import cPickle
from Queue import Queue
from threading import Thread,RLock

def contgo(func):
    def doctors(*args,**kwargs):
        count = 5
        while True:
            try:
                return func(*args,**kwargs)
            except Exception as e:
                print e
                count -= 1
                if not count:
                    return None
    return doctors

def save_data(data,filename):
    with open(filename,'wb') as savfilename:
        cPickle.dump(data,savfilename)

def load_data(filename):
    with open(filename,'rb') as datafile:
        data = cPickle.load(datafile)
        return data

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko)'}

@contgo
def getpageinfo(url):
    a = requests.get(url,headers=headers,timeout = 3)
    a.encoding = 'utf-8'
    result = BeautifulSoup(a.text,'html.parser').find(name='source',src = True)['src']
    print url,result
    return result


# print getpageinfo('http://www.websc.cc/f/2.php')
# exit()
a = load_data('log/websc')
for i in a:
    print i,a[i].values()
exit()

if __name__ == '__main__':
    result = {}
    idcount = 0
    for zimu in range(99, 123):
        for shuzi in range(1,100):
            url = 'http://www.websc.cc/%s/%s.php' % (chr(zimu),str(shuzi))
            link = getpageinfo(url)
            if link:
                result[idcount] = {'link':url,'source':link}
                idcount += 1
    save_data(result,'log/websc')
