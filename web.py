#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from time import strftime, gmtime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from termcolor import colored
from yahoo import yahooGetDiv, yahooGetInfo
from flask import Flask, request, render_template, jsonify
import thread

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('main_page.html')

@app.route('/price', methods=['GET'])
def price():
	stockNum = request.args.get('stockNum')
	info = yahooGetInfo(stockNum)
	return jsonify(final_price=info.final_price)

@app.route('/div', methods=['GET'])
def div():
	stockNum = request.args.get('stockNum')
	d = yahooGetDiv(stockNum)
	perdiv = d.cashAverage(5)
	return jsonify(perdiv=perdiv)

def main():
	app.run('0.0.0.0')

if __name__ == '__main__':
	main()

