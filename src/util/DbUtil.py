import pymysql

db = pymysql.connect("localhost","root","root","stockdata",3306,None,'utf8') 
cursor  = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

def init(): 
    # 打开数据库连接
    db = pymysql.connect("localhost","root","root","stockdata" )     
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    cursor.execute('SET NAMES UTF8')  
    return cursor
 
def executeUpdate(sql):
    try:
        # 执行SQL语句
        result = cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except OSError as err:
        print(err)
        # 发生错误时回滚
        db.rollback()
    return result
       
def executeQuery(sql):
    results = 0;
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        results = cursor.fetchall()
    except OSError as err:
        print(err)
        # 发生错误时回滚
        db.rollback()       
    return results
       
def closeDbContect():
    # 关闭数据库连接
    db.close()