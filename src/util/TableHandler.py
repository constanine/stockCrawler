import util.DbUtil

__createStockInfoSql  = '''
    CREATE TABLE `stockdata`.`stockinfo` (
        `id` INT NOT NULL auto_increment,
        `name` VARCHAR(45) NULL,
        `code` VARCHAR(10) NULL,
        `stockNo` VARCHAR(10) NULL,
        `version`INT NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`)
    )
'''

__createCSRCTypeDataSql = '''
    CREATE TABLE `stockdata`.`csrctypedata` (
        `id` INT NOT NULL auto_increment,
        `name` VARCHAR(45) NULL,
        `code` VARCHAR(10) NULL,
        `typeno` VARCHAR(10) NULL,
        `firstPinYin` VARCHAR(4) NULL,
        `version`INT NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`)
    )
'''

__createQQIndTypeDataSql = '''
    CREATE TABLE `stockdata`.`qqindsttypedata` (
        `id` INT NOT NULL auto_increment,
        `name` VARCHAR(45) NULL,
        `code` VARCHAR(10) NULL,
        `typeno` VARCHAR(10) NULL,
        `firstPinYin` VARCHAR(4) NULL,
        `version`INT NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`)
    )
'''

__createCSRCMappingDataSql = '''
    CREATE TABLE `stockdata`.`csrcmappingdata` (
        `id` INT NOT NULL auto_increment,
        `code` VARCHAR(10) NULL,
        `name` VARCHAR(45) NULL,
        `stockNo` VARCHAR(10) NULL,
        `parentID` INT NULL,
        `parentName` VARCHAR(45) NULL,
        `parentCode` VARCHAR(10) NULL,
        `version`INT NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`)
    )
'''

__createQQIndstueryMappingDataSql = '''
    CREATE TABLE `stockdata`.`qqindstmappingdata` (
        `id` INT NOT NULL auto_increment,
        `code` VARCHAR(10) NULL,
        `name` VARCHAR(45) NULL,
        `stockNo` VARCHAR(10) NULL,
        `parentID` INT NULL,
        `parentName` VARCHAR(45) NULL,
        `parentCode` VARCHAR(10) NULL,
        `version`INT NOT NULL DEFAULT 1,
        PRIMARY KEY (`id`)
    )
'''

__createXueQiuExactStockDataSql = '''
    CREATE TABLE `stockdata`.`xueqiuexactstockdata` (
        `code` VARCHAR(10) NULL,
        `stockNo` VARCHAR(10) NULL,
        `volume` INT NULL,
        `openP` INT NULL,
        `closeP` INT NULL,
        `highP` INT NULL,
        `lowP` INT NULL,
        `priceChange` INT NULL,
        `percent` INT NULL,
        `turnrate` INT NULL,
        `ma5` INT NULL,
        `ma10` INT NULL,
        `ma20` INT NULL,
        `ma30` INT NULL,
        `dif` INT NULL,
        `dea` INT NULL,
        `macd` INT NULL,
        `lot_volume` INT NULL,
        `tranTimestamp` INT NULL,
        `tranDate` VARCHAR(12)
        PRIMARY KEY (`code`,`tranDate`)
    )
'''

__createWangYiExactStockDataSql = '''
    CREATE TABLE `stockdata`.`wangyiexactstockdata`` (
        `code` VARCHAR(10) NULL,
        `stockNo` VARCHAR(10) NULL,        
        `openP` INT NULL,
        `closeP` INT NULL,
        `highP` INT NULL,
        `lowP` INT NULL,
        `priceChange` INT NULL,
        `percent` INT NULL,
        `turnrate` INT NULL,
        `volume` INT NULL,
        `volumeAmout` INT NULL,
        `totalMarketValue` INT NULL,
        `currentValue` INT NULL,
        `volumeHand` INT NULL,
        `tranTimestamp` INT NULL,
        `tranDate` VARCHAR(12)
        PRIMARY KEY (`code`,`tranDate`)
    )
'''

def __getCreateTableSql(tableName):
    if tableName == "stockinfo":
        return __createStockInfoSql
    elif tableName == "csrctypedata":
        return __createCSRCTypeDataSql
    elif tableName == "qqindsttypedata":
        return __createQQIndTypeDataSql
    elif tableName == "csrcmappingdata":
        return __createCSRCMappingDataSql
    elif tableName == "qqindstmappingdata":
        return __createQQIndstueryMappingDataSql
    elif tableName == "xueqiuexactstockdata":
        return __createXueQiuExactStockDataSql
    elif tableName == "wangyiexactstockdata":
        return __createWangYiExactStockDataSql
        
def __checkTableIsExistSql(tableName):
    checkSql = '''SELECT table_name,TABLE_SCHEMA 
         FROM information_schema.TABLES 
         WHERE table_name=\''''+tableName+'''\' and TABLE_SCHEMA='stockdata'
    '''
    return checkSql

def checkTableIsExist(tableName):
    checkSql = __checkTableIsExistSql(tableName)
    reulsts = util.DbUtil.executeQuery(checkSql)
    if len(reulsts) > 0 :
        print("table "+tableName +" is Exist!")

def __checkTableIsExistAndInit(tableName):
    checkSql = __checkTableIsExistSql(tableName)
    reulsts = util.DbUtil.executeQuery(checkSql)
    if len(reulsts) < 1 :
        util.DbUtil.executeUpdate(__getCreateTableSql(tableName))
    else :
        print("table "+tableName +" is Exist!")

def dbInit():
    __checkTableIsExistAndInit("stockinfo")
    __checkTableIsExistAndInit("csrctypedata")
    __checkTableIsExistAndInit("qqindsttypedata")
    __checkTableIsExistAndInit("csrcmappingdata")
    __checkTableIsExistAndInit("qqindstmappingdata")
    __checkTableIsExistAndInit("xueqiuexactstockdata")
    __checkTableIsExistAndInit("wangyiexactstockdata")
    
    