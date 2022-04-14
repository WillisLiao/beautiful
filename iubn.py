import requests
import bs4 
import mysql.connector as myconn
import datetime
import threading
import time 
import concurrent.futures as cf  

dbConn = myconn.connect (
    host = 'localhost' , 
    user = 'aquser' ,
    password = '!a000000' 
    )
my_cursor = dbConn.cursor()
my_cursor.execute('CREATE DATABASE IF NOT EXISTS `aqD1089308`')

dbConn = myconn.connect ( 
    host = 'localhost' ,
    user = 'aquser' ,
    password = '!a000000' , 
    database = 'aqD1089308'
    )
my_cursor = dbConn.cursor()

sql = '''CREATE TABLE BookData (    # 表格tittle 建立 
    ID INTEGER AUTO_INCREMENT PRIMARY KEY , 
    Title VARCHAR (255) NOT NULL ,
    Publish_Data VARCHAR (255) NOT NULL 
    )'''
my_cursor.execute(sql)   # 寫入title


# b = [] 
# for time in range (5) :
    
#     keyword = input()
#     header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
#     url = 'https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=' + keyword
#     html = requests.get (url ,headers = header)
#     web = bs4.BeautifulSoup(html.text ,'lxml')
#     resultTable = web.select ('.book-data')
    
#     for i in range(len(resultTable)) :  
#         a = []      
#         result1 = resultTable[i].select('strong')
#         if len(result1)!=0:
#             if result1[0].select('a')[0].getText() !='':
#                 # print(result1[0].select('a')[0].getText())
#                 data = result1[0].select('a')[0].getText()
#                 a.append(data)
        
#         result2 = resultTable[i] .select('ul') 
#         if len(result2) != 0 :
#             if result2[0].select('span')[0].getText() != '':
#                 # print (result2[0].select('span')[0].getText())
#                 data = result2[0].select ('span')[0].getText()
#                 a.append(data)
#                 a = tuple(a)
#                 b.append(a)
# print(b)

def main(c) :
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
    for n in c :
        url = 'https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=' + n
        html = requests.get (url ,headers = header)
        web = bs4.BeautifulSoup(html.text ,'lxml')
        resultTable = web.select ('.book-data')

        for i in range(len(resultTable)) :  
            a = []      
            result1 = resultTable[i].select('strong')
            if len(result1)!=0:
                if result1[0].select('a')[0].getText() !='':
                    # print(result1[0].select('a')[0].getText())
                    data = result1[0].select('a')[0].getText()
                    a.append(data)
        
            result2 = resultTable[i] .select('ul') 
            if len(result2) != 0 :
                if result2[0].select('span')[0].getText() != '':
                    # print (result2[0].select('span')[0].getText())
                    data = result2[0].select ('span')[0].getText()
                    a.append(data.replace('出版日期：' ,''))   
                    # a.append(data)                
                    a = tuple(a)
                    b.append(a)
        print('Done')

search = [] 
b = []
for i in range (5) :
    keyword = input()
    search.append(keyword)
    # print (search)

st = time.time()
with cf.ThreadPoolExecutor (max_workers=10) as executor :
    executor.map(main ,search)

et = time.time()
set = et - st 
print(set)

sql = 'INSERT INTO BookData ( Title ,Publish_Data ) VALUES ( %s ,%s )'
my_cursor.executemany(sql , b) # 將檔案加入，並依照title格式
dbConn.commit()
print('Done')