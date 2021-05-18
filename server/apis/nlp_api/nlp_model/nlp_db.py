# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:27:11 2021

@author: shangfr
"""

from sqlalchemy import text
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

# sqlalchemy orm模式-创建表-插入数据
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
engine = create_engine('sqlite:///nlp.db', echo=True)

Base = declarative_base()


class UserDict(Base):
    __tablename__ = 'user_dict'

    id = Column(Integer, primary_key=True)
    word = Column(String(30))
    freq = Column(Integer,default=10)
    tag = Column(String)

    addresses = relationship("Address", back_populates="userdict")

    def __repr__(self):
        return f"UserDict(id={self.id!r}, word={self.word!r}, tag={self.tag!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    full_address = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey('user_dict.id'))

    userdict = relationship("UserDict", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, full_address={self.full_address!r})"

class EventType(Base):
    __tablename__ = 'event_words'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    keyword = Column(String, nullable=False)

    def __repr__(self):
        return f"EventType(id={self.id!r}, category={self.category!r})"


UserDict.__table__

Base.metadata.create_all(engine)

# 使用Session插入数据
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
sessionobj = Session()

word01 = UserDict(word="云计算", freq=10,tag='n')
word02 = UserDict(word="中国梦")
#sessionobj.add(word01)
sessionobj.add_all([word01,word02])
sessionobj.commit()


address02 = Address(full_address='华山一号院12栋',userdict = word01)
sessionobj.add(address02)
sessionobj.commit()

sessionobj.close()
