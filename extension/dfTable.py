import pandas as pd
import pymysql


def get_dfTable(tablename):
    serverName = '127.0.0.1'
    # 登陆用户名和密码
    userName = 'root'
    passWord = 'root'
    # 建立连接并获取cursor
    db = pymysql.connect(user=userName, password=passWord, host=serverName, database="torch")
    cur = db.cursor()
    sql = f'select * from {tablename}'
    cur.execute(sql)
    col = cur.description
    dbdata = cur.fetchall()
    db.close()
    col_list = [i[0] for i in col]
    return pd.DataFrame(dbdata, columns=col_list)