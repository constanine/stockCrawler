# stockCrawler
crawler stock data for analysis

# 改数据爬取分为3个部分
   1. 通过QQ股票的接口,获取了沪深股票基础数据,近1800个股
   2. 通过QQ股票的接口,获取了沪深股票所属板块,按行业标准分`SCRC`,按QQ标准分`QQIndustry`
   3. 确切的个股日K线,通过3个接口获取,以比对3个接口数据准确性,以Merger和数据有效性,
       3.1 QQ个股日K线 http://data.gtimg.cn/flashdata/hushen/daily/{00}/{sz000750}.js?visitDstTime=1
	   3.2 网易个股接口 http://quotes.money.163.com/service/chddata.html?code=1002566&start=20150104&end=20160108
	   3.3 雪球个股接口 https://xueqiu.com/stock/forchartk/stocklist.json?symbol=SH600756&period=1day&type=before&begin=1478620800000&end=1510126200000&_=1510126200000
	   
# TODO,盘口数据获取,KDJ,MACD的计算