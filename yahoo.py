#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from time import strftime, gmtime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from termcolor import colored

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

def main():
	with open('stocklist.txt') as f:
	    content = f.readlines()
	content = [x.strip() for x in content]

	while True:
		print("=================================================")
		for c in content:
			info = yahooGetInfo(c)
			div = yahooGetDiv(c)
			perdiv = div.cashAverage(5)
			if info.final_price <= perdiv*16:
				print(colored("{} : ==={} {} {}=== , {}".format(c,perdiv*16,perdiv*20,perdiv*32,info.final_price),'cyan'))
			elif info.final_price >= perdiv*20:
				print(colored("{} : ==={} {} {}=== , {}".format(c,perdiv*16,perdiv*20,perdiv*32,info.final_price),'red'))
			else:
				print("{} : ==={} {} {}=== , {}".format(c,perdiv*16,perdiv*20,perdiv*32,info.final_price))
		time.sleep(5)

if __name__ == '__main__':
	main()
