import backtrader 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import math
from matplotlib.dates import  warnings 


class AllSizer(backtrader.Sizer):
    def _getsizing(self, comminfo,cash,data,isbuy):
        if isbuy:
            return math.floor(cash/data.high)
        else:
            return self.broker.getposition(data)


        
     
    
class SmaCross(backtrader.SignalStrategy):
    def __init__(self):
        sma10 = backtrader.ind.SMA(period=10)
        sma30 = backtrader.ind.SMA(period=30)
        crossover = backtrader.ind.CrossOver(sma10, sma30)
        self.signal_add(backtrader.SIGNAL_LONG, crossover)
            
        self.setsizer(AllSizer())

z=input("請輸入股票代號(台股請加.TW)") 
     
cerebro = backtrader.Cerebro()            
data = backtrader.feeds.YahooFinanceData(
    dataname= z ,
    fromdate=datetime.strptime(input("請輸入起始日期"),'%Y,%m,%d'),
    todate=datetime.strptime(input("請輸入結束日期"),'%Y,%m,%d'))
x=int(input("請輸入資產"))
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)
cerebro.broker.set_cash(cash=x)
cerebro.addanalyzer(backtrader.analyzers.SharpeRatio,_name = "SR",timeframe=backtrader.TimeFrame.Years)
cerebro.addanalyzer(backtrader.analyzers.DrawDown,_name = "DW",)
cerebro.addanalyzer(backtrader.analyzers.TimeReturn,_name = "TR",timeframe=backtrader.TimeFrame.Months)
results = cerebro.run()
print("Sharpe Ratio:" , results[0].analyzers.SR.get_analysis())
print("Max DrawDown:" , results[0].analyzers.DW.get_analysis().max)
for date, value in results[0].analyzers.TR.get_analysis().items():
    print(date,value)

cerebro.plot()

plt.savefig("C:\\Users\\ASUS\\Desktop\\py\\data\\figure.png")

import os
os.system('pause')