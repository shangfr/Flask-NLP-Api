# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:04:28 2021

@author: shangfr
"""

from server import create_app


app = create_app('dev')


if __name__ == '__main__':
    app.run()