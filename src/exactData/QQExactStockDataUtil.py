import requests
import time
import json
import sys
import importlib
importlib.reload(sys)
import util.DbUtil

url_XQ = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=before&begin=%d&end=%d'

def initStockInfoDataFromXQ():
    getStockInfoDataFromXQ('2001-01-01','2018-01-22')

def getStockInfoDataFromXQ(beginTimeStr,endTimeStr):
    beginTime = time.strptime(beginTimeStr, '%Y-%m-%d')
    endTime = time.strptime(endTimeStr, '%Y-%m-%d')
    beginStamp = int(time.mktime(beginTime)) * 1000
    endStamp = int(time.mktime(endTime)) * 1000
    requests.get(url='https://xueqiu.com')
    selectSql = '''
        select code,stockNo FROM `stockdata`.`stockinfo`
    '''    
    results = util.DbUtil.executeQuery(selectSql)
    for row in results:
        try:
            code = row[0];
            targetUrl = url_XQ % (code, beginStamp, endStamp)        
            resp = requests.get(url=targetUrl)
            content = resp.content            
            decodeContent = content.encode('latin-1').decode('unicode_escape')
            data = json.loads(decodeContent)
            __analsisQQStockDataAndUpdateDb(data)
        except Exception as err:
            print(err)


def __analsisQQStockDataAndUpdateDb(data):
    deteleSqlTmp = '''
        DELETE FROM `stockdata`.`qqexactstockdata` WHERE code='%S'
    ''';
    insertSqlTmp = '''
        INSERT INO  `stockdata`.`qqexactstockdata`
        (code,stockNo,volume,openP,closeP,highP,lowP,priceChange,percent,turnrate,ma5,ma10,ma20,ma30,dif,dea,macd,lot_volume,tranTimestamp,tranDate)
        VALUES
        ('%s','%s',%d, %d,%d,%d,%d, %d,%d,%d, %d,%d,%d,%d, ,%d,%d,%d,%d, ,%d,'%s')
    '''
    code = data.stock.symbol
    stockNo = code[2, 8]
    deteleSql = deteleSqlTmp % (code)
    util.DbUtil.executeUpdate(deteleSql)
    
    stockdata = data.chartlist
    for stockDayData in stockdata:
        volume = stockDayData.volume
        openP = stockDayData.open
        closeP = stockDayData.close
        highP = stockDayData.high
        lowP = stockDayData.low
        priceChange = stockDayData.chg
        percent = stockDayData.percent
        turnrate = stockDayData.turnrate
        ma5 = stockDayData.ma5
        ma10 = stockDayData.ma10
        ma20 = stockDayData.ma20
        ma30 = stockDayData.ma30
        dif = stockDayData.dif
        dea = stockDayData.dea
        macd = stockDayData.macd
        lot_volume = stockDayData.lot_volume
        tranTimestamp = stockDayData.timestamp
        time_run = time.gmtime(tranTimestamp / 1000)
        tranDate = time.strptime(time_run, "%Y-%m-%d")
        insertSql = insertSqlTmp % (code,stockNo,volume, openP,closeP,highP,lowP,priceChange,percent,turnrate,ma5,ma10,ma20,ma30,dif,dea,macd,lot_volume,tranTimestamp,tranDate)
        util.DbUtil.executeUpdate(insertSql)