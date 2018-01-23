import requests
import xlrd
import importlib
import sys
importlib.reload(sys)
import util.DbUtil
import cfg.Config

def getSCRCMappingData():
    targetStdUrl = 'http://stock.gtimg.cn/data/get_hs_xls.php?id=%s&type=1&metric=name'
    selectSql = '''
        select id,name,code,typeno FROM `stockdata`.`csrctypedata`
    '''
    results = util.DbUtil.executeQuery(selectSql)
    for row in results:
        try:
            rowId = row[0];
            name = row[1];
            code = row[2];
            typeNo = row[3];
            filename = cfg.Config.sysPath+'basedata/scrcmapping-%s.xls' % (name)
            targetUrl = targetStdUrl % (typeNo)        
            resp = requests.get(url = targetUrl)
            content = resp.content
            f = open(filename, 'wb')
            f.write(content)        
            __analsisSMDataAndUpdateDb(filename,rowId,name,code)
        except Exception as err:
            print(err)
            
    print("SCRCMappingDataUtil data is done!")

def __analsisSMDataAndUpdateDb(filename,parentId,parentName,parentCode):
    data = xlrd.open_workbook(filename)
    sheet = data.sheet_by_index(0)
    rows = sheet.nrows
    rowIdx = 0;
    for row in range(rows):           
        if (rowIdx < 2):
            rowData = sheet.row_values(row)
            if(rowData[0] == '404 Not Found'):
                break
            rowIdx += 1
            continue
        else :
            rowData = sheet.row_values(row)
            code = rowData[0]
            stockNo = code[2:8];
            name = rowData[1]
            updateSql = '''UPDATE `stockdata`.`csrcmappingdata` SET name='%s',stockNo='%s',version = version+1,
                parentID = %d, parentName = '%s', parentCode = '%s'
                WHERE code='%s' ''' % (name,stockNo,parentId,parentName,parentCode,code)
            result = util.DbUtil.executeUpdate(updateSql)
            if(result < 1):
                insertSql = '''INSERT INTO `stockdata`.`csrcmappingdata` (name,code,stockNo,parentID,parentName,parentCode) 
                    VALUES ('%s','%s','%s',%d,'%s','%s') ''' % (name,code,stockNo,parentId,parentName,parentCode)
                util.DbUtil.executeUpdate(insertSql)
                rowIdx += 1
    print("SCRC %s data is done!" % (parentName)) 