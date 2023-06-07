import requests
from lxml import etree
import csv
import random
import time

def header_x():
    # 随机获取一个headers
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'
                   ]

    headers = {
        "User-Agent": random.choice(user_agents)
    }
    return headers

ip_list = []
with open('./python/practice/ip_broker.txt') as f:
    ip_list = f.readlines()

# 获取ip代理
def get_ip():
    proxy = ip_list[random.randint(0,len(ip_list)-1)]
    proxy = proxy.replace("\n","")
    proxies = {
        'http':'http://'+str(proxy),
    }
    return proxies

def get_parse(result):
    items = etree.HTML(result)
    # 共6页，分为文学，流行，文化，生活，经管，科技
    for i in range(1, 7):
        item = items.xpath('//*[@id="content"]/div/div[1]/div[2]/div[{}]'.format(i))
        for it in item:
            # 归属大类
            category = it.xpath('./a/@name')[0]
            # 辅助列
            auxiliary_array = it.xpath('./table/tbody/tr')
            for its in auxiliary_array:
                for j in range(1, 5):
                    time.sleep(random.randint(2, 6))
                    try:
                        # 标签
                        label = its.xpath('./td[{}]/a/text()'.format(j))[0]
                        # 标签链接
                        link = its.xpath('./td[{}]/a/@href'.format(j))[0]
                    except:
                        continue
                    # 书籍解析
                    get_content(category,label,link)

