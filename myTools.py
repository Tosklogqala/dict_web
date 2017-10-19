from bs4 import BeautifulSoup
import requests
import pymysql

import hashlib
import os
import sys
import io

YTENX_FILE_NAME = 'ytenx_gy_xiaoyun_{0}'

# 现在这个路径与调用的py所在的路径有关。以后要改成myTools所在的路径
PROJ_PATH = sys.path[0]
YTENX_PATH= os.path.join(PROJ_PATH,"ytenx")
NAVER_PATH= os.path.join(PROJ_PATH,"naver")
HANVIET_PATH=os.path.join(PROJ_PATH,"hanviet")

MYSQL_CONFIG = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'123',
          'db':'cl',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }

# class myTools():
	# @staticmethod
def getUniStr(hanzi):
	if hanzi>='\4e00' and hanzi<='\u9fff' :
		return hanzi.encode("unicode-escape").decode("ascii").replace('\\u','')
	else:
		return '0'


def getMd5Str(_str):
	hs = hashlib.md5()
	hs.update(_str.encode('utf-8'))
	return hs.hexdigest()

	# @staticmethod
def hasFile(root,fileName):
	for f in os.listdir(root):
		# if os.path.isfile(f) :
		if f==fileName:
			return True
	return False

	# @staticmethod
def hasDict(root,dictName):
	for f in os.listdir(root):
		if not os.path.isfile(f) :
			if f==dictName:
				return True
	return False


def writeResWeb(dictName,fileName,resWeb=""):
	if hasFile(dictName,fileName):
		return

	newfile = os.path.join(dictName,fileName)
	try:
		fp = open(newfile,'w',encoding='utf-8')
		fp.write(resWeb)
	except Exception as e:
		print(e)
		os.remove(newfile)
	finally:
		fp.close()
