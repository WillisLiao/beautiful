import requests
from bs4 import BeautifulSoup 
import re
import time
import concurrent.futures as cf
import mysql.connector as myconn
import pandas as pd

#取得網頁的html
url = "https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword=Java"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
print(doc.prettify)
print('html successfully requested!')
while True:
    action  = input("Search: 1   Get title, publish date and insert to database: 2\n: ")



    #search keywords
    if action=="1":

        kw1, kw2, kw3, kw4, kw5 = map(str, input('type in 5 keywords(case sensitive): ').split())
        kwList = [kw1, kw2, kw3, kw4, kw5]

        start_time = time.time()

        def search(keyword):

            keywords = doc.find_all()
            for rows in keywords:
                for i in range(5):
                    if keyword in str(rows.string):
                            print(rows.string)
                            
            

            if len(keywords) == 0:
                    print('no result found, please type in another keyword')
            
            
        
        keywords = doc.find_all()
        for rows in keywords:
            for i in range(5):
                if kwList[i] in str(rows.string):
                        print(rows.string)
                        
        end_time = time.time()

        if len(keywords) == 0:
                print('no result found, please type in another keyword')

        print('\n')

        start_time2 = time.time()
        with cf.ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(search, kwList)
        end_time2 = time.time()

        print(f'Single threaded search time: {end_time - start_time}')
        print(f'Multi threaded search time: {end_time2 - start_time2}')
        






    elif action=='2':
        start_time = time.time()
        #書名
        name_list = []
        tags = doc.find_all(['a'], class_="cover w-full")
        for i in range(len(tags)):
            tags = doc.find_all(['a'], class_="cover w-full")[i]
            tags2 = tags.find('img')

            print(re.search(r'"(.*?)"', str(tags2)).group(1))
            name_list.append(re.search(r'"(.*?)"', str(tags2)).group(1))
        



        #出版日期
        dates = doc.find_all(text = re.compile(r'出版日期.*'))

        n=0
        pbdateList = []
        print(len(dates))
        for i in range(31):

            datesp = dates[i].parent


            if '-' in str(datesp.string):
                i+=1
                print(datesp.string)
                pbdateList.append(datesp.string.strip('出版日期:'))
        print(name_list)
        print(pbdateList)
        print('\nGot title & publish_date!\n')
    




        dbConn = myconn.connect(
                        host = 'localhost',
                        user = 'aquser',
                        password = '!a000000',
                        #database = 'aqD1047316'
                        
            )
        my_cursor = dbConn.cursor()
        my_cursor.execute('CREATE DATABASE IF NOT EXISTS aqD1047316')
        dbConn = myconn.connect(
                        host = 'localhost',
                        user = 'aquser',
                        password = '!a000000',
                        database = 'aqD1047316'
                        
            )
        
        
        print('creating table....')

        sql = '''CREATE TABLE Books(
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        title varchar(255) ,
                        publish_date varchar(255) 
     
                        )
                        '''

        my_cursor = dbConn.cursor()   
        my_cursor.execute('DROP TABLE IF EXISTS Books')                                 
        my_cursor.execute(sql)
        print('Table is created....')
        my_cursor.execute('SHOW TABLES')

        print('Tables: ')
        for table in my_cursor:
                print(table[0])


        dbConn = myconn.connect(
                        host = 'localhost',
                        user = 'aquser',
                        password = '!a000000',
                        database = 'aqD1047316'
                        
            )
        
        my_cursor = dbConn.cursor(buffered=True)       #buffered = True 解決 unread results Error                      
        my_cursor.execute('SHOW TABLES')

        #loop through the data frame
        for data in name_list:
            sql2 = '''INSERT IGNORE INTO aqD1047316.Books( title ) VALUES(%s)'''
            my_cursor.execute(sql2)
            print('Record inserted')
            dbConn.commit()

        for data in pbdateList:
            sql3 = '''INSERT IGNORE INTO aqD1047316.Books( publish_date ) VALUES(%s)'''
            my_cursor.execute(sql3)
            print('Record inserted')
            dbConn.commit()

        end_time = time.time()
        print(f'took {start_time - end_time} seconds')
        

    elif action=='stop':
        break






    
    
        
