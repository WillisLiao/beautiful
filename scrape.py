''' 請同學以「天瓏書局」為目標，讓使用者一次輸入 5 種不同的查詢關鍵字，例如:
講理, Python, Java, Database, C++。程式可以經由網頁爬蟲程式抓取
● 請分別以傳統的爬蟲方式查詢，再以多執行緒的方式進行查詢，並分別計算其
所花費的時間分別是多少
● 下列網址為 天瓏書局的網址最後面的 Java 就是使用者輸入的 查詢關鍵字
● https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=Java
● 下頁投影片是 查詢結果的頁面，請同學用爬蟲取書籍的「書名」及「出版日期」
資料
● 請用 MySQL 建立一個資料表，欄位有「id」、「title」、「publish_date」並將前小題
得到的結果存入到 MySQL 的資料表中
● 程式結束時要能呈現綜上操作程式執行網路爬蟲並完成寫入到資料庫總共花
了多少時間'''




#取得網頁的html
import requests
from bs4 import BeautifulSoup 
import re
import time
import concurrent.futures as cf
url = "https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=Java"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
print(doc.prettify)

#while True:
 #   action  = input("Search: 1\tGet title and publish date: 2\tInsert to database: 3")



#search keywords

kw1, kw2, kw3, kw4, kw5 = map(input('type in 5 keywords').split())
kwList = [kw1, kw2, kw3, kw4, kw5]

start_time = time.time()


keywords = doc.find_all()
for rows in keywords:
    for i in range(5):
        if kwList[i] in str(rows.string):
                print(rows.string)
end_time = time.time()

if len(keywords) == 0:
        print('no result found, please type in another keyword')

print(f'search time: {end_time - start_time}')



with cf.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map()









#書名
name_list = []
tags = doc.find_all(['a'], class_="cover w-full")
for i in range(len(tags)):
    tags = doc.find_all(['a'], class_="cover w-full")[i]
    tags2 = tags.find('img')

    print(re.search(r'"(.*?)"', str(tags2)).group(1))
    name_list.append(re.search(r'"(.*?)"', str(tags2)).group(1))
print(name_list)










#出版日期
dates = doc.find_all(text = re.compile(r'出版日期.*'))

n=0
print(len(dates))
for i in range(31):

    datesp = dates[i].parent


    if '-' in str(datesp.string):
        i+=1
        print(datesp.string)






    
    
        
