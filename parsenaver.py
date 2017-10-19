from bs4 import BeautifulSoup
import requests
import pymysql

import os
import sys
import io
import myTools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def parseAhanja(filename):
	hanzi_id = filename
	fullpath = os.path.join(myTools.NAVER_PATH, filename)
	with open(fullpath,'r',encoding='utf-8') as fp:
		soup = BeautifulSoup(fp.read(),"html.parser")
		# parse xun and yin
		single = soup.find("dl",{"class":"single"})
		hanzi = single.find("dt").text
		print(hanzi)

		# korean中以id查看
		hasInKorean = False
		with db.cursor() as cursor:
			try:
				cursor.execute('SELECT * FROM korean WHERE id=%s',(hanzi_id))
				results = cursor.fetchall()
				for one in results:
					hasInKorean = True
					break
			except Exception as e:
				print(e)

		# 训 音;训 音
		yinxun = single.find("dd").find("strong")
		yins = str.split(yinxun.text,",")

		hyInMain = ""
		hanjas = []
		hanguls= []
		for idx,yin in enumerate(yins):
			hanja = yin[len(yin)-1]
			hangul= yin[0:len(yin)-1]
			hangul = hangul.lstrip()
			hangul = hangul.rstrip()

			hanjas.append(hanja)
			hanguls.append(hangul)
			hyInMain += hanja
			# print('{0}: '.format(idx) + "hangul = " + hangul + ";hanja = " + hanja)

		# korean中创建id的条目 尚未加入 汉字 和 拉丁转写
		if not hasInKorean :
			with db.cursor() as cursor:
				try:
					if len(hanjas)==1 :
						cursor.execute('INSERT INTO korean (id, hanzi, xun1, hangul1, zx1) VALUES (%s,%s,%s,%s,%s)',(hanzi_id,hanzi,hanguls[0],hanja[0],""))
					if len(hanjas)==2 :
						cursor.execute('INSERT INTO korean (id, hanzi, xun1, hangul1, zx1, xun2, hangul2, zx2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(hanzi_id,hanzi,hanguls[0],hanja[0],"",hanguls[1],hanja[1],""))
					if len(hanjas)>=3 :
						cursor.execute('INSERT INTO korean (id, hanzi, xun1, hangul1, zx1, xun2, hangul2, zx2, xun3, hangul3, zx3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(hanzi_id,hanzi,hanguls[0],hanja[0],"",hanguls[1],hanja[1],"",hanguls[2],hanja[2],""))
				except Exception as e:
					print(e)
			

		# maintable中的hy 把 音 连成一串
		changeInMain= 'UPDATE maintable SET hy=%s WHERE id=%s'
		with db.cursor() as cursor:
			try:
				cursor.execute(changeInMain,(hyInMain,hanzi_id))
			except Exception as e:
				print(e)

			db.commit()


		# parse mean in korean and search in chinese

def parseAllHanja():
	# for test
	test_max = 1
	test_num = 1
	for f in os.listdir(myTools.NAVER_PATH):
		# for test
		if test_num>test_max:
			break
		parseAhanja(f)
		# for test
		test_num += 1


db = pymysql.connect(**myTools.MYSQL_CONFIG)
parseAllHanja()
db.close()