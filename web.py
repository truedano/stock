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

@app.route('/stocklist', methods=['GET'])
def stocklist():
	with open('stocklist.txt') as f:
	    content = f.readlines()
	content = [x.strip() for x in content]
	return jsonify(stocklist = content)

@app.route('/redirect', methods=['GET'])
def redirect():
	page = request.args.get('page')
	return render_template(page+'.html')

def main():
	app.run('0.0.0.0')

if __name__ == '__main__':
	main()

