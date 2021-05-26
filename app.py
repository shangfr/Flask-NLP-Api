# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:40:56 2021

@author: shangfr
"""

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000, debug = True, ssl_context='adhoc')