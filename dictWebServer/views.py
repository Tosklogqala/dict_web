# -*- coding: utf-8 -*-
from dictWebServer import app

import flask
from flask import jsonify
from .dbModel import dbmodel
import collections
import re
import json
from .tools import myTools as tl
from .tools import queryTools as qt

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
	zi = flask.request.args["zi"]
	opt= flask.request.args["opt"]
	page = 1
	if 'page' in flask.request.args:
		page = int(flask.request.args['page'])

	
	ext={}
	ext["zi"]=zi
	ext["opt"]=opt
	ext["curpage"]=page
	ext["totalpage"]=1
	ext["err"]=0

	results=[]
	if opt=="hanzi":
		ext["err"],results = qt.queryTools().danHanzi(zi)
		if ext["err"]==1:
			return flask.render_template("zisearch.html",results=results)
	elif opt=="sheng":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danSheng(zi,page)
	elif opt=="yun":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danYun(zi,page)
	elif opt=="xiaoyun":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danXiaoyun(zi,page)
	elif opt=="pychn":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danPinyin(zi,page)
	elif opt=="zgys":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danZgys(zi,page)
	elif opt=="jpnwu":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danJpn(zi,page,"wu")
	elif opt=="jpnhan":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danJpn(zi,page,"han")
	elif opt=="kor":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danKor(zi,page)
	elif opt=="vnm":
		ext["err"],results,ext["totalpage"] = qt.queryTools().danVnm(zi,page)

	return flask.render_template('dansearch.html',results=results,ext=ext)

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
		session.close()

	return trans
