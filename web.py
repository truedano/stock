#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from time import strftime, gmtime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from termcolor import colored
from yahoo import yahooGetDiv, yahooGetInfo
from flask import Flask, request, render_template, jsonify, Response
import json

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('main_page.html')

@app.route('/price', methods=['GET'])
def price():
	stockNum = request.args.get('stockNum')
	info = yahooGetInfo(stockNum)
	return jsonify(final_price=info.final_price)

@app.route('/perdiv', methods=['GET'])
def perdiv():
	stockNum = request.args.get('stockNum')
	d = yahooGetDiv(stockNum)
	perdiv = d.cashAverage(5)
	return jsonify(perdiv=perdiv)

@app.route('/setting', methods=['GET','POST'])
def setting():
	if request.method == 'GET':
		with open('config.json') as data_file:    
			data = json.load(data_file)
		return jsonify(data)
	else:
		with open('config.json','w',encoding = 'UTF-8') as file:
			file.write(request.data.decode("utf-8"))
		file.close()
		return render_template('main_page.html')

def main():
	app.run('0.0.0.0')

if __name__ == '__main__':
	main()

