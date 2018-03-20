#coding=utf-8
import KBM
import AO
import AC
import datasv

if __name__=='__main__':
	#请替换EDB中的指标ID或目录中的excel文件名
	#example KBM.run(u"S0059749") 
	#or      KBM.run(u"测试.xls")
	a=input("Please enter the Index ID:")
	b=input("Please enter frequency(D/W/M):")
	df=datasv.tran_df(code=str(a),freq=str(b))
	KBM.plot(df)
	AO.plot(df)
	AC.plot(df)