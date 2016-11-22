#coding:utf-8

import re
import requests
import urllib
import time
import random
from PIL import Image
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#账号密码
username = '18711138248'
password = 'liubowen110'
#预回复的贴吧
tiebaming = 'dota2'
tiebaming_url = urllib.quote(tiebaming)
#验证码保存地址
img_yzm = 'code.jpg'
#回帖次数和刷新首页次数
huifucishu = 1
shuaxincishu = 1
#回复的内容，多加，避开关键词不然会被度娘吞贴
huifu_content = [
'一个老师问三个学生，你们用什么东西可以将一间屋子填满。第一个学生找来了稻草，铺满了地板，老师摇了摇头。第二个学生找来一根蜡烛，顿时屋子里充满了光芒，老师还是摇了摇头，因为学生的影子没有被照到。 这时第三个学生往地板上丢了块肥皂，没一会，欢快的娇喘声便充满了整个房间。',
'分手后，前任给她现任男友打电话嘱咐：“她胃不好，每天早上要喝一碗粥，晚上记得给他熬生姜汁”，现任男友：“我花5万块钱给根治了”',
'女生和男神表白。男神默默地掏出手机后说：“我有女朋友了，你要看照片吗？”女生万念俱灰间下意识点了头 ，缓缓抬头。瞬间看见了暗掉的手机屏幕和镜面反射后自己的容颜。抑制不住的泪水划出眼眶流过脸颊。男神见状有些诧异，拿回手机后挠了挠头说：”哎？不好意思，黑屏了。”',
'叫醒你的不是闹钟，是梦想',
'终于有天我长大了，一大早起来去买菜，我在家用地理知识测了今天的风速天气等，保证我不会被大风吹走后换衣服出门。到了菜市场我跟卖菜的大妈说：汝可有青菜否？大妈说：你说啥，说清楚点。我说：Can you sell some qing cai to me？大妈说：你他妈给我说人话。我说：就是那些由植物细胞组成的，里面有叶绿体线粒体高尔基体核糖体内质网液泡等等的东西啊。大妈恼了：你他妈来捣乱的吧。说完给了我一巴掌。我很生气的说：南京大屠杀告诉我们做人不可以这样，不能那么残忍动不动就动手打人，如果每个人都像你这样，就会像曾经第二次世界大战那样……我还没说完大妈又给了我一巴掌！…好不容易大妈知道了我要买青菜，我好心的说：大妈我帮你用函数关系式算一下。说完我拿出随身携带的笔和纸算了起来。几分钟后我大妈已经将青菜装进黑袋子，我兴奋的跟大妈说：大妈我算出来了我只用付您5块钱！大妈抬手又给了我一巴掌：操你妈你买了那么多青菜5块钱想赖账吗！！……经过一番激烈的…被打。我乖乖的付了足够的钱，转身就要走，突然想起了什么，回头问大妈：大妈你这个塑料袋是什么做的啊，会不会和青菜发生化学反应，那些化学反应的方程式您可以写给我吗？……后来我被路人打电话叫来的警察局的人带走了。警察问我：年龄。我说：18。医生问：职业？我说：学霸!呵呵呵呵呵呵呵呵呵呵呵呵呵呵呵。',
'今天跟一个妹子下象棋。。。你说你马可以走“目”字。因为是千里马。我忍了。你的兵可以倒退走。说是特种兵。我忍了。。你的象可以过河。是小飞象。我忍了。你说你的炮可以不用隔棋或者隔两个以上都可以打。因为是高射炮。我也忍了。你的车可以拐弯。还说哪有车不能拐弯的吗？？这。。。我也忍了。。。。但你用我的士干掉我的将。还说是你培养了多年的间谍。特意派来做卧底的。。。怎么不直接把帅丢了，说不配',
'不禁让我想起高中时我的同桌，那时候她很喜欢我，可当时我晚熟，不懂她的心思，当年我很喜欢踢球，经常跟她讲关于足球方面的事，我很喜欢小贝，她也跟着我喜欢小贝，我每次踢球她都会来看，我还送了张小贝的明信片，她当时高兴坏了，我以为是因为小贝的原因。不知不觉高中毕业，然后是大学，我也再没有跟她联系，因为工作的原因很少踢球了，有一天，突然心血来潮，来到球场看人踢球，突然我被一小男孩吸引住了，他的运球，射门颇有小贝的味道，我就上前跟她聊了聊，当我问他最喜欢哪个球星时他回答道小贝，小贝都退役这么多年了一个小孩子也知道？我好奇的问道你也知道小贝？我当然知道，我妈妈还有一张他的明信片呢，小男孩看着我认真的说，我看着面前的小男孩，阳光洒在他脸上，我却一点也不感到悲伤，因为上面都是我瞎编的。',
'话说有个女人身材极差，所以就找魔法校长邓不利多看看能不能帮到她。邓不利多：“禁忌森林湖边有只魔法青蛙，只要你能让它说一次‘不行’，你就会升2 Cup。”女人跟着指示去到湖边，她看着自己的Ａ Cup想了想，就问：“青蛙！青蛙！我可不可以吃了你？” 青蛙：“不行！” 女人果然由Ａ Cup升至C Cup，但她并未满意，于是又问：“你可不可以被我吃了？” 青蛙：“不行！”女人又大2 Cup！但她贪心想做H Cup波霸，于是又问多次：“真的不行？” 青蛙：“怎么这么烦啊你！要我讲多少次呀？都说不行啦！不行不行不行???????????????????????????',
'晚上，关上灯，妻子对睡在身边的丈夫小声说：“强子，村里的工厂在招人，你明天去试试吧？”强子是村里唯一的大学生，大学毕业后一直没找到合意的工作，已经在家闲了两年，家里的开支全靠妻子丽琴白天在外摆摊卖小吃赚钱。“我可是大学生，哪里能去村里的厂子做工人卖苦力。你一个女人懂啥，我是做大事的人！”强子很不高兴，翻身背对着丽琴睡了。丽琴枕边湿了一圈……….“强子，我最近摆摊回来的晚，要不你在家把晚饭做了吧。”丽琴忙了一天才回家，拖着疲惫的身子一边准备晚饭一边和坐在电脑前的丈夫商量。“我是个做大事的男人，做饭这种家务活是你们女人的事，别丢给我。”强子头也不回的丢下一句，继续打他的游戏，丝毫没有要帮帮丽琴的意思。丽琴并没有因为强子的话而放弃，手里一边淘米一边走到强子身边：“那要不然你白天来我的摊子帮我一起卖小吃吧？现在客人越来越多，我一个人也忙不过来。干脆我们夫妻俩一起做这个摊子，一定能把生意做大的。”她其实早就想让强子和她一起打理摊子的生意了，既然强子一直找不到满意的工作，那夫妻俩一起把现在的小吃摊做大也是不错的。可丽琴的提议并没有换来强子的回头，他只是当听了一阵耳边风似得轻哼一声，非常不屑的说：“切，就你那个小摊，我这个大学生去了岂不是大材小用！我可不去做那种小买卖。”丽琴看着强子打游戏的背影，嘴张开迟疑了一下终究又闭上了………日复一日年复一年，强子依旧每天呆在家里等待着他合意的工作，等待着他飞黄腾达的机会。而妻子丽琴自那次以后再也没有劝过他什么，每天白天早早的就出门打理自己的生意，晚上回来默默整理好被强子弄乱的家。疲惫一天的她晚上几乎累到倒头就睡，而丈夫强子不是对着电脑就是和哥们出门喝酒打牌，夫妻两的对话越来越少。忽然某天，强子在外喝酒时偶然听人说丽琴的小吃配方被大企业看中了要收购，丽琴也将成为大公司的高管，他立即急匆匆的跑回家找到妻子。“琴，听说你的凉粉被大企业看上了，你要做大企业的高管了？”“嗯，怎么了？”丽琴不紧不慢的应了一句，依旧背对着强子准备着她的晚饭。“那可是大公司，你把你老公我介绍进去呗。这可是千载难逢的好机会啊。”强子越说越高兴，他感觉他的机遇终于来到了。',
'一个男孩爱打dota。当一次他过生日时一个他暗恋好久的女孩子问他，你们打dota的男孩子最常听到的话是什么，男孩为了装个逼，说当然是戈软的配置（五杀），女孩听了就走了。过了几天女孩说借电脑用一下，给他一个生日礼物。等到男孩再从女孩手里把电脑拿回来时迫不及待的开了一句dota。等到开始游戏了之后他才发现女孩把游戏里所有的音效都改了，全部变成了女孩亲自录制的萌萌的声音。时隔多年，男孩女孩早已不再联系，当男孩第一次拿到人生中第一次五杀时，他后悔不已。因为他听到的是I love you。 这个故事告诉我们，，，，，菜比 是不配拥有爱情的！！！！',
'一想到一个月后水嫩水嫩的学妹就要在烈日下军训了，身为学长的我真是心痛不已，真想让她们皮糙肉厚的学姐替她们军训。',
'某天你男友出差，长夜漫漫，你很无聊，写了一篇博客，记录下了盛夏夜中你此刻的心情。喝完咖啡，你正打算上床睡觉了，突然你又好奇想知道自己青春的文采已被多少人阅读。于是你打开电脑，登上服务器，去查看你博客的访问日志，从referrer中你发现，你的男朋友和你的男同事在凌晨一点，都访问了你发的链接，并且IP一样。这个时候，作为一个男子汉，你可能要考虑下，应该哭多大声才不会吵到邻居……当然，你还可以安慰自己，他们是一起在网吧通宵玩游戏',
]
mouse_pwd1=[
'40%2C47%2C45%2C54%2C43%2C42%2C34%2C42%2C44%2C19%2C43%2C54%2C42%2C54%2C43%2C54%2C42%2C54%2C43%2C54%2C42%2C54%2C43%2C54%2C42%2C54%2C43%2C54%2C42%2C19%2C46%2C43%2C45%2C35%2C34%2C19%2C43%2C40%2C34%2C42%2C54%2C34%2C42%2C42%2C',
'83%2C81%2C88%2C76%2C81%2C80%2C85%2C82%2C88%2C105%2C81%2C76%2C80%2C76%2C81%2C76%2C80%2C76%2C81%2C76%2C80%2C76%2C81%2C76%2C80%2C76%2C81%2C76%2C80%2C105%2C82%2C85%2C83%2C84%2C88%2C105%2C81%2C82%2C88%2C80%2C76%2C88%2C80%2C80%2C',
'110%2C105%2C105%2C112%2C109%2C109%2C105%2C100%2C109%2C85%2C109%2C112%2C108%2C112%2C109%2C112%2C108%2C112%2C109%2C112%2C108%2C112%2C109%2C112%2C108%2C112%2C109%2C112%2C108%2C85%2C109%2C107%2C110%2C111%2C107%2C85%2C109%2C110%2C100%2C108%2C112%2C100%2C108%2C108%2C',
'56%2C63%2C62%2C38%2C59%2C58%2C61%2C50%2C51%2C3%2C59%2C38%2C58%2C38%2C59%2C38%2C58%2C38%2C59%2C38%2C58%2C38%2C59%2C38%2C58%2C3%2C57%2C63%2C58%2C57%2C3%2C59%2C56%2C50%2C58%2C38%2C50%2C58%2C58%2C',
'113%2C114%2C119%2C110%2C119%2C117%2C112%2C119%2C75%2C115%2C110%2C114%2C110%2C115%2C110%2C114%2C110%2C115%2C110%2C114%2C110%2C115%2C110%2C114%2C110%2C115%2C110%2C114%2C75%2C115%2C122%2C114%2C123%2C115%2C75%2C115%2C112%2C122%2C114%2C110%2C122%2C114%2C114%2C',
]


