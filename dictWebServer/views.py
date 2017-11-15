# -*- coding: utf-8 -*-
from dictWebServer import app

import flask
from flask import jsonify
from .dbModel import dbmodel
import collections
import re
from .tools import myTools as tl

import os


@app.route('/',methods=['GET'])
def index():
	print("index")
	# print(os.path.split(os.path.realpath(__file__)))
	# print(myTools.SQL_URL)
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
		session = dbmodel.getSession(tl.SQL_URL)
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
	
	session = dbmodel.getSession(tl.SQL_URL)
	zilist = session.query(dbmodel.hanzi).filter(dbmodel.hanzi.zi==zi).all()
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danSheng(zi,offset):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(tl.SQL_URL)
	zglist = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.sheng==zi).order_by(dbmodel.zgchn.id).offset(offset).limit(10)
	zilist = []
	[zilist.append(yun.hanzi) for yun in zglist if not yun.hanzi in zilist]
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danYun(zi,offset):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(tl.SQL_URL)
	zglist = session.query(dbmodel.zgchn).filter(dbmodel.zgchn.yun==zi).all()
	zilist = []
	[zilist.append(yun.hanzi) for yun in zglist if not yun.hanzi in zilist]
	results = parseFromZiList(zilist)
	session.close()
	return 0,results

def danXiaoyun(zi):
	if len(zi)<1 or len(zi)>1:
		return -1,[]

	session = dbmodel.getSession(tl.SQL_URL)
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

		if len(one.sg)>0:
			langAddToColumn(one.sg,resultOfZi,addSg)

		if len(one.py)>0:
			langAddToColumn(one.py,resultOfZi,addPy)

		if one.jpn_id != None:
			langAddToColumn(one.jp.wuhan,resultOfZi,addJp)

		if len(one.kr)>0:
			langAddToColumn(one.kr[0].yinxun,resultOfZi,addKr)

		if len(one.vn)>0:
			langAddToColumn(one.vn[0].yin,resultOfZi,addVn)

		[results.append(y) for y in resultOfZi]

	return results

def addSg(entry,ary,bold=True):
	safeAppend('shengfu',entry.shengfu,ary)
	safeAppend('yunbu',entry.yunbu,ary)
	safeAppend('sgzz',entry.sgzz,ary)

def addPy(entry,ary,bold=True):
	if bold==True:
		safeAppend('pinyin',entry.pinyin,ary)
	else:
		safeAppend('pinyin',"<i>"+entry.pinyin+"</i>",ary)

def addJp(entry,ary,bold=True):
	if bold==True:
		safeAppend('wu',entry.wu,ary)
		safeAppend('han',entry.han,ary)
	else:
		safeAppend('wu',"<i>"+entry.wu+"</i>",ary)
		safeAppend('han',"<i>"+entry.han+"</i>",ary)

def addKr(entry,ary,bold=True):
	ky=""
	if entry.liu == "":
		ky=entry.yin
	else:
		ky=entry.yin+"("+entry.liu+")"
	safeAppend('kr',ky,ary)

def addVn(entry,ary,bold=True):
	safeAppend('vn',entry.yin,ary)

def langAddToColumn(lang,dic,func):
	size = len(dic)
# 若不存在中古韻，建立新的行来填写本语言信息
	if size == 0:
		line={}
		for entry in lang:
			func(entry,line)
		dic.append(line)
# 若只有一個中古韻，則顯示在一行。（也许上古多于一行时，应建立新的行？）
	elif size==1:
		for entry in lang:
			#填在第一行而不匹配当行中古韵的读音，用特殊字体标识
			if dic[0]['xiaoyun']==entry.xiaoyun:
				func(entry,dic[0])
			else:
				func(entry,dic[0],False)
	elif size>1:
# 若存在多个中古韻，則能匹配的填在對應的後面。
		for entry in lang:
			found=False
			for x in range(0,size):
				if dic[x]['xiaoyun']==entry.xiaoyun:
					func(entry,dic[x])
					found=True
					break
# 若不能匹配到中古韻。則填在第一行。
			#填在第一行而不匹配当行中古韵的读音，用特殊字体标识
			if not found:
				func(entry,dic[0],False)

def safeAppend(dst,src,dic):
	if dst in dic.keys() and dic[dst]!="":
		dic[dst] = dic[dst] + "," + src
	else:
		dic[dst] = src