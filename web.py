# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:27:28 2017

@author: Administrator
"""
import io
import sys
# sys.path.append("..")

from datetime import datetime
import flask
from flask import jsonify

# import pymysql
from dbModel import dbmodel
import collections
import re

import myTools
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=['GET'])
def index():
	print("index")
	# return flask.render_template('trans.html')
	return flask.render_template('dansearch.html')

@app.route('/dan',methods=['GET'])
def dan():
	print("dan")
	zi = flask.request.args["zi"]
	opt= flask.request.args["opt"]
	# print(zi+";"+opt)
	results=[]
	err=0
	if opt=="hanzi":
		err,results = danHanzi(zi)
	elif opt=="sheng":
		err,results = danSheng(zi,0)
	elif opt=="yun":
		err,results = danYun(zi,0)
	elif opt=="xiaoyun":
		err,results = danXiaoyun(zi)

	return flask.render_template('dansearch.html',err=err,results=results,opt=opt)

@app.route('/ju',methods=['GET'])
def ju():
	print("ju")
	return flask.render_template('jusearch.html')

@app.route('/sentence',methods=['POST'])
def sentence():
	print("sentence")
	# dst = flask.request.args["dstlang"]
	# src = flask.request.args["srclang"]
	# txt = flask.request.args["text"]
	netdata = flask.request.get_json()
	# print(netdata)
	txt = netdata["text"]
	src = netdata["srclang"]
	dst = netdata["dstlang"]
	print(dst+src+txt)

	trans = collections.OrderedDict()
	trans["results"]=[]
	if src=="zgys" and dst=="hanzi":
		doTranslate(txt,src,dst,trans)
	# zgys是用空格分词的，汉字尚未分成一个一个的字
	# if src=="hanzi" and dst=="zgys":
	# 	doTranslate(db,txt,src,dst,trans)

	return jsonify(trans)

def doTranslate(txt,src,dst,trans):
	try:
		session = dbmodel.getSession(myTools.SQL_URL)
		restxt= str.split(txt," ")
		for zi in restxt:
			results = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.zgys==zi).all()
			do = []
			for dan in results:
				do.append(dan.hanzi_zi)
			trans["results"].append(do)
	except Exception as e:
		print(e)
		trans={}
	finally:
		pass

	return trans

def danHanzi(zi):
	if len(zi)<1 or len(zi)>1:
		return -1,[]
	
	session = dbmodel.getSession(myTools.SQL_URL)
	zilist = session.query(dbmodel.hanzi).filter(dbmodel.hanzi.zi==zi).all()
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danSheng(zi,offset):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(myTools.SQL_URL)
	zglist = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.sheng==zi).order_by(dbmodel.zgchn.id).offset(offset).limit(10)
	zilist = []
	[zilist.append(yun.hanzi) for yun in zglist if not yun.hanzi in zilist]
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danYun(zi,offset):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(myTools.SQL_URL)
	zglist = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.yun==zi).all()
	zilist = []
	[zilist.append(yun.hanzi) for yun in zglist if not yun.hanzi in zilist]
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danXiaoyun(zi):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(myTools.SQL_URL)
	zglist = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.xiaoyun==zi).all()
	zilist = []
	[zilist.append(yun.hanzi) for yun in zglist if not yun.hanzi in zilist]
	results = parseFromZiList(zilist)
	session.close()
	return 0,results


def parseFromZiList(zilist):
	results = []
	for one in zilist:
		resultOfZi=[]
		for zgy in one.zg:
			line={}
			if len(resultOfZi)==0:
				line['zi']=one.zi
			else:
				line['zi']=""

			line['xiaoyun']	= zgy.xiaoyun
			line['fanqie'] 	= zgy.fanqie_1+zgy.fanqie_2
			line['sheng']	= zgy.sheng
			line['yun']		= zgy.yun
			line['diao']	= zgy.diao
			line['deng']	= zgy.deng
			line['hu']		= zgy.hu
			line['she'] 	= zgy.she
			line['zgzz'] 	= zgy.zgzz
			line['zgys'] 	= zgy.zgys

			resultOfZi.append(line)

		size1 = len(resultOfZi)
		for j,sgy in enumerate(one.sg):
			# 若不存在中古韻，建立上古音的行
			if size1 == 0:
				line={}
				line['shengfu'] =sgy.shengfu
				line['yunbu'] = sgy.yunbu
				line['sgzz'] = sgy.sgzz
				resultOfZi.append(line)
			else:
				# 若只有一個中古韻，一個上古音。則顯示在一行。
				# 若有多個中古韻，一個上古音。則上古音顯示在第一行
				if len(one.sg)==1:
					resultOfZi[0]['shengfu']=sgy.shengfu
					resultOfZi[0]['yunbu']=sgy.yunbu
					resultOfZi[0]['sgzz']=sgy.sgzz
				else:
					# 若存在中古韻，且有多個上古音。則能匹配的填在對應的後面。多於1條則加...
					found=False
					for x in range(0,size1):
						if resultOfZi[x]['xiaoyun']==sgy.xiaoyun:
							resultOfZi[x]['shengfu'] = safeAppend('shengfu',sgy.shengfu,resultOfZi[x])
							resultOfZi[x]['yunbu'] = safeAppend('yunbu',sgy.yunbu,resultOfZi[x])
							resultOfZi[x]['sgzz'] = safeAppend('sgzz',sgy.sgzz,resultOfZi[x])
							found=True
							break
					# 若不能匹配到中古韻。則填在第一行。多於1條則加... 有可能能匹配到第一行的顯示不出來
					if not found:
						resultOfZi[0]['shengfu'] = safeAppend('shengfu',sgy.shengfu,resultOfZi[0])
						resultOfZi[0]['yunbu'] = safeAppend('yunbu',sgy.yunbu,resultOfZi[0])
						resultOfZi[0]['sgzz'] = safeAppend('sgzz',sgy.sgzz,resultOfZi[0])

		#0行時添一行。1行時填在第一行。多行時匹配中古韻。匹配不到的都填在第一行。加..
		if len(one.py)>0:
			size2 = len(resultOfZi)
			if size2==0:
				line={}
				for pyy in one.py:
					line['pinyin'] = safeAppend('pinyin',pyy.pinyin,line)
				resultOfZi.append(line)
			elif size2==1:
				for pyy in one.py:
					resultOfZi[0]['pinyin'] = safeAppend('pinyin',pyy.pinyin,resultOfZi[0])
					pass
			elif size2>1:
				for pyy in one.py:
					found=False
					for x in range(0,size2):
						if resultOfZi[x]['xiaoyun']==pyy.xiaoyun:
							resultOfZi[x]['pinyin']=safeAppend('pinyin',pyy.pinyin,resultOfZi[x])
							found=True
							break
					if not found:
						resultOfZi[0]['pinyin'] = safeAppend('pinyin',pyy.pinyin,resultOfZi[0])

		if one.jpn_id != None:
			size3 = len(resultOfZi)
			if size3==0:
				if len(one.jp.wuhan)>0:
					line={}
					for jpwh in one.jp.wuhan:
						line['wu'] = safeAppend('wu',jpwh.wu,line)
						line['han'] = safeAppend('han',jpwh.han,line)
					resultOfZi.append(line)
			elif size3==1:
				for jpwh in one.jp.wuhan:
					resultOfZi[0]['wu'] = safeAppend('wu',jpwh.wu,resultOfZi[0])
					resultOfZi[0]['han'] = safeAppend('han',jpwh.han,resultOfZi[0])
			elif size3>1:
				for jpwh in one.jp.wuhan:
					found=False
					for x in range(0,size3):
						if resultOfZi[x]['xiaoyun']==jpwh.xiaoyun:
							resultOfZi[x]['wu']=safeAppend('wu',jpwh.wu,resultOfZi[x])
							resultOfZi[x]['han']=safeAppend('han',jpwh.han,resultOfZi[x])
							found=True
							break
					if not found:
						resultOfZi[0]['wu'] = safeAppend('wu',jpwh.wu,resultOfZi[0])
						resultOfZi[0]['han'] = safeAppend('han',jpwh.han,resultOfZi[0])

		if len(one.kr)>0:
			size4 = len(resultOfZi)			
			if size4==0:
				line={}
				for kryx in one.kr[0].yinxun:
					ky=""
					if kryx.liu == "":
						ky=kryx.yin
					else:
						ky=kryx.yin+"("+kryx.liu+")"
					line['kr'] = safeAppend('kr',ky,line)
				resultOfZi.append(line)
			elif size4==1:
				for kryx in one.kr[0].yinxun:
					ky=""
					if kryx.liu == "":
						ky=kryx.yin
					else:
						ky=kryx.yin+"("+kryx.liu+")"
					resultOfZi[0]['kr'] = safeAppend('kr',ky,resultOfZi[0])
			elif size4>1:
				for kryx in one.kr[0].yinxun:
					found=False
					for x in range(0,size4):
						if resultOfZi[x]['xiaoyun']==kryx.xiaoyun:
							ky=""
							if kryx.liu == "":
								ky=kryx.yin
							else:
								ky=kryx.yin+"("+kryx.liu+")"
							resultOfZi[x]['kr']=safeAppend('kr',ky,resultOfZi[x])
							found=True
							break
					if not found:
						ky=""
						if kryx.liu == "":
							ky=kryx.yin
						else:
							ky=kryx.yin+"("+kryx.liu+")"
						resultOfZi[0]['kr'] = safeAppend('kr',ky,resultOfZi[0])

		if len(one.vn)>0:
			size5 = len(resultOfZi)	
			if size5==0:
				line={}
				for vny in one.vn[0].yin:
					line['vn'] = safeAppend('vn',vny.yin,line)
				resultOfZi.append(line)
			elif size5==1:
				for vny in one.vn[0].yin:
					resultOfZi[0]['vn'] = safeAppend('vn',vny.yin,resultOfZi[0])
			elif size5>1:
				for vny in one.vn[0].yin:
					found=False
					for x in range(0,size5):
						if resultOfZi[x]['xiaoyun']==vny.xiaoyun:
							resultOfZi[x]['vn']=safeAppend('vn',vny.yin,resultOfZi[x])
							found=True
							break
					if not found:
						resultOfZi[0]['vn'] = safeAppend('vn',vny.yin,resultOfZi[0])

		[results.append(y) for y in resultOfZi]

	return results

def safeAppend(dst,src,dic):
	if dst in dic.keys() and dic[dst]!="":
		# if dic[dst].find("...")>=0:
		# 	return dic[dst]
		# else:
		return dic[dst]+","+src
	else:
		return src


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    # app.run()