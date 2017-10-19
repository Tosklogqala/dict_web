# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:27:28 2017

@author: Administrator
"""
from datetime import datetime
import flask
from flask import jsonify

import pymysql
import collections

import io
import sys
sys.path.append("..")
import myTools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=['GET'])
def index():
	print("index")
	return flask.render_template('trans.html')
    # print("index")
    # return flask.render_template('pure.html')

@app.route('/search',methods=['POST'])
def search():
	# print("search")
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
	db = pymysql.connect(**myTools.MYSQL_CONFIG)
	if src=="zgys" and dst=="hanzi":
		doTranslate(db,txt,src,dst,trans)
	# zgys是用空格分词的，汉字尚未分成一个一个的字
	if src=="hanzi" and dst=="zgys":
		doTranslate(db,txt,src,dst,trans)

	db.close()
	return jsonify(trans)


def doTranslate(db,txt,src,dst,trans):
	sql = "SELECT " + dst + " FROM maintable WHERE " + src + " =%s"
	with db.cursor() as cursor:
		try:
			restxt= str.split(txt," ")
			for zi in restxt:
				cursor.execute(sql,(zi))
				results = cursor.fetchall()
				do = []
				for dan in results:
					do.append(dan[dst])
				print(do)
				trans["results"].append(do)
		except Exception as e:
			print(e)
			trans={}
	return trans


if __name__ == '__main__':
    app.run(debug=True)