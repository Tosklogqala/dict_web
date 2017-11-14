# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:27:28 2017

@author: Administrator
"""
# import io
# import sys
# sys.path.append("..")

# from datetime import datetime
import flask


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# if __name__ == '__main__':
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import dictWebServer.views