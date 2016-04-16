from __future__ import division
from bs4 import BeautifulSoup, Comment
import requests
import json
import sys
import csv
import math
import re
import pymysql
from mailer import Mailer
from mailer import Message
import time
import os
from unidecode import unidecode
field={}
j=0
csv_columns = ["url", "Category Name"]
currentPath = os.getcwd()
csv_file = "Souq_cat.csv"
data={}
def WriteDictToCSV(dict_data):
	global csv_columns
	global csv_file
	global j
	try:
		with open(csv_file, 'a+') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=csv_columns)
			if j == 0:
				writer.writeheader()
				j=1
			
			for data in dict_data:
				writer.writerow(data)
				
		return 1
	except TypeError as e:
		print (str(e)+"3")
	except IOError as e:
		print ("I/O error({0}): {1}".format(e.errno, e.strerror)+"3")
		print (e)
	except ValueError as e:
		print ("Could not convert data to an integer.")
		print (str(e)+"3")
	except:
		print ("Unexpected error:", sys.exc_info()[0]+"3")
		return 0
def souqCatScrape(url):
	global data
	r=requests.get(url)
	html = r.text.encode("utf-8")
	pp = BeautifulSoup(html, "html.parser")
	names = pp.find('div', attrs={'class':'small-12 large-12 columns'})
	titles = names.findAll('h3' , attrs={"class":"shop-all-title"})
	links=	names.findAll('div' , attrs={"class":"grouped-list"})
	i=0
	for link in links:
		cat = link.findAll("a")
		for ca in cat:
			if ca.get('href'):
				print(unidecode(titles[i].text)+"/"+unidecode(ca.text.replace(",","")) +";" +ca['href'])
		i+=1
	return	
souqCatScrape('http://uae.souq.com/ae-en/shop-all-categories/c/')