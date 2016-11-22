#encoding:utf-8
import sys
import requests
from bs4 import BeautifulSoup
import time
import os
reload(sys)
sys.setdefaultencoding('utf8')
def get_baidu_dingdian(ficname):
    try:
        baidu_fiction_url = '''http://www.baidu.com/s?wd=site:www.dingdianzw.com intitle:'''+ficname+ '''&oq=site:www.dingdianzw.com'''
        a = requests.get(baidu_fiction_url)
        bsaint = BeautifulSoup(a.text,"html.parser")
        geturl = [i.find(name='a') for i in bsaint.find(name='div',id = 'content_left').find_all(name = 'h3')]
        return [i['href'] for i in geturl]
    except Exception as e:
        print e
        raise
    # 返回百度查询到定点的小说链接

def get_baidu_biquge(ficname):
    try:
        baidu_fiction_url = '''http://www.baidu.com/s?wd=site:www.biqugezw.com intitle:'''+ficname+ '''&oq=site:www.biqugezw.com'''
        a = requests.get(baidu_fiction_url)
        bsaint = BeautifulSoup(a.text,"html.parser")
        geturl = [i.find(name='a') for i in bsaint.find(name='div',id = 'content_left').find_all(name = 'h3')]
        return [i['href'] for i in geturl]
    except Exception as e:
        print e
        raise
    # 返回百度查询到笔趣的小说链接

def retry3(fun):
    def dfun(*args):
        for i in range(3):
            try:
                data = fun(*args)
                return data
            except Exception as e:
                print e
        return False
    return dfun

# @retry3
def main_biquge_fiction(urls):
        a = requests.get(urls)
        a.encoding = 'gbk'
        mpbs = BeautifulSoup(a.text,"html.parser")
        all_f_list = [(i.text,'http://www.biqugezw.com' + i['href']) for i in mpbs.find(name='div',id = 'list').find_all(name = 'a')]
        return all_f_list
    #返回小说所有的章节名和链接

@retry3
def main_dingdian_fiction(urls):
    mpbs = BeautifulSoup(requests.get(urls).text,"html.parser")
    all_f_list = [(i.string,'http://www.dingdianzw.com' + i['href']) for i in mpbs.find(name='table',id = 'bgdiv').find_all(name = 'a')]
    return all_f_list
    #返回小说所有的章节名和链接

@retry3
def get_dingdian_ficzhang(urls):
    a = BeautifulSoup(requests.get(urls).text,"html.parser").find(name='div',id='content')
    a = a.text.replace(u'\n','').replace(u'\r','').replace(u'\t','').replace(u'\xa0\xa0\xa0\xa0','')
    a = a.replace(u'\u5929\u624d\u4e00\u79d2\u8bb0\u4f4f\u672c\u7ad9\u5730\u5740:(\u9876\u70b9\u4e2d\u6587)www.dingdianzw.com,\u6700\u5feb\u66f4\u65b0!\u65e0\u5e7f\u544a!','')
    return a

    # stripped_strings
    # 天才一秒记住本站地址:(顶点中文)
    # www.dingdianzw.com, 最快更新!无广告!
    # (未完待续。)手机用户请浏览阅读，更优质的阅读体验

@retry3
def get_biquge_ficzhang(urls):
    url_req = requests.get(urls)
    url_req.encoding = 'gbk'
    a = BeautifulSoup(url_req.text,"html.parser").find(name='div',id='content')
    a = a.text.replace(u'\n', '').replace(u'\r', '').replace(u'\t', '').replace(u'\xa0\xa0\xa0\xa0', '')
    a = a.replace(u'\u4e00\u79d2\u8bb0\u4f4f\u3010\u7b14\u8da3\u9601\u4e2d\u6587\u7f51www.biqugezw.com\u3011\uff0c\u4e3a\u60a8\u63d0\u4f9b\u7cbe\u5f69\u5c0f\u8bf4\u9605\u8bfb\u3002','')
    a = a.replace(u'\u624b\u673a\u7528\u6237\u8bf7\u6d4f\u89c8m.biqugezw.com\u9605\u8bfb\uff0c\u66f4\u4f18\u8d28\u7684\u9605\u8bfb\u4f53\u9a8c\u3002','')
    return a


def save_data(filename,data = ''):
    with open(filename,'a') as f_file:
        f_file.write(data+'\n')

def djstr(zname,filename):
    with open(filename) as mefile:
        while True:
            lines = mefile.readline()
            if lines == '':
                return False
            if zname in mefile.readline():
                return True

def run(ficname):
    for bi_url in get_baidu_biquge(ficname):
        sav_filename = 'biqu/' + ficname +'.txt'
        # if os.path.exists(sav_filename):
        #     os.remove(sav_filename)

        if len(bi_url) > 0:
            save_data(sav_filename)
        else:
            break

        for pageurl in main_biquge_fiction(bi_url):
            if not djstr(pageurl[0],sav_filename):
                print pageurl[0]
                save_data(sav_filename,pageurl[0])
                print pageurl[1]
                pagedata = get_biquge_ficzhang(pageurl[1])
                if pagedata:save_data(sav_filename,pagedata)
                sys.stdout.flush()

    for din_url in get_baidu_dingdian(ficname):
        sav_filename = 'dingdian/'+ficname +'.txt'
        if len(din_url) > 0:
            save_data(sav_filename)
        else:
            break

        for pageurl in main_dingdian_fiction(din_url) or []:
            if not djstr(pageurl[0], sav_filename):
                print pageurl[0]
                save_data(sav_filename,pageurl[0])
                print pageurl[1]
                pagedata = get_dingdian_ficzhang(pageurl[1])
                if pagedata:save_data(sav_filename,pagedata)
                sys.stdout.flush()

def biqulinkpid(bi_url,ficname):
    sav_filename = 'biqu/' + ficname + '.txt'
    save_data(sav_filename)
    for pageurl in main_biquge_fiction(bi_url):
        time.sleep(0.5)
        if not djstr(pageurl[0], sav_filename):
            print pageurl[0]
            save_data(sav_filename, pageurl[0])
            print pageurl[1]
            pagedata = get_biquge_ficzhang(pageurl[1])
            if pagedata: save_data(sav_filename, pagedata)
            sys.stdout.flush()

def ddlinkpid(dd_url,ficname):
    sav_filename = 'dingdian/' + ficname + '.txt'
    save_data(sav_filename)
    for pageurl in main_dingdian_fiction(dd_url):
        time.sleep(0.5)
        if not djstr(pageurl[0], sav_filename):
            print pageurl[0]
            save_data(sav_filename, pageurl[0])
            print pageurl[1]
            pagedata = get_dingdian_ficzhang(pageurl[1])
            if pagedata: save_data(sav_filename, pagedata)
            sys.stdout.flush()

if __name__ == '__main__':
    # xsname = sys.argv[1].decode('gbk').encode('utf-8').decode('utf-8')
    run(ficname = u'一念永恒')
    # biqulinkpid('http://www.biqugezw.com/0_317/',u'不朽凡人')

# get_dingdian_ficzhang('http://www.dingdianzw.com/chapter/2430_2052331.html')
# print get_biquge_ficzhang('http://www.biqugezw.com/3_3096/2599596.html')
# 数据模型计划
'''
表1  所有的爬过的书 cid     qi/b    bookname    firsttime   uptime

表2  书的章节       cid     numb     zhangname   sourceurl    body   firsttime   uptime

表3  更新情况       cid     who      upbody   uptime
'''
