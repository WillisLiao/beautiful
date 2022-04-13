import mysql.connector as myconn
import pandas as pd
import re
data = pd.read_csv('aq.csv', index_col=False, delimiter = ',')
print(data.head())   #.head() prints the first 5 rows, useful for checking data



#Pandas Dataframe 空值會寫Nan, 這行把Nan換成None, 等會insert時會被視為空值
data2 = data.astype(object).where(pd.notnull(data), None)

while True:

    action = input("Create database and table '1' \t Insert data '2' \tSearch by date '3': ")
    if action =='1':

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
        #`pm2.5`   有 . 就加 ``
        sql = '''CREATE TABLE Xituan(
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        aqi varchar(255) ,
                        co varchar(255) ,
                        co_8hr varchar(255) ,
                        county varchar(255)  ,
                        datacreationdate varchar(255),
                        latitude varchar(255) ,
                        longitude varchar(255),
                        no varchar(255) ,
                        no2 varchar(255) ,
                        nox varchar(255) ,
                        o3 varchar(255) ,
                        o3_8hr varchar(255) ,
                        pm10 varchar(255) ,
                        pm10_avg varchar(255) ,
                        `pm2.5` varchar(255) ,         
                        `pm2.5_avg` varchar(255) ,
                        pollutant varchar(255) ,
                        siteid varchar(255) ,
                        sitename varchar(255) ,
                        so2 varchar(255) ,
                        so2_avg varchar(255) ,
                        status varchar(255),
                        unit varchar(255),
                        winddirec varchar(255) ,
                        windspeed varchar(255)       
                        )
                        '''

        my_cursor = dbConn.cursor()   
        my_cursor.execute('DROP TABLE IF EXISTS Xituan')                                 
        my_cursor.execute(sql)
        print('Table is created....')
        my_cursor.execute('SHOW TABLES')

        print('Tables: ')
        for table in my_cursor:
                print(table[0])
                


    elif action =='2':
        dbConn = myconn.connect(
                        host = 'localhost',
                        user = 'aquser',
                        password = '!a000000',
                        database = 'aqD1047316'
                        
            )
        
        my_cursor = dbConn.cursor(buffered=True)       #buffered = True 解決 unread results Error                      
        my_cursor.execute('SHOW TABLES')

        #loop through the data frame
        for i, row in data2.iterrows():
            sql2 = '''INSERT IGNORE INTO aqD1047316.Xituan( aqi, co, co_8hr, county, datacreationdate, latitude, longitude, no, no2, nox, o3, o3_8hr, pm10, pm10_avg, `pm2.5`, `pm2.5_avg`, pollutant, siteid, sitename, so2, so2_avg, status, unit, winddirec, windspeed) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            my_cursor.execute(sql2, tuple(row))
            print('Record inserted')
            dbConn.commit()


    elif action == '3':
        dbConn = myconn.connect(
                        host = 'localhost',
                        user = 'aquser',
                        password = '!a000000',
                        database = 'aqD1047316'
                        
            )
        
        my_cursor = dbConn.cursor(buffered=True)    
        date = input('date: ')
        creationdatelist = data['datacreationdate'].tolist()
        r = re.compile(f'.*{date}') # '.'Any character except newline , '*' 0 or more  
        newlist = list(filter(r.match, creationdatelist))


        data.set_index("datacreationdate", inplace=True)
        count=0
        
        print(f'有{len(newlist)}筆資料')
        c = int(input('你要幾筆: '))
        

        for i in range(c):

            my_cursor.execute(f'''select * from Xituan where `datacreationdate` ='{newlist[i]}' ''')
            records = my_cursor.fetchall()
            for record in records:
                print(record)

    elif action == 'stop':
        break





            
        


