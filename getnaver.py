from bs4 import BeautifulSoup
import requests
import urllib.parse
import pymysql

import myTools

import time
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

naver = "http://hanja.naver.com/hanja"

def getAhanja(hanzi):
	filename = myTools.getUniStr(hanzi)
	if filename == '0':
		return

	if myTools.hasFile(myTools.NAVER_PATH,filename):
		return

	try:
		response = requests.get(naver,params={"q":hanzi,"cp_code":0,"sound_id":0})
		myTools.writeResWeb(myTools.NAVER_PATH,filename,response.text)
	except Exception as e:
		print(e)
	finally:
		time.sleep(1)


def getAllHanja():
	# for test
	# test_max = 1
	# test_num = 1

	if not myTools.hasDict(myTools.PROJ_PATH,"naver"):
		os.mkdir("naver")

	sql = 'SELECT hanzi FROM maintable'

	db = pymysql.connect(**myTools.MYSQL_CONFIG)
	with db.cursor() as cursor:
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				# for test
				# if test_num>test_max:
				# 	break
				hanzi = row['hanzi']
				getAhanja(hanzi)
				# for test
				# test_num += 1

		except Exception as e:
			print(e)

	db.close()


def main():
	getAllHanja()


if __name__ == '__main__':
    main()