r = requests.Session()
r.get('http://www.baidu.com/')
r.get('https://passport.baidu.com/v2/api/?login')
cook = r.get('https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true')
cookie_token = cook.text
token = re.findall(r"bdPass.api.params.login_token='(.*?)'", cookie_token)[0]

headers = {
    'Host': 'passport.baidu.com',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com/',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
r.get('https://passport.baidu.com/v2/api/?login',headers=headers)
 
payload1={
        'staticpage':'http://www.baidu.com/res/static/thirdparty/pass_v3_jump.html',
        'charset':'utf-8',
        'token':token,
        'tpl':'pp',
        'apiver':'v3',
        'tt': '1392637410384',
        'codestring' : '',
        'safeflg' : '0',
        'u' :'http://www.baidu.com/',
        'isPhone' : 'false',
        'quick_user'  : '0',
        'loginmerge': 'true',
        'logintype' : 'basicLogin',
        'username': username,
        'password': password,
        'verifycode':'',
        'mem_pass':'on',
        'ppui_logintime' : '49586',
        'callback':'parent.bd__pcbs__hksq59'
    } 
login = r.post('https://passport.baidu.com/v2/api/?login',data=payload1,headers=headers,verify=True)
get_code = re.findall(r'codeString=(.*?)&userName',login.text)[0]
# print get_code
code = r.get("https://passport.baidu.com/cgi-bin/genimage",params=get_code,stream=True)

if code.status_code == 200:
    with open(img_yzm, 'wb') as f:
        for chunk in code.iter_content():
            f.write(chunk)

#没有载入Image库就删除下面两句，手动打开验证码文件
image = Image.open(img_yzm)
image.show()

verifycode = ''
while not verifycode:
    verifycode = raw_input(r'Input verifycode:')

     
payload2={
        'staticpage' : 'http://www.baidu.com/res/static/thirdparty/pass_v3_jump.html',
        'charset' : 'utf-8',
        'token' : token,
        'tpl':'netdisk',
        'apiver':'v3',
        'tt': '1392637410384',
        'codestring' : get_code,
        'safeflg' : '0',
        'u' :'http://www.baidu.com/',
        'isPhone' : 'false',
        'quick_user'  : '0',
        'loginmerge': 'true',
        'logintype' : 'basicLogin',
        'username': username,
        'password': password,
        'verifycode':verifycode,
        'ppui_logintime' : '49586',
        'callback':'parent.bd__pcbs__hksq59'
    } 
r.post("https://passport.baidu.com/v2/api/?login", data=payload2,headers=headers,verify=True)
exit()
#回帖
def _huitie(r,qbeau):
	for x in qbeau.find_all(name='li',attrs = {'class':' j_thread_list clearfix'}):
            title = x.find_all(name = 'a',attrs ={'href':True,'title':True,'target':'_blank','class':'j_th_tit'})
            for i in title:
                print 'Title:"' + i['title'] + '"',  

            huifu = x.find_all(name = 'span',title = '回复')
            for j in huifu:
                print '回复:' + j.text,   
                if j.text == '0':
                    print 'http://tieba.baidu.com' + i['href']
                    tiezi = r.get('http://tieba.baidu.com' + i['href'])
                    huifucontent = random.choice(huifu_content)
                    huifucontent = urllib.quote(huifucontent)
                    mouse_pwd = random.choice(mouse_pwd1)
                    link = re.findall(r'''<link rel="canonical" href="http://tieba.baidu.com/p/(.*?)"/>''',tiezi.text)[0]
                    tbs = re.findall(r'''var PageData = {        "tbs": "(.*?)",        "charset"''',tiezi.text)
                    if tbs:
                        fid = re.findall(r'''data-fid="(.*?)" data-tid=''',q.text)
                        if fid:
                            fid = fid[2]
                        else:
                            print 'fid错误'
                            exit()
                        tbs = tbs[0]
                    else:
                        tbs = re.findall(r'''var PageData = {"tbs"  : "(.*?)","charset"''',tiezi.text)
                        if tbs:
                            fid = re.findall(r'''data-fid="(.*?)" data-tid=''',q.text)[3]
                            if fid:
                                fid = fid[2]
                            else:
                                print 'fid错误'
                                exit()
                            tbs = tbs[0]
                        else:
                            print '获取tbs失败,请重试'
                            exit()
                    shijianchuo1 = str(time.time())
                    shijianchuo = shijianchuo1[:10] + '266'
                    # print 'tiebaming_url:' + tiebaming_url
                    # print 'fid:' + fid
                    # print 'link:' + link
                    # print 'tbs:' + tbs
                    # print 'huifucontent:' + huifucontent
                    # print 'mouse_pwd:' + mouse_pwd
                    # print 'shijianchuo:' + shijianchuo
                    huitie = 'ie=utf-8&kw=' + tiebaming_url + '&fid=' + fid + '&tid=' + link + '&vcode_md5=&floor_num=1&rich_text=1&tbs=' + tbs + '&content=' + huifucontent + '&files=%5B%5D&mouse_pwd=' + mouse_pwd + shijianchuo + '0&mouse_pwd_t=' + shijianchuo + '&mouse_pwd_isclick=0&__type__=reply'
                    #print huitie
                    fatie_result = r.post('http://tieba.baidu.com/f/commit/post/add',data = huitie)
                    print fatie_result.text
                    print 'huifu:' + str(huifucishu)
                    #返回 "no":0,"err_code":0 代表发帖成功无错误，但可能会被度娘吞贴，自己查看吧
                    time.sleep(60)
                    #不是常用IP登陆的话，第二次回帖会返回7001	
                    return True
                else:
                    print

if 'BDUSS' in r.cookies:
    q = r.get('http://tieba.baidu.com/')
    tieba = q.text
    user = re.findall(r'>                    (.*?)</a></div>',q.text)[0]
    print r'登陆用户：%s'%user
    q = r.get('http://tieba.baidu.com/home/main?un=' + user + '&fr=ibaidu&ie=utf-8')
    guanzhudeba = re.findall(r'''forum_name":"(.*?)","is_black"''',q.text)[0:]
    num = 0
    baming = []

#显示关注的吧及等级
    for i in guanzhudeba:
        levelid = re.findall(r'''level_id":(.*?),"cur_score"''',q.text)[num]
        baming.append(i)
        print r'关注的吧：'+ i + "\t贴吧等级:" + levelid
        num = num + 1

#签到
    ba_num = num
    num = 0
    while(num != ba_num):
        data_qiandao = 'ie=utf-8&kw=' + baming[num].encode()
        q = r.post('http://tieba.baidu.com/sign/add',data = data_qiandao)
        num = num + 1

#占领二楼
    while(True):
        q = r.get('http://tieba.baidu.com/f?kw=' + tiebaming + '&fr=index')
        print 'http://tieba.baidu.com/f?kw=' + tiebaming + '&fr=index'
        print 'shuaxin:' + str(shuaxincishu)
        shuaxincishu = shuaxincishu + 1
        qbeau = BeautifulSoup(q.text,'html.parser')
        if _huitie(r,qbeau,huifucishu):
        	huifucishu += 1
        
        
        time.sleep(1)



else:
    print '登陆失败，请重试'
