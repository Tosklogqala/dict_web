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

hanviet = "http://hanviet.org/hv_timchu_ndv.php"

def getAchuhan(hanzi):
	filename = myTools.getUniStr(hanzi)
	if filename == '0':
		return

	if myTools.hasFile(myTools.HANVIET_PATH,filename):
		return

	try:
		response = requests.get(hanviet,params={"unichar":hanzi})
		myTools.writeResWeb(myTools.HANVIET_PATH,filename,response.text)
	except Exception as e:
		print(e)
	finally:
		time.sleep(1)


def getAllChuhan():
	# for test
	test_max = 1
	test_num = 1

	if not myTools.hasDict(myTools.PROJ_PATH,"hanviet"):
		os.mkdir("hanviet")

	sql = 'SELECT hanzi FROM maintable'

	db = pymysql.connect(**myTools.MYSQL_CONFIG)
	with db.cursor() as cursor:
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				# for test
				if test_num>test_max:
					break
				hanzi = row['hanzi']
				getAchuhan(hanzi)
				# for test
				test_num += 1

		except Exception as e:
			print(e)

	db.close()


def main():
	getAllChuhan()


if __name__ == '__main__':
    main()


