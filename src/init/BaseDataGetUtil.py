from baseData import *

def baseDataInit():
    StockBaseInfoDataUtil.getStockInfoDataFromQQ()
    SCRCMenuDataUtil.getCSRCData()
    QQIndustryMenuDataUtil.getQQIndustryData()
    SCRCMappingDataUtil.getSCRCMappingData()
    QQIndstueryMappingDataUtil.getQQIndstueryMappingData()