import requests
import xlrd
import importlib
import sys
importlib.reload(sys)
import util.DbUtil
import cfg.Config

filename = cfg.Config.sysPath+'/stockdata.xls'

def getStockInfoDataFromQQ():
    target = 'http://stock.gtimg.cn/data/get_hs_xls.php?id=rankash&type=1&metric=chr'
    resp = requests.get(url = target)
    content = resp.content
    f = open(filename, 'wb')
    f.write(content)
    __analsisBaseDataAndUpdateDb(filename);
    print("base data is done!")


def __analsisBaseDataAndUpdateDb(filename):
    data = xlrd.open_workbook(filename)
    sheet = data.sheet_by_index(0)
    rows = sheet.nrows
    rowIdx = 0;
    for row in range(rows):
        if (rowIdx < 2):
            rowIdx += 1
            continue
        else :
            rowData = sheet.row_values(row)
            code = rowData[0]
            stockNo = code[2:8];
            name = rowData[1]
            updateSql = '''UPDATE `stockdata`.`stockinfo` SET name='%s',stockNo='%s',version = version+1
                WHERE code='%s' ''' % (name,stockNo,code)
            result = util.DbUtil.executeUpdate(updateSql)
            if(result < 1):
                insertSql = '''INSERT INTO `stockdata`.`stockinfo` (name,code,stockNo) 
                    VALUES ('%s','%s','%s')''' % (name,code,stockNo)
                util.DbUtil.executeUpdate(insertSql)
                rowIdx += 1