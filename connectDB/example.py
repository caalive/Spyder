#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/25 9:14 PM
# Author : CA

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date


#创建连接字段
HOST_NAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'root'
PASSWORD = 'root'

#创建数据库引擎连接数据库,固定格式
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                           PASSWORD,
                                                           HOST_NAME,
                                                           PORT,
                                                           DATABASE)

engine = create_engine(DB_URI)
Base = declarative_base(engine)

class User(Base):
    __tablename__ = 'muiltype'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    gender = Column(Boolean)
    register_time = Column(DateTime, default=datetime.now)
    birth_time = Column(Date)

Base.metadata.create_all()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()


root = User(name='root', gender=True, birth_time=date(2015, 5 ,23))
session.add(root)
session.commit()


