from WindPy import w
import numpy as np
import pandas as pd


def tran_df(code="M1000166", start="", end="",freq="W"):
	return data_from_wind(code, freq, start, end)


def data_from_wind(code, freq,start="", end=""):
	w.start()
	if freq=='D':
		df=w.wsd(code, "OPEN,HIGH,LOW,CLOSE", start, end, "")
	else:
		df = w.edb(code, start, end, "Fill=Previous")
	w.close()
	kl=to_dataframe(df,freq)
	return kl


def to_dataframe(data,freq):
	df = pd.DataFrame((np.array(data.Data)).transpose(), index=data.Times, columns=data.Fields)
	df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df.index)))
	if freq=='D':
		kl=df.copy()
	else:
		kl = df.resample(freq).min()
		kl.columns = ['LOW']
		kl['HIGH'] = df.resample(freq).max()
		kl['OPEN'] = df.resample(freq).first()
		kl['CLOSE'] = df.resample(freq).last()
	kl = kl.dropna(axis=0)
	return kl
