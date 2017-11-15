# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:27:28 2017

@author: Administrator
"""

import flask

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
if __name__ == '__main__':
	app.run()


import dictWebServer.views