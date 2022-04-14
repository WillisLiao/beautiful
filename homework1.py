import requests
from bs4 import BeautifulSoup 
import re
import time
import concurrent.futures as cf
import mysql.connector as myconn


#取得網頁的html
def scrape(yourlist):
        print('\nrequesting for html........\n')
        url = f"https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword={yourlist}"

        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        print('html successfully requested!\n')





        
            #書名
        name_list = []
        tags = doc.find_all(['a'], class_="cover w-full")
        for i in range(len(tags)):
            tags = doc.find_all(['a'], class_="cover w-full")[i]
            tags2 = tags.find('img')
            a = str(re.search(r'"(.*?)"', str(tags2)).group(1))

            name_list.append(a.replace("'", ''))
            



            #出版日期
        dates = doc.find_all(text = re.compile(r'出版日期.*'))

        n=0
        pbdateList = []
    
        for i in range(31):

            datesp = dates[i].parent


            if '-' in str(datesp.string):
                i+=1

                pbdateList.append(str(datesp.string.replace('出版日期：',''))) #冒號為全形

        print('\nGot title & publish_date!\n')
        






        dbConn = myconn.connect(
                            host = 'localhost',
                            user = 'aquser',
                            password = '!a000000',
                            database = 'aqD1047316'
                            
                )
            
        my_cursor = dbConn.cursor(buffered=True)       #buffered = True 解決 unread results Error                      
        my_cursor.execute('SHOW TABLES')

            #loop through the data frame
        print(name_list)
        print(pbdateList)
        for i in range(len(name_list)):

            sql4 = f'''INSERT IGNORE INTO aqD1047316.Books( title, publish_date) VALUES('{str(name_list[i])}','{str(pbdateList[i])}')'''
            my_cursor.execute(sql4)
            print('Record inserted')
            dbConn.commit()



        


while True:
    
    kw1, kw2, kw3, kw4, kw5 = map(str, input('type in 5 keywords: ').split())
    if kw1=='stop' and kw2=='1' and kw3=='2' and kw4=='3' and kw5=='4':
        break

    kwList = [kw1, kw2, kw3, kw4, kw5]
    start_time = time.time()
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
            
    time.sleep(2)
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
    time.sleep(2)
    print('Table is created....')
    my_cursor.execute('SHOW TABLES')
    time.sleep(2)
    print('Tables: ')
    for table in my_cursor:
        print(table[0])
    time.sleep(2)

    for i in kwList:

        print('\nrequesting for html........\n')
        url = f"https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword={i}"

        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        print('html successfully requested!\n')





        
            #書名
        name_list = []
        tags = doc.find_all(['a'], class_="cover w-full")
        for i in range(len(tags)):
            tags = doc.find_all(['a'], class_="cover w-full")[i]
            tags2 = tags.find('img')
            a = str(re.search(r'"(.*?)"', str(tags2)).group(1)).replace(':','')

            name_list.append(a.replace("'", ''))
            



            #出版日期
        dates = doc.find_all(text = re.compile(r'出版日期.*'))

        n=0
        pbdateList = []
    
        for i in range(31):

            datesp = dates[i].parent


            if '-' in str(datesp.string):
                i+=1

                pbdateList.append(str(datesp.string.replace('出版日期：',''))) #冒號為全形

        print('\nGot title & publish_date!\n')
        






        dbConn = myconn.connect(
                            host = 'localhost',
                            user = 'aquser',
                            password = '!a000000',
                            database = 'aqD1047316'
                            
                )
            
        my_cursor = dbConn.cursor(buffered=True)       #buffered = True 解決 unread results Error                      
        my_cursor.execute('SHOW TABLES')

            #loop through the data frame
        print(name_list)
        print(pbdateList)
        for i in range(len(name_list)):

            sql4 = f'''INSERT IGNORE INTO aqD1047316.Books( title, publish_date) VALUES('{str(name_list[i])}','{str(pbdateList[i])}')'''
            my_cursor.execute(sql4)
            print('Record inserted')
            dbConn.commit()

    end_time = time.time()
    print('starting multi thread...')
    time.sleep(1)
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
            
    time.sleep(2)
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
    time.sleep(2)
    print('Table is created....')
    my_cursor.execute('SHOW TABLES')
    time.sleep(2)
    print('Tables: ')
    for table in my_cursor:
        print(table[0])
    time.sleep(2)
    start_time2 = time.time()
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape, kwList)
    
    end_time2 = time.time()
    print(f'\n Single threaded took {end_time - start_time - 8} seconds\n')
    print(f'\n Multi threaded took {end_time2 - start_time2 } seconds\n')



    

        

