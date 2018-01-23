from exactData import XueQiuExactStockDataUtil,WangYiExactStockDataUtil

def exactDataInit():
    XueQiuExactStockDataUtil.initStockInfoDataFromXQ()
    WangYiExactStockDataUtil.initStockInfoDataFromWY()