def get_content(category,label,link):
    D=[]
    # 最多展示50页
    for i in range(0, 50):
        # 设置换页的时间等待时间
        time.sleep(random.randint(3, 5))
        print('+++++++++++++++++++++',i)
        # 链接
        # https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=40&type=T
        link1 = 'https://book.douban.com' + link + '?start={}&type=T'.format(i * 20)
        print(link1)
        try:
            response = requests.get(url=link1, proxies=get_ip(), headers=header_x())
        except:
            continue
        items = etree.HTML(response.text)
        item = items.xpath('//*[@id="subject_list"]/ul/li')
        for its in item:
            # 设置每条数据的时间间隔
            time.sleep(random.randint(2, 5))

            try:
                # 书名
                title = its.xpath('./div[2]/h2/a/text()')[0]
                # 删除不需要的单元格
                title1 = title.replace('\n', '').replace('\t', '').strip()
            except:
                continue

            # 辅助列
            auxiliary_array = its.xpath('./div[2]/div[1]/text()')[0]
            auxiliary_array = auxiliary_array.replace('\n', '').replace('\t', '').strip().split('/')
            for i in range(0, 20):
                for it1 in auxiliary_array:
                    if (it1.strip() == ''):
                        auxiliary_array.remove(it1)

            if len(auxiliary_array) == 5:
                broker = auxiliary_array[0].split(']')
                if len(broker) == 1:
                    broker = auxiliary_array[0].split('】')
                    if len(broker) == 1:
                        broker = auxiliary_array[0].split(')')
                        if len(broker) == 1:
                            broker = auxiliary_array[0].split('）')
                            if len(broker) == 1:
                                broker = auxiliary_array[0].split('〕')
                                if len(broker) == 1:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                                elif len(broker) == 2:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                        # 作者
                                        author = broker[1].strip()
                                    else:
                                        # 国家
                                        country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                else:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                    else:
                                        # 国家
                                        country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            elif len(broker) == 2:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        elif len(broker) == 2:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                                # 作者
                                author = broker[1].strip()
                            else:
                                # 国家
                                country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        else:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                            else:
                                # 国家
                                country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    elif len(broker) == 2:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                            # 作者
                            author = broker[1].strip()
                        else:
                            # 国家
                            country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    else:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                        else:
                            # 国家
                            country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                elif len(broker) == 2:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                        # 作者
                        author = broker[1].strip()
                    else:
                        # 国家
                        country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                else:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                    else:
                        # 国家
                        country = ''
                    # 作者
                    author = auxiliary_array[0].strip()
                
                # 译者
                translator = auxiliary_array[1].strip()
                # 出版社
                press = auxiliary_array[2].strip()
                # 出版日期
                pubdate = auxiliary_array[3].strip()
                # 价格
                price = auxiliary_array[4].strip()

            elif len(auxiliary_array) == 4:
                flag = 0
                thing1 = auxiliary_array[3].split('-')
                if (len(thing1) > 1):
                    flag = 1
                elif (len(thing1) == 1):
                    try:
                        if ((int(thing1[0].strip()) > 1800) and int(thing1[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                thing2 = auxiliary_array[3].split('年')
                if (len(thing2) > 1):
                    flag = 1
                elif (len(thing2) == 1):
                    try:
                        if (int(thing2[0].strip()) > 1800 and int(thing2[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                thing3 = auxiliary_array[3].split('.')
                if (len(thing3) > 2):
                    flag = 1
                elif (len(thing3) == 2):
                    try:
                        if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224 and int(thing3[1].strip()) < 12 and int(thing3[1].strip()) > 0):
                            flag = 1
                    except:
                        pass
                elif (len(thing3) == 1):
                    try:
                        if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                if (flag == 1):
                    broker = auxiliary_array[0].split(']')
                    if len(broker) == 1:
                        broker = auxiliary_array[0].split('】')
                        if len(broker) == 1:
                            broker = auxiliary_array[0].split(')')
                            if len(broker) == 1:
                                broker = auxiliary_array[0].split('）')
                                if len(broker) == 1:
                                    broker = auxiliary_array[0].split('〕')
                                    if len(broker) == 1:
                                        # 国家
                                        country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                    elif len(broker) == 2:
                                        if broker[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker[0].strip('〔')
                                            # 作者
                                            author = broker[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker[0].strip('〔')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                elif len(broker) == 2:
                                    if broker[0].strip()[0] == '（':
                                        # 国家
                                        country = broker[0].strip('（')
                                        # 作者
                                        author = broker[1].strip()
                                    else:
                                        # 国家
                                        country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                else:
                                    if broker[0].strip()[0] == '（':
                                        # 国家
                                        country = broker[0].strip('（')
                                    else:
                                        # 国家
                                        country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            elif len(broker) == 2:
                                if broker[0].strip()[0] == '(':
                                    # 国家
                                    country = broker[0].strip('(')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '(':
                                    # 国家
                                    country = broker[0].strip('(')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        elif len(broker) == 2:
                            if broker[0].strip()[0] == '【':
                                # 国家
                                country = broker[0].strip('【')
                                # 作者
                                author = broker[1].strip()
                            else:
                                # 国家
                                country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        else:
                            if broker[0].strip()[0] == '【':
                                # 国家
                                country = broker[0].strip('【')
                            else:
                                # 国家
                                country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    elif len(broker) == 2:
                        if broker[0].strip()[0] == '[':
                            # 国家
                            country = broker[0].strip('[')
                            # 作者
                            author = broker[1].strip()
                        else:
                            # 国家
                            country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    else:
                        if broker[0].strip()[0] == '[':
                            # 国家
                            country = broker[0].strip('[')
                        else:
                            # 国家
                            country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                    
                    # 译者
                    translator = auxiliary_array[1].strip()
                    # 出版社
                    press = auxiliary_array[2].strip()
                    # 出版日期
                    pubdate = auxiliary_array[3].strip()
                    # 价格
                    price = ''
                else:
                    broker = auxiliary_array[0].split('】')
                    broker1 = auxiliary_array[0].split(']')
                    broker2 = auxiliary_array[0].split(')')
                    broker3 = auxiliary_array[0].split('）')
                    broker4 = auxiliary_array[0].split('〕')
                    if ((len(broker) == 1) and (len(broker1) == 1) and (len(broker2) == 1) and (len(broker3) == 1) and (len(broker4) == 1)):
                        thing = auxiliary_array[2].strip()
                        if ((thing[0] !='0') and (thing[0] !='1') and (thing[0] !='2') and (thing[0] !='3') and (thing[0] !='4') and (thing[0] !='5') and (thing[0] !='6') and (thing[0] !='7') and (thing[0] !='8') and (thing[0] !='9')):
                            # 国家
                            country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                            # 译者
                            translator = auxiliary_array[1].strip()
                            # 出版社
                            press = auxiliary_array[2].strip()
                            # 出版日期
                            pubdate = ''
                            # 价格
                            price = auxiliary_array[3].strip()
                        else:
                            # 国家
                            country = '中'
                            # 作者
                            author = auxiliary_array[0].strip()
                            # 译者
                            translator = ''
                            # 出版社
                            press = auxiliary_array[1].strip()
                            # 出版日期
                            pubdate = auxiliary_array[2].strip()
                            # 价格
                            price = auxiliary_array[3].strip()
                    else:
                        if len(broker) > 1:
                            if len(broker) == 2:
                                if broker[0].strip()[0] == '【':
                                    # 国家
                                    country = broker[0].strip('【')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '【':
                                    # 国家
                                    country = broker[0].strip('【')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker1) > 1:
                            if len(broker1) == 2:
                                if broker1[0].strip()[0] == '[':
                                    # 国家
                                    country = broker1[0].strip('[')
                                    # 作者
                                    author = broker1[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker1[0].strip()[0] == '[':
                                    # 国家
                                    country = broker1[0].strip('[')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker2) > 1:
                            if len(broker2) == 2:
                                if broker2[0].strip()[0] == '(':
                                    # 国家
                                    country = broker2[0].strip('(')
                                    # 作者
                                    author = broker2[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker2[0].strip()[0] == '(':
                                    # 国家
                                    country = broker2[0].strip('(')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker3) > 1:
                            if len(broker3) == 2:
                                if broker3[0].strip()[0] == '（':
                                    # 国家
                                    country = broker3[0].strip('（')
                                    # 作者
                                    author = broker3[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip() 
                            else:
                                if broker3[0].strip()[0] == '（':
                                    # 国家
                                    country = broker3[0].strip('（')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker4) > 1:
                            if len(broker4) == 2:
                                if broker4[0].strip()[0] == '〔':
                                    # 国家
                                    country = broker4[0].strip('〔')
                                    # 作者
                                    author = broker4[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()    
                            else:
                                if broker4[0].strip()[0] == '〔':
                                    # 国家
                                    country = broker4[0].strip('〔')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if ((country == '清') or (country == '明') or (country == '元') or (country == '宋') or (country == '唐') or (country == '汉')):
                            # 国家
                            country = '中'
                        thing = auxiliary_array[2].strip()
                        if ((thing[0] !='0') and (thing[0] !='1') and (thing[0] !='2') and (thing[0] !='3') and (thing[0] !='4') and (thing[0] !='5') and (thing[0] !='6') and (thing[0] !='7') and (thing[0] !='8') and (thing[0] !='9')):
                            # 译者
                            translator = auxiliary_array[1].strip()
                            # 出版社
                            press = auxiliary_array[2].strip()
                            # 出版日期
                            pubdate = ''
                            # 价格
                            price = auxiliary_array[3].strip()
                        else:
                            # 译者
                            translator = ''
                            # 出版社
                            press = auxiliary_array[1].strip()
                            # 出版日期
                            pubdate = auxiliary_array[2].strip()
                            # 价格
                            price = auxiliary_array[3].strip()

            elif len(auxiliary_array) == 3:
                flag = 0
                thing1 = auxiliary_array[2].split('-')
                if (len(thing1) > 1):
                    flag = 1
                elif (len(thing1) == 1):
                    try:
                        if (int(thing1[0].strip()) > 1800 and int(thing1[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                thing2 = auxiliary_array[2].split('年')
                if (len(thing2) > 1):
                    flag = 1
                elif (len(thing2) == 1):
                    try:
                        if (int(thing2[0].strip()) > 1800 and int(thing2[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                thing3 = auxiliary_array[2].split('.')
                if (len(thing3) > 2):
                    flag = 1
                elif (len(thing3) == 2):
                    try:
                        if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224 and int(thing3[1].strip()) < 12 and int(thing3[1].strip()) > 0):
                            flag = 1
                    except:
                        pass
                elif (len(thing3) == 1):
                    try:
                        if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224):
                            flag = 1
                    except:
                        pass
                if (flag == 1):
                    broker = auxiliary_array[0].split('】')
                    broker1 = auxiliary_array[0].split(']')
                    broker2 = auxiliary_array[0].split(')')
                    broker3 = auxiliary_array[0].split('）')
                    broker4 = auxiliary_array[0].split('〕')
                    if ((len(broker) == 1) and (len(broker1) == 1) and (len(broker2) == 1) and (len(broker3) == 1) and (len(broker4) == 1)):
                        # 国家
                        country='中'
                        # 作者
                        author = auxiliary_array[0].strip()
                        # 译者
                        translator = ''
                        # 出版社
                        press = auxiliary_array[1].strip()
                        # 出版日期
                        pubdate = auxiliary_array[2].strip()
                        # 价格
                        price = ''
                    else:
                        if len(broker) > 1:
                            if len(broker) == 2:
                                if broker[0].strip()[0] == '【':
                                    # 国家
                                    country = broker[0].strip('【')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '【':
                                    # 国家
                                    country = broker[0].strip('【')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker1) > 1:
                            if len(broker1) == 2:
                                if broker1[0].strip()[0] == '[':
                                    # 国家
                                    country = broker1[0].strip('[')
                                    # 作者
                                    author = broker1[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker1[0].strip()[0] == '[':
                                    # 国家
                                    country = broker1[0].strip('[')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker2) > 1:
                            if len(broker2) == 2:
                                if broker2[0].strip()[0] == '(':
                                    # 国家
                                    country = broker2[0].strip('(')
                                    # 作者
                                    author = broker2[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker2[0].strip()[0] == '(':
                                    # 国家
                                    country = broker2[0].strip('(')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker3) > 1:
                            if len(broker3) == 2:
                                if broker3[0].strip()[0] == '（':
                                    # 国家
                                    country = broker3[0].strip('（')
                                    # 作者
                                    author = broker3[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip() 
                            else:
                                if broker3[0].strip()[0] == '（':
                                    # 国家
                                    country = broker3[0].strip('（')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if len(broker4) > 1:
                            if len(broker4) == 2:
                                if broker4[0].strip()[0] == '〔':
                                    # 国家
                                    country = broker4[0].strip('〔')
                                    # 作者
                                    author = broker4[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()    
                            else:
                                if broker4[0].strip()[0] == '〔':
                                    # 国家
                                    country = broker4[0].strip('〔')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        if ((country == '清') or (country == '明') or (country == '元') or (country == '宋') or (country == '唐') or (country == '汉')):
                            # 国家
                            country = '中'
                        # 译者
                        translator = ''
                        # 出版社
                        press = auxiliary_array[1].strip()
                        # 出版日期
                        pubdate = auxiliary_array[2].strip()
                        # 价格
                        price = ''
                else:
                    flag = 0
                    thing1 = auxiliary_array[1].split('-')
                    if (len(thing1) > 1):
                        flag = 1
                    elif (len(thing1) == 1):
                        try:
                            if (int(thing1[0].strip()) > 1800 and int(thing1[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    thing2 = auxiliary_array[1].split('年')
                    if (len(thing2) > 1):
                        flag = 1
                    elif (len(thing2) == 1):
                        try:
                            if (int(thing2[0].strip()) > 1800 and int(thing2[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    thing3 = auxiliary_array[1].split('.')
                    if (len(thing3) > 2):
                        flag = 1
                    elif (len(thing3) == 2):
                        try:
                            if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224 and int(thing3[1].strip()) < 12 and int(thing3[1].strip()) > 0):
                                flag = 1
                        except:
                            pass
                    elif (len(thing3) == 1):
                        try:
                            if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    if (flag == 1):
                        thing3 = auxiliary_array[0].strip()
                        if ((thing3[-1] != '社') and (thing3[-1] != '版') and (thing3[-1] != '化' and (thing3[-1] != '文')) and (thing3[-1] != '司' and (thing3[-1] != '公'))):
                            broker = auxiliary_array[0].split('】')
                            broker1 = auxiliary_array[0].split(']')
                            broker2 = auxiliary_array[0].split(')')
                            broker3 = auxiliary_array[0].split('）')
                            broker4 = auxiliary_array[0].split('〕')
                            if ((len(broker) == 1) and (len(broker1) == 1) and (len(broker2) == 1) and (len(broker3) == 1) and (len(broker4) == 1)):
                                # 国家
                                country='中'
                                # 作者
                                author = auxiliary_array[0].strip()
                            else:
                                if len(broker) > 1:
                                    if len(broker) == 2:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                            # 作者
                                            author = broker[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker1) > 1:
                                    if len(broker1) == 2:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                            # 作者
                                            author = broker1[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker2) > 1:
                                    if len(broker2) == 2:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                            # 作者
                                            author = broker2[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker3) > 1:
                                    if len(broker3) == 2:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                            # 作者
                                            author = broker3[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip() 
                                    else:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker4) > 1:
                                    if len(broker4) == 2:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                            # 作者
                                            author = broker4[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()    
                                    else:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if ((country == '清') or (country == '明') or (country == '元') or (country == '宋') or (country == '唐') or (country == '汉')):
                                    # 国家
                                    country = '中'

                            # 译者
                            translator = ''
                            # 出版社
                            press = ''
                            # 出版日期
                            pubdate = auxiliary_array[1].strip()
                            # 价格
                            price = auxiliary_array[2].strip()
                        else:
                            # 国家
                            country=''
                            # 作者
                            author = ''
                            # 译者
                            translator = ''
                            # 出版社
                            press = auxiliary_array[0].strip()
                            # 出版日期
                            pubdate = auxiliary_array[1].strip()
                            # 价格
                            price = auxiliary_array[2].strip()
                    else:
                        thing3 = auxiliary_array[2].strip()
                        if ((thing3[-1] != '社') and (thing3[-1] != '版') and (thing3[-1] != '化' and (thing3[-1] != '文')) and (thing3[-1] != '司' and (thing3[-1] != '公'))):
                            broker = auxiliary_array[0].split('】')
                            broker1 = auxiliary_array[0].split(']')
                            broker2 = auxiliary_array[0].split(')')
                            broker3 = auxiliary_array[0].split('）')
                            broker4 = auxiliary_array[0].split('〕')
                            if ((len(broker) == 1) and (len(broker1) == 1) and (len(broker2) == 1) and (len(broker3) == 1) and (len(broker4) == 1)):
                                # 国家
                                country='中'
                                # 作者
                                author = auxiliary_array[0].strip()
                            else:
                                if len(broker) > 1:
                                    if len(broker) == 2:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                            # 作者
                                            author = broker[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker1) > 1:
                                    if len(broker1) == 2:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                            # 作者
                                            author = broker1[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker2) > 1:
                                    if len(broker2) == 2:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                            # 作者
                                            author = broker2[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker3) > 1:
                                    if len(broker3) == 2:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                            # 作者
                                            author = broker3[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip() 
                                    else:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker4) > 1:
                                    if len(broker4) == 2:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                            # 作者
                                            author = broker4[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()    
                                    else:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if ((country == '清') or (country == '明') or (country == '元') or (country == '宋') or (country == '唐') or (country == '汉')):
                                    # 国家
                                    country = '中'
                            # 译者
                            translator = ''
                            # 出版社
                            press = auxiliary_array[1].strip()
                            # 出版日期
                            pubdate = ''
                            # 价格
                            price = auxiliary_array[2].strip()
                        else:
                            broker = auxiliary_array[0].split('】')
                            broker1 = auxiliary_array[0].split(']')
                            broker2 = auxiliary_array[0].split(')')
                            broker3 = auxiliary_array[0].split('）')
                            broker4 = auxiliary_array[0].split('〕')
                            if ((len(broker) == 1) and (len(broker1) == 1) and (len(broker2) == 1) and (len(broker3) == 1) and (len(broker4) == 1)):
                                # 国家
                                country='中'
                                # 作者
                                author = auxiliary_array[0].strip()
                            else:
                                if len(broker) > 1:
                                    if len(broker) == 2:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                            # 作者
                                            author = broker[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker[0].strip()[0] == '【':
                                            # 国家
                                            country = broker[0].strip('【')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker1) > 1:
                                    if len(broker1) == 2:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                            # 作者
                                            author = broker1[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker1[0].strip()[0] == '[':
                                            # 国家
                                            country = broker1[0].strip('[')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker2) > 1:
                                    if len(broker2) == 2:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                            # 作者
                                            author = broker2[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()
                                    else:
                                        if broker2[0].strip()[0] == '(':
                                            # 国家
                                            country = broker2[0].strip('(')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker3) > 1:
                                    if len(broker3) == 2:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                            # 作者
                                            author = broker3[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip() 
                                    else:
                                        if broker3[0].strip()[0] == '（':
                                            # 国家
                                            country = broker3[0].strip('（')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if len(broker4) > 1:
                                    if len(broker4) == 2:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                            # 作者
                                            author = broker4[1].strip()
                                        else:
                                            # 国家
                                            country = ''
                                            # 作者
                                            author = auxiliary_array[0].strip()    
                                    else:
                                        if broker4[0].strip()[0] == '〔':
                                            # 国家
                                            country = broker4[0].strip('〔')
                                        else:
                                            # 国家
                                            country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                if ((country == '清') or (country == '明') or (country == '元') or (country == '宋') or (country == '唐') or (country == '汉')):
                                    # 国家
                                    country = '中'
                            # 译者
                            translator = auxiliary_array[1].strip()
                            # 出版社
                            press = auxiliary_array[2].strip()
                            # 出版日期
                            pubdate = ''
                            # 价格
                            price = ''

            elif  len(auxiliary_array) == 2:
                thing3 = auxiliary_array[0].strip()
                if ((thing3[-1] != '社') and (thing3[-1] != '版') and (thing3[-1] != '化' and (thing3[-1] != '文')) and (thing3[-1] != '司' and (thing3[-1] != '公'))):
                    thing = auxiliary_array[0].strip()
                    if ((thing[0] !='0') and (thing[0] !='1') and (thing[0] !='2') and (thing[0] !='3') and (thing[0] !='4') and (thing[0] !='5') and (thing[0] !='6') and (thing[0] !='7') and (thing[0] !='8') and (thing[0] !='9')):
                        # 国家
                        country='中'
                        # 作者
                        author = auxiliary_array[0].strip()
                        # 译者
                        translator = ''
                        # 出版社
                        press = auxiliary_array[1].strip()
                        # 出版日期
                        pubdate = ''
                        # 价格
                        price = ''
                    else:
                        # 国家
                        country=''
                        # 作者
                        author = ''
                        # 译者
                        translator = ''
                        # 出版社
                        press = ''
                        # 出版日期
                        pubdate = auxiliary_array[0].strip()
                        # 价格
                        price = auxiliary_array[1].strip()
                else:
                    flag = 0
                    thing1 = auxiliary_array[1].split('-')
                    if (len(thing1) > 1):
                        flag = 1
                    elif (len(thing1) == 1):
                        try:
                            if (int(thing1[0].strip()) > 1800 and int(thing1[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    thing2 = auxiliary_array[1].split('年')
                    if (len(thing2) > 1):
                        flag = 1
                    elif (len(thing2) == 1):
                        try:
                            if (int(thing2[0].strip()) > 1800 and int(thing2[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    thing3 = auxiliary_array[1].split('.')
                    if (len(thing3) > 2):
                        flag = 1
                    elif (len(thing3) == 2):
                        try:
                            if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224 and int(thing3[1].strip()) < 12 and int(thing3[1].strip()) > 0):
                                flag = 1
                        except:
                            pass
                    elif (len(thing3) == 1):
                        try:
                            if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224):
                                flag = 1
                        except:
                            pass
                    if flag == 0:
                        # 国家
                        country=''
                        # 作者
                        author = ''
                        # 译者
                        translator = ''
                        # 出版社
                        press = auxiliary_array[0].strip()
                        # 出版日期
                        pubdate = ''
                        # 价格
                        price = auxiliary_array[1].strip()
                    else:
                        # 国家
                        country=''
                        # 作者
                        author = ''
                        # 译者
                        translator = ''
                        # 出版社
                        press = auxiliary_array[0].strip()
                        # 出版日期
                        pubdate = auxiliary_array[1].strip()
                        # 价格
                        price = ''
            
            elif  len(auxiliary_array) == 1:
                thing3 = auxiliary_array[0].strip()
                if ((thing3[-1] != '社') and (thing3[-1] != '版') and (thing3[-1] != '化' and (thing3[-1] != '文')) and (thing3[-1] != '司' and (thing3[-1] != '公'))):
                    thing = auxiliary_array[0].strip()
                    if ((thing[0] !='0') and (thing[0] !='1') and (thing[0] !='2') and (thing[0] !='3') and (thing[0] !='4') and (thing[0] !='5') and (thing[0] !='6') and (thing[0] !='7') and (thing[0] !='8') and (thing[0] !='9')):
                        flag = 0
                        thing1 = auxiliary_array[0].split('-')
                        if (len(thing1) > 1):
                            flag = 1
                        elif (len(thing1) == 1):
                            try:
                                if (int(thing1[0].strip()) > 1800 and int(thing1[0].strip()) < 2224):
                                    flag = 1
                            except:
                                pass
                        thing2 = auxiliary_array[0].split('年')
                        if (len(thing2) > 1):
                            flag = 1
                        elif (len(thing2) == 1):
                            try:
                                if (int(thing2[0].strip()) > 1800 and int(thing2[0].strip()) < 2224):
                                    flag = 1
                            except:
                                pass
                        thing3 = auxiliary_array[0].split('.')
                        if (len(thing3) > 2):
                            flag = 1
                        elif (len(thing3) == 2):
                            try:
                                if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224 and int(thing3[1].strip()) < 12 and int(thing3[1].strip()) > 0):
                                    flag = 1
                            except:
                                pass
                        elif (len(thing3) == 1):
                            try:
                                if int(thing3[0].strip()) > 1800:
                                    flag = 1
                            except:
                                pass
                        elif (len(thing3) == 1):
                            try:
                                if (int(thing3[0].strip()) > 1800 and int(thing3[0].strip()) < 2224):
                                    flag = 1
                            except:
                                pass
                        if (flag != 1):
                            # 国家
                            country=''
                            # 作者
                            author = ''
                            # 译者
                            translator = ''
                            # 出版社
                            press = ''
                            # 出版日期
                            pubdate = ''
                            # 价格
                            price = auxiliary_array[0].strip()
                        else:
                            # 国家
                            country=''
                            # 作者
                            author = ''
                            # 译者
                            translator = ''
                            # 出版社
                            press = ''
                            # 出版日期
                            pubdate = auxiliary_array[0].strip()
                            # 价格
                            price = ''
                    else:
                        # 国家
                        country=''
                        # 作者
                        author = auxiliary_array[0].strip()
                        # 译者
                        translator = ''
                        # 出版社
                        press = ''
                        # 出版日期
                        pubdate = ''
                        # 价格
                        price = ''
                else:
                    # 国家
                    country=''
                    # 作者
                    author = ''
                    # 译者
                    translator = ''
                    # 出版社
                    press = auxiliary_array[0].strip()
                    # 出版日期
                    pubdate = ''
                    # 价格
                    price = ''
            elif len(auxiliary_array) == 6:
                broker = auxiliary_array[0].split(']')
                if len(broker) == 1:
                    broker = auxiliary_array[0].split('】')
                    if len(broker) == 1:
                        broker = auxiliary_array[0].split(')')
                        if len(broker) == 1:
                            broker = auxiliary_array[0].split('）')
                            if len(broker) == 1:
                                broker = auxiliary_array[0].split('〕')
                                if len(broker) == 1:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                                elif len(broker) == 2:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                        # 作者
                                        author = broker[1].strip()
                                    else:
                                        # 国家
                                        country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                else:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                    else:
                                        # 国家
                                        country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            elif len(broker) == 2:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        elif len(broker) == 2:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                                # 作者
                                author = broker[1].strip()
                            else:
                                # 国家
                                country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        else:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                            else:
                                # 国家
                                country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    elif len(broker) == 2:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                            # 作者
                            author = broker[1].strip()
                        else:
                            # 国家
                            country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    else:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                        else:
                            # 国家
                            country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                elif len(broker) == 2:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                        # 作者
                        author = broker[1].strip()
                    else:
                        # 国家
                        country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                else:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                    else:
                        # 国家
                        country = ''
                    # 作者
                    author = auxiliary_array[0].strip()
                
                # 译者
                translator = auxiliary_array[1].strip()
                # 出版社
                press = auxiliary_array[2].strip()
                # 出版日期
                pubdate = auxiliary_array[3].strip()
                # 价格
                price = auxiliary_array[4].strip() + '/' + auxiliary_array[5].strip()
            elif len(auxiliary_array) == 7:
                broker = auxiliary_array[0].split(']')
                if len(broker) == 1:
                    broker = auxiliary_array[0].split('】')
                    if len(broker) == 1:
                        broker = auxiliary_array[0].split(')')
                        if len(broker) == 1:
                            broker = auxiliary_array[0].split('）')
                            if len(broker) == 1:
                                broker = auxiliary_array[0].split('〕')
                                if len(broker) == 1:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                                elif len(broker) == 2:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                        # 作者
                                        author = broker[1].strip()
                                    else:
                                        # 国家
                                        country = ''
                                        # 作者
                                        author = auxiliary_array[0].strip()
                                else:
                                    if broker[0].strip()[0] == '〔':
                                        # 国家
                                        country = broker[0].strip('〔')
                                    else:
                                        # 国家
                                        country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            elif len(broker) == 2:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                    # 作者
                                    author = broker[1].strip()
                                else:
                                    # 国家
                                    country = ''
                                    # 作者
                                    author = auxiliary_array[0].strip()
                            else:
                                if broker[0].strip()[0] == '（':
                                    # 国家
                                    country = broker[0].strip('（')
                                else:
                                    # 国家
                                    country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        elif len(broker) == 2:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                                # 作者
                                author = broker[1].strip()
                            else:
                                # 国家
                                country = ''
                                # 作者
                                author = auxiliary_array[0].strip()
                        else:
                            if broker[0].strip()[0] == '(':
                                # 国家
                                country = broker[0].strip('(')
                            else:
                                # 国家
                                country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    elif len(broker) == 2:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                            # 作者
                            author = broker[1].strip()
                        else:
                            # 国家
                            country = ''
                            # 作者
                            author = auxiliary_array[0].strip()
                    else:
                        if broker[0].strip()[0] == '【':
                            # 国家
                            country = broker[0].strip('【')
                        else:
                            # 国家
                            country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                elif len(broker) == 2:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                        # 作者
                        author = broker[1].strip()
                    else:
                        # 国家
                        country = ''
                        # 作者
                        author = auxiliary_array[0].strip()
                else:
                    if broker[0].strip()[0] == '[':
                        # 国家
                        country = broker[0].strip('[')
                    else:
                        # 国家
                        country = ''
                    # 作者
                    author = auxiliary_array[0].strip()
                
                # 译者
                translator = auxiliary_array[1].strip()
                # 出版社
                press = auxiliary_array[2].strip()
                # 出版日期
                pubdate = auxiliary_array[3].strip() + '-' + auxiliary_array[4].strip() + '-' + auxiliary_array[5].strip()
                # 价格
                price = auxiliary_array[6].strip()
            else:
                # 国家
                country=''
                # 作者
                author = ''
                # 译者
                translator = ''
                # 出版社
                press = ''
                # 出版日期
                pubdate = ''
                # 价格
                price = ''

            # 国家
            country = country
            # 作者
            author = author
            # 译者
            translator = translator
            # 出版社
            press = press
            # 出版日期
            pubdate = pubdate
            # 价格
            price = price

            # 评分
            try:
                score = its.xpath('./div[2]/div[2]/span[2]/text()')[0]
            except:
                score = ''
        
            # 评价人数
            try:
                raters_number = its.xpath('./div[2]/div[2]/span[3]/text()')[0]
                raters_number = raters_number.replace('\n', '').replace('\t','').strip().strip('(').strip(')')
            except:
                raters_number = ''
            
            # 书籍简介
            try:
                profile = its.xpath('./div[2]/p/text()')[0].replace('\n', '').replace('\t','')
            except:
                profile = ''

            data=[category,label,title1,country,author,translator,press,pubdate,price,score,raters_number,profile]
            D.append(data)
        save(D)
        D.clear()


def save(name):
    with open('./豆瓣读书.csv', 'a', newline='', encoding='gb18030') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerows(name)

def main():
    header = ['大类别','标签','书名','国家','作者','译者','出版社','出版日期','价格','评分','评价人数','简介']
    with open('./豆瓣读书.csv','a', newline='', encoding='gb18030')as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        
    url='https://book.douban.com/tag/'
    result=requests.get(url, proxies=get_ip(), headers=header_x()).text
    get_parse(result)

if __name__=='__main__':
    main()


