
# coding: utf-8
# In[1]:
import xlrd
from xlrd import xldate_as_tuple
from pyecharts import Page
from pyecharts import Line,Grid,Bar,Overlap,Kline
from WindPy import w
from datetime import datetime
import talib
import math
import numpy as np
import pandas as pd
import os

# In[2]:
def plot(df):
	kl=df.copy()
	#计算指标
	macd = talib.MACD(np.array(kl['CLOSE']), fastperiod=12, slowperiod=26, signalperiod=9)
	boll = talib.BBANDS(np.array(kl['CLOSE']), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
	#绘图
	page = Page(page_title='KBM')
	kline = Kline()
	kline.add('', list(kl.index), [list(kl[['OPEN', 'CLOSE', 'LOW', 'HIGH']].iloc[i,].values) for i in range(len(kl))],is_datazoom_show=True, datazoom_xaxis_index=[0, 1], datazoom_type="both", is_xaxislabel_align=True,tooltip_axispointer_type="cross")
	line = Line(' ')
	line.add('upperband', list(kl.index), boll[0].tolist())
	line.add('middleband', list(kl.index), boll[1].tolist())
	line.add('lowerband', list(kl.index), boll[2].tolist())
	overlap1 = Overlap()
	overlap1.add(kline)
	overlap1.add(line)
	# line=Line(' ',width=1800,height=600)
	# line.add('中债国债到期收益率:10年',df.Times,df.Data[0], mark_line=0,is_datazoom_show=True,datazoom_xaxis_index=[0, 1],is_xaxislabel_align=True)
	line2 = Line(' ')
	line2.add('MACD', list(kl.index), macd[0].tolist())
	line2.add('MACDsignal',list(kl.index), macd[1].tolist(), is_datazoom_show=True,tooltip_axispointer_type="cross")
	bar = Bar(' ')
	macd2 = macd[2].tolist()
	macdhistUp = []
	macdhistDown = []
	for i in range(len(macd2)):
		if (macd2[i] > 0):
			macdhistUp.append(macd2[i])
			macdhistDown.append(0)
		else:
			macdhistUp.append(0)
			macdhistDown.append(macd2[i])
	# bar.add('MACDhist',klt,macd[2].tolist(),is_datazoom_show=True,legend_top='65%')
	bar.add('MACDhistUp', list(kl.index), macdhistUp, is_datazoom_show=True, legend_top='65%', label_color=['#ff0000'])
	bar.add('MACDhistDown', list(kl.index), macdhistDown, is_datazoom_show=True, legend_top='65%', label_color=['#00ff00'])
	overlap = Overlap()
	overlap.add(bar)
	overlap.add(line2)
	grid = Grid(width=1920, height=950)
	grid.add(overlap1, grid_bottom='40%')
	grid.add(overlap, grid_top='70%')
	# page.add(line)
	# page.add(overlap)
	page.add(grid)
	path=os.path.abspath('.')
	page.render(path+'\\plot\\KBM.html')
