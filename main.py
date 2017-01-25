
import time
from time import strftime, gmtime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from termcolor import colored
from yahoo import yahooGetDiv, yahooGetInfo

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

