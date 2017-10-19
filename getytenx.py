from bs4 import BeautifulSoup
import requests
import hashlib
import time
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


import myTools




# 写到/ytenx/文件夹下
# def writeResWeb(fileName="",resWeb=""):
# 	if myTools.hasFile(YTENX_PATH,fileName):
# 		return

# 	newfile = os.path.join(YTENX_PATH,fileName)
# 	try:
# 		fp = open(newfile,'w',encoding='utf-8')
# 		fp.write(resWeb)
# 	except Exception as e:
# 		print(e)
# 		os.remove(newfile)
# 	finally:
# 		fp.close()


# 获取ytenx网页
def getYtenx():
	if not myTools.hasDict(myTools.PROJ_PATH,"ytenx"):
		os.mkdir("ytenx")

	urlhead = 'http://ytenx.org/kyonh/sieux/'
	for idx in range(1,3875):
		urltext = urlhead+'{0}'.format(idx)+'/'
		filename = myTools.YTENX_FILE_NAME.format(idx)
		if myTools.hasFile(myTools.YTENX_PATH,filename):
			continue

		try:
			response = requests.get(urltext)
			# soup = BeautifulSoup(response.text,"html.parser")
			myTools.writeResWeb(myTools.YTENX_PATH,filename,response.text)
		except Exception as e:
			print(e)
		finally:
			time.sleep(2)


def main():
	# writeResWeb("test_bin","i am test_bin")
	getYtenx()
	# print(ytenx_path)
	# print(getMd5Str('http://ytenx.org/kyonh/sieux/1/'))

if __name__ == '__main__':
    main()