# -*- coding: utf-8 -*-
"""
Created on Thu May 13 14:33:23 2021

@author: shangfr
"""

from server import create_app
from flask_script import Manager

app=create_app('dev')
manager=Manager(app)

@manager.command
def run():
    app.run()
    

if __name__ == '__main__':
    manager.run()