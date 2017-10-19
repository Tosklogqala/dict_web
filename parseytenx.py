from bs4 import BeautifulSoup
import requests
import pymysql

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import myTools

def parseAxiaoyun(filename):
	fullpath = os.path.join(myTools.YTENX_PATH, filename)
	with open(fullpath,'r',encoding='utf-8') as fp:
		soup = BeautifulSoup(fp.read(),"html.parser")

		gy_xiaoyun = ""
		gy_mu = ""
		gy_yun = ""
		gy_diao = ""
		gy_deng = ""
		gy_hu = ""
		xiaoyun = soup.find("div",{"class":"span4"}).find("table",{"class":"table table-bordered"})
		for entry in xiaoyun.find_all("tr"):
			dui = entry.find_all("td")
			if dui[0].text=="小韻" :
				gy_xiaoyun = dui[1].text.strip()
			if dui[0].text=="聲母" :
				gy_mu = dui[1].text.strip()
			if dui[0].text=="韻目" :
				gy_yun = dui[1].text.strip()
			if dui[0].text=="調" :
				gy_diao = dui[1].text.strip()
			if dui[0].text=="等" :
				gy_deng = dui[1].text.strip()
			if dui[0].text=="呼" :
				gy_hu = dui[1].text.strip()

		zgzz = ""
		zgys = ""
		for niyin in soup.find("div",{"class":"span3"}).find_all("table",{"class":"table table-bordered"}) :
			for entry in niyin.find_all("tr") :
				dui = entry.find_all("td")
				if dui[0].text=="鄭張尚芳" :
					zgzz = dui[1].text
				if dui[0].text=="古韻羅馬字" :
					zgys = dui[1].text

		zibiao = soup.find("table",{"class":"table table-condensed table-bordered"})
		for zi in zibiao.find_all("tr"):
			dui = zi.find_all("td")
			with db.cursor() as cursor:
				sql = 'INSERT INTO maintable (hanzi, mean, gy_xiaoyun, gy_mu, gy_yun, gy_diao, gy_deng, gy_hu, zgzz, zgys) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				try:
					cursor.execute(sql,(dui[0].text,dui[1].text.strip(), gy_xiaoyun, gy_mu, gy_yun, gy_diao, gy_deng, gy_hu, zgzz, zgys))
				except Exception as e:
					print("{0},{1}".format(dui[0].text,e))
			db.commit()


# config = {
#           'host':'127.0.0.1',
#           'port':3306,
#           'user':'root',
#           'password':'123',
#           'db':'cl',
#           'charset':'utf8mb4',
#           'cursorclass':pymysql.cursors.DictCursor,
#           }

db = pymysql.connect(**myTools.MYSQL_CONFIG)
try:
	for f in os.listdir(myTools.YTENX_PATH):
		parseAxiaoyun(f)
finally:
	db.close()