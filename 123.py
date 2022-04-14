import re
import threading
import time
import scrapy
import requests
from bs4 import BeautifulSoup as bs
import urllib.request as req
#<span class="publish-date">出版日期：2019-06-14</span>



a = []
b = []
while True:
    n = input('輸入關鍵字:')
    url = "https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword={}".format(n)
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    })

    with req.urlopen(request) as r:
        data = r.read().decode("utf-8")
    
    root = bs(data, "html.parser")
    title = root.find_all("li")
    
    for t in title:
        if t.a != None:
            a.append(t.a.string)
            #print(t.a.string)
            for i in range(len(a)):
                if a[i] != None:
                    x = re.search(str(a[i]), n).group()
                    if x == n:
                        b.append(a[i])
                        print(b)
            '''
            if :
                b.append(a)
                print(b)
        else:
            print('none')
            '''