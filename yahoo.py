#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from time import strftime, gmtime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from termcolor import colored
from yahoo_finance import Share

class yahooGetInfo(object):
	def __init__(self,stock_number='1101'):
		self.url = 'https://tw.stock.yahoo.com/q/q'
		self.stock_number = stock_number
		self.time = None
		self.final_price = None
		self.buy_price = None
		self.sell_price = None
		self.number = None
		self.yesterday_price = None
		self.open_price = None
		self.high_price = None
		self.low_price = None
		
		params={
    		's': '1101'
		}
		params['s'] = self.stock_number
		headers={
    		'Host': 'tw.stock.yahoo.com',
    		'Connection': 'keep-alive',
    		'Accept': 'text/plain, */*; q=0.01',
    		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    		'Accept-Encoding': 'gzip, deflate, sdch',
    		'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2'
		}
		r = requests.get(self.url,params=params,headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		rows = soup.find_all('td', {'align':'center', 'bgcolor': '#FFFfff'})
		for row in rows:
			#print(row.get_text())
			pass
		self.time = str(rows[0].get_text())
		self.final_price = float(str(rows[1].get_text()))
		try:
			self.buy_price = float(str(rows[2].get_text()))
		except ValueError:
			pass
		#self.sell_price = float(rows[3].get_text())
		#self.number = int(str(rows[5].get_text()).replace(",", ""))
		#self.yesterday_price = float(rows[6].get_text())
		#self.open_price = float(rows[7].get_text())
		#self.high_price = float(rows[8].get_text())
		#self.low_price = float(rows[9].get_text())
		#print("時間 收盤")
		#print("-----------------")
		#print("{} {}".format(self.time,self.final_price))

class yahooGetDiv(object):
	def __init__(self,stock_number='1101'):
		self.url = 'https://tw.stock.yahoo.com/d/s/dividend_'+stock_number+'.html'
		self.div=[]
		headers={
    		'Host': 'tw.stock.yahoo.com',
    		'Connection': 'keep-alive',
    		'Accept': 'text/plain, */*; q=0.01',
    		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    		'Accept-Encoding': 'gzip, deflate, sdch',
    		'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2'
		}
		r = requests.get(self.url,headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		rows = soup.find_all('tr', {'bgcolor':'#FFFFFF'})
		for row in rows:
			llls = row.find_all('td')
			tmp_array=[]
			for lll in llls:
				tmp_array.append(float(lll.get_text()))
			#print(tmp_array)
			self.div.append(tmp_array)
		#print(self.div)
	def cashAverage(self,year=3):
		sumadd = 0
		for i in range(0,year,1):
			#print(i)
			sumadd += self.div[i][1]
		return (sumadd/year)

#===========================================================================================================
class yahooHistory(object):
	def __init__(self,stock_number=1101,start_day='2000-01-01'):
		self.stock_number = stock_number
		self.start_day = start_day
		self.fee = 0.0007125 #手續費
		self.tax = 0.003 #稅金
	
	def getStockNumber(self):
		return self.stock_number
	def getStartDay(self):
		return self.start_day
	def getHistoryData(self):
		stock = Share(str(self.stock_number)+'.TW')
		today = time.strftime("%Y-%m-%d")
		self.data = stock.get_historical(self.start_day, str(today))
		self.totalDays = len(self.data)
		return self.data
	def getAverage(self,averageDay):
		days = len(self.data) #期間總天數
		self.averageRet = []
		for i in range(0,days-averageDay,1):
			sum = 0
			for k in range(0,averageDay):
				sum += float(self.data[i+k]['Close'])
			tmpdict = {'Data': self.data[i]['Date'],'Close':float(self.data[i]['Close']),'AvgClose': sum/averageDay,'Diff':float(self.data[i]['Close'])-sum/averageDay}
			self.averageRet.append(tmpdict)
		return self.averageRet
	def getAverageClose(self,days):
		ret = self.getAverage(days);
		sum = 0
		for x in range(0,days-1,1):
			sum += ret[x]['AvgClose']
		#sum += getNowClose(self.stock_number)
		sum += yahooGetInfo(stock_number=self.stock_number).final_price
		return sum/days

def getNowClose(stock_number):
	stock = Share(str(stock_number)+'.tw')
	stock.refresh()
	return float(stock.get_price())

def getProfitAvgBuyAndSell(history,stock_number,start_day,avg_num,momey):
	#history = yahooHistory(stock_number,start_day)
	#history.getHistoryData()
	avg = history.getAverage(avg_num)
	avg.reverse()
	buyCnt = 0
	sellCnt = 0
	profit = 0
	for x in range(1,len(avg),1):
		yesterdayDiff = avg[x-1]['Diff']
		nowDiff = avg[x]['Diff']
		nowClose = avg[x]['Close']
		if yesterdayDiff <= 0 and nowDiff > 0 :
			#print(x,avg[x]['Data'],nowClose,"買進")
			buyCnt += 1
			profit -= (nowClose * 1000 * (1+history.fee))
		elif yesterdayDiff >= 0 and nowDiff < 0 :
			#print(x,avg[x]['Data'],nowClose,"賣出")
			sellCnt += 1
			profit += nowClose * 1000
			profit -= nowClose * 1000 * history.tax

	print("=============================================================================")
	print("股票代號 : ",history.stock_number,",均線 : ",avg_num)
	print("買進次數 : ",buyCnt,", 賣出次數 : ",sellCnt)
	print("損益 : ",profit,",總天數 : ",history.totalDays)
	print("年化報酬率 : ",profit/momey*history.totalDays/365,"%")

def getProfitAvgBuyOnly(history,stock_number,start_day,avg_num):
	#history = yahooHistory(stock_number,start_day)
	#history.getHistoryData()
	avg = history.getAverage(avg_num)
	avg.reverse()
	buyCnt = 0
	sellCnt = 0
	profit = 0
	cost = 0
	nowValue = 0
	for x in range(1,len(avg),1):
		yesterdayDiff = avg[x-1]['Diff']
		nowDiff = avg[x]['Diff']
		nowClose = avg[x]['Close']
		if yesterdayDiff <= 0 and nowDiff > 0 :
			#print(x,avg[x]['Data'],nowClose,"買進")
			buyCnt += 1
			cost += (nowClose * 1000 * (1+history.fee))
	nowValue = float(history.data[0]['Close'])*buyCnt*1000
	profit = nowValue - cost
	perYearBuyCnt = buyCnt/(history.totalDays/365)
	print("=============================================================================")
	print("股票代號 : ",history.stock_number,",均線 : ",avg_num)
	print("買進次數 : ",buyCnt,", 賣出次數 : ",sellCnt)
	print("市值 : ",nowValue)
	print("總成本 : ",cost,",總天數 : ",history.totalDays,",每年買進次數 : ",perYearBuyCnt)
	print("浮動損益 : ",profit,",浮動年化報酬率 : ",profit/cost*history.totalDays/365,"%")

def getProfitAvgDeviateBuyOnly(history,stock_number,start_day,avg_num,deviate):
	#history = yahooHistory(stock_number,start_day)
	#history.getHistoryData()
	avg = history.getAverage(avg_num)
	avg.reverse()
	buyCnt = 0
	sellCnt = 0
	profit = 0
	cost = 0
	nowValue = 0
	for x in range(1,len(avg),1):
		nowClose = avg[x]['Close']
		avgClose = avg[x]['AvgClose']
		if ( (avgClose - nowClose)/avgClose ) >= (deviate/100) :
			buyCnt += 1
			cost += (nowClose * 1000 * (1+history.fee))
	nowValue = float(history.data[0]['Close'])*buyCnt*1000
	profit = nowValue - cost
	perYearBuyCnt = buyCnt/(history.totalDays/365)
	if perYearBuyCnt < 20 :
		print("=============================================================================")
		print("股票代號 : ",history.stock_number,",均線 : ",avg_num,",乖離率 : ",deviate,"%")
		print("買進次數 : ",buyCnt,", 賣出次數 : ",sellCnt)
		print("市值 : ",nowValue)
		print("總成本 : ",cost,",總天數 : ",history.totalDays,",每年買進次數 : ",perYearBuyCnt)
		print("浮動損益 : ",profit,",浮動年化報酬率 : ",profit/cost*history.totalDays/365,"%")

def getProfitInit(stock_number,start_day):
	history = yahooHistory(stock_number,start_day)
	history.getHistoryData()
	return history

def main():
	history = getProfitInit('0050','2008-01-01')
	for x in range(20,100,1):
		for y in range(4,8,1):
			getProfitAvgDeviateBuyOnly(history,'0050','2008-01-01',x,y)

	#history = getProfitInit('2330','2000-01-01')
	#for x in range(20,121,1):
	#	getProfitAvgBuyOnly(history,'2330','2000-01-01',x)
	pass

if __name__ == '__main__':
	main()
