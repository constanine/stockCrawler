import requests
import xlrd
import time
import sys
import importlib
importlib.reload(sys)
import util.DbUtil
import cfg.Config

url_WY = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s'

def initStockInfoDataFromWY():
    getStockInfoDataFromWY('2001-01-01','2018-01-22')

def getStockInfoDataFromWY(beginTime,endTime):
    selectSql = '''
        select code,stockNo FROM `stockdata`.`stockinfo`
    '''
    
    results = util.DbUtil.executeQuery(selectSql)
    for row in results:
        try:
            code = row[0];
            stockNo = row[1];
            stockCode = '0'+row[1]
            if ( code.startswith('sz') ):
                stockCode = '1'+row[1]
            targetUrl = url_WY % (stockNo, beginTime, endTime)
            resp = requests.get(url=targetUrl)
            content = resp.content
            filename = cfg.Config.sysPath+'exactdata/qqindmapping-%s.xls' % (stockCode)
            f = open(filename, 'wb')
            f.write(content)        
            __analsisWYStockDataAndUpdateDb(filename,code,stockNo)
        except Exception as err:
            print(err)


def __analsisWYStockDataAndUpdateDb(filename,code,stockNo):
    deteleSqlTmp = '''
        DELETE FROM `stockdata`.`wangyiexactstockdata` WHERE code='%S'
    ''';
    insertSqlTmp = '''
        INSERT INO  `stockdata`.`wangyiexactstockdata`
        (code,stockNo,openP,closeP,highP,lowP,priceChange,percent,turnrate,volume,volumeAmout,totalMarketValue,currentValue,tranTimestamp,volumeHand,tranDate)
        VALUES
        ('%s','%s', %d,%d,%d,%d, %d,%d,%d, %d,%d,%d,%d,%d, %d,'%s')
    '''
    deteleSql = deteleSqlTmp % (code)
    util.DbUtil.executeUpdate(deteleSql)
    
    data = xlrd.open_workbook(filename)
    sheet = data.sheet_by_index(0)
    rows = sheet.nrows
    rowIdx = 0;
    for row in range(rows):
        stockDayData = sheet.row_values(row)
        if (rowIdx < 1) :
            if(stockDayData[0] == '404 Not Found'):
                break
            rowIdx += 1
            continue
        else :
            tranDate = stockDayData[0]
            tranDate.replace('/','-')
            closeP = stockDayData[3]
            highP = stockDayData[4]
            lowP = stockDayData[5]
            openP = stockDayData[6]
            priceChange = stockDayData[8]
            percent = stockDayData[9]
            turnrate = stockDayData[10]
            volume = stockDayData[11]
            volumeAmout = stockDayData[12]
            totalMarketValue = stockDayData[13]
            currentValue = stockDayData[14]
            volumeHand = stockDayData[15]
            timeTuple = time.strptime(tranDate, "%Y-%m-%d")
            tranTimestamp = int(time.mktime(timeTuple))*1000
            insertSql = insertSqlTmp % (code,stockNo,openP,closeP,highP,lowP,priceChange,percent,turnrate,volume,volumeAmout,totalMarketValue,currentValue,volumeHand,tranTimestamp,tranDate)
            util.DbUtil.executeUpdate(insertSql)