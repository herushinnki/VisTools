
from pyecharts import Page
from pyecharts import Line, Grid, Bar, Overlap, Kline
from WindPy import w
from datetime import datetime
import talib
import math
import numpy as np
import pandas as pd
import os

def plot(df):
	kl=df.copy()
	kl['MID'] = (kl['HIGH'] + kl['LOW']) / 2
	kl['AG13'] = kl['MID'].rolling(window=13).mean()
	kl['AG8'] = kl['MID'].rolling(window=8).mean()
	kl['AG5'] = kl['MID'].rolling(window=5).mean()
	kl['SMA5']=kl['MID'].rolling(window=5).mean()
	kl['SMA34']=kl['MID'].rolling(window=34).mean()
	kl['AO']=kl['SMA5']-kl['SMA34']
	kl=kl[20:]
	for i in range(2,len(kl['MID'])):
		kl.ix[i,'AG13']=(kl.ix[i-1,'AG13']*12+(kl.ix[i,'HIGH']+kl.ix[i,'LOW'])/2)/13
		kl.ix[i, 'AG8'] = (kl.ix[i - 1, 'AG8'] * 7 + (kl.ix[i, 'HIGH'] + kl.ix[i, 'LOW']) / 2) / 8
		kl.ix[i, 'AG5'] = (kl.ix[i - 1, 'AG5'] * 4 + (kl.ix[i, 'HIGH'] + kl.ix[i, 'LOW']) / 2) / 5
	kl['AG13'] = kl['AG13'].shift(8)
	kl['AG8'] = kl['AG8'].shift(5)
	kl['AG5'] = kl['AG5'].shift(3)
	kl = kl.where(kl.notnull(), 0)
	kl['GTUP'] = abs(kl['AG13'] - kl['AG8'])
	kl['GTDOWN'] = abs(kl['AG8'] - kl['AG5'])
	kl['MUP']=0
	kl['MDOWN']=0
	markd=[]
	for i in range(2,len(kl['MID'])-2):
		if kl.ix[i,'HIGH']==max(kl.ix[i-2,'HIGH'],kl.ix[i-1,'HIGH'],kl.ix[i,'HIGH'],kl.ix[i+1,'HIGH'],kl.ix[i+2,'HIGH']):
			#kl.ix[i,'MUP']=1
			markd.append({"coord":[kl.index[i],kl.ix[i,'HIGH']],"name":"1"})
		if kl.ix[i,'LOW']==min(kl.ix[i-2,'LOW'],kl.ix[i-1,'LOW'],kl.ix[i,'LOW'],kl.ix[i+1,'LOW'],kl.ix[i+2,'LOW']):
			markd.append({"coord": [kl.index[i], kl.ix[i,'LOW']], "name":"2"})

	page = Page(page_title='AO')
	kline = Kline()
	kline.add('', list(kl.index), [list(kl[['OPEN', 'CLOSE', 'LOW', 'HIGH']].iloc[i,].values) for i in range(len(kl))],
			  is_datazoom_show=True, datazoom_xaxis_index=[0, 1], datazoom_type="both", is_xaxislabel_align=True,
			  tooltip_axispointer_type="cross",mark_point=markd,mark_point_symbol='circle',mark_point_symbolsize=10)
	line = Line(' ')
	line.add('JAW', list(kl.index), list(kl['AG13']), line_color=['#0000ff'], label_color=['#0000ff'])
	line.add('TEETH', list(kl.index), list(kl['AG8']), line_color=['#ff0000'], label_color=['#ff0000'])
	line.add('LIPS', list(kl.index), list(kl['AG5']), line_color=['#00ff00'], label_color=['#00ff00'])
	overlap1 = Overlap()
	overlap1.add(kline)
	overlap1.add(line)
	#gator
	# bar1 = Bar(' ')
	# bar2 = Bar(' ')
	# up = list(kl['GTUP'])
	# down = list(kl['GTDOWN'])
	# redup = []
	# greenup = []
	# reddown = []
	# greendown = []
	# for i in range(len(up)):
	# 	if (i == 0):
	# 		greenup.append(up[i])
	# 		redup.append(0)
	# 		greendown.append(-down[i])
	# 		reddown.append(0)
	# 		continue
	# 	if (up[i] > up[i - 1]):
	# 		greenup.append(up[i])
	# 		redup.append(0)
	# 	else:
	# 		greenup.append(0)
	# 		redup.append(up[i])
	# 	if (down[i] > down[i - 1]):
	# 		greendown.append(-down[i])
	# 		reddown.append(0)
	# 	else:
	# 		greendown.append(0)
	# 		reddown.append(-down[i])
	#
	# 	# bar.add('MACDhist',klt,macd[2].tolist(),is_datazoom_show=True,legend_top='65%')
	# bar1.add('GTREDUP', list(kl.index), redup, legend_top='65%', label_color=['#ff0000'])
	# bar2.add('GTREDDOWN', list(kl.index), reddown, legend_top='65%', label_color=['#00ff00'])
	# bar1.add('GTGREENUP', list(kl.index), greenup, legend_top='65%', label_color=['#ff0000'])
	# bar2.add('GTGREENDOWN', list(kl.index), greendown, legend_top='65%', label_color=['#00ff00'])
	bar1 = Bar(' ')
	bar2 = Bar(' ')
	ao=list(kl['AO'])
	aor=[]
	aog=[]
	for i in range(len(ao)):
		if (i==0):
			aor.append(ao[i])
			aog.append(0)
			continue
		if ao[i]>ao[i-1]:
			aor.append(0)
			aog.append(ao[i])
		else:
			aor.append(ao[i])
			aog.append(0)
	bar1.add('AOR', list(kl.index), aor, legend_top='65%', label_color=['#ff0000'])
	bar2.add('AOG', list(kl.index), aog, legend_top='65%', label_color=['#00ff00'])
	overlap2 = Overlap()
	overlap2.add(bar1)
	overlap2.add(bar2)
	grid = Grid(width=1920, height=950)
	grid.add(overlap1, grid_bottom='40%')
	grid.add(overlap2, grid_top='70%')
	# page.add(line)
	# page.add(overlap)
	page.add(grid)
	path=os.path.abspath('.')
	page.render(path+'\\plot\\AO.html')
