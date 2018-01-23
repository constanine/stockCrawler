import requests
import json
import importlib
import sys
importlib.reload(sys)
import util.DbUtil

def getQQIndustryData():
    target = 'http://stockapp.finance.qq.com/mstats/menu_childs.php?id=bd_ind'
    resp = requests.get(url = target)
    content = resp.text
    decodeContent = content.encode('latin-1').decode('unicode_escape')
    data = json.loads(decodeContent)
    typekeys = data.keys()
    for typekey in typekeys:
        typeInfo = data[typekey]
        name = typeInfo['t']
        typeno = typeInfo['clk']
        typeno = typeno[3:len(typeno)]
        firstPinYin = typeInfo['fl']
        updateSql = '''UPDATE `stockdata`.`qqindsttypedata` SET name='%s',typeno='%s',firstPinYin='%s',version = version+1
            WHERE code='%s' ''' % (name,typeno,firstPinYin,typekey)
        result = util.DbUtil.executeUpdate(updateSql)
        if(result < 1):
            insertSql = '''INSERT INTO `stockdata`.`qqindsttypedata` (name,code,typeno,firstPinYin)
                    VALUES 
                    ('%s','%s','%s','%s')''' % (name,typekey,typeno,firstPinYin)
            util.DbUtil.executeUpdate(insertSql)
    print("QQIndustryData data is done!")