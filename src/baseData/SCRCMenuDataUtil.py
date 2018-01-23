import requests
import importlib
import json
import sys
importlib.reload(sys)
import util.DbUtil

def getCSRCData():
    target = 'http://stockapp.finance.qq.com/mstats/menu_childs.php?id=bd_csrc'
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
        updateSql = '''UPDATE `stockdata`.`csrctypedata` SET name='%s',typeno='%s',firstPinYin='%s',version = version+1
            WHERE code='%s' ''' % (name,typeno,firstPinYin,typekey)
        result = util.DbUtil.executeUpdate(updateSql)
        if(result < 1):
            insertSql = '''INSERT INTO `stockdata`.`csrctypedata` (name,code,typeno,firstPinYin)
                    VALUES 
                    ('%s','%s','%s','%s')''' % (name,typekey,typeno,firstPinYin)
            util.DbUtil.executeUpdate(insertSql)
    print("CSRCData data is done!")