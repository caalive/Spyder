#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/21 8:55 PM
# Author : CA

#导入数据库引擎
from sqlalchemy import create_engine

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
#创建引擎
engine = create_engine(DB_URI)
print(type(engine))


#创建数据库表,声明映像
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)

#创建数据库表对应的类
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(30))

    def __repr__(self):
        return 'User(id={},username={},password={})'.format(self.id, self.username, self.password)

#将对应类映射到数据库的表中
Base.metadata.create_all()

#创建数据库表会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()

#添加数据
def add_user():
    # 增加数据,添加单个对象　　
    # caa = User(username='fff', password='123456')
    # session.add(caa)
    # 添加多个对象
    session.add_all([
        User(username='cbb', password='root'),
        User(username='ccc', password='gen'),
        User(username='ddd', password='hot')
    ])
    session.commit()


#查找数据
def search_user():
    result = session.query(User).all()
    result = session.query(User).first()
    print(result.password)

    result = session.query(User).filter_by(password='hot').all()
    #result为对象的列表
    result = session.query(User).filter(User.username == 'caa').all()
    print(result)

#修改数据
def modfiy_user():
    result = session.query(User).filter_by(password='123456')[0]
    #result为类对象,可以使用类的操作方法
    result.password = 'caaroot'
    session.commit()
    print(result)

def delete_uesr():
    #删除数据
    result = session.query(User).filter(User.username == 'cbb')[0]
    session.delete(result)
    session.commit()



#search_user()


#条件查询等于 ==
result = session.query(User).filter(User.username == 'caa').all()[0]
# print(result)

#条件查询不等于 !=
result = session.query(User).filter(User.username !='caa').all()
# print(result)

#模糊匹配 like
result = session.query(User).filter(User.username.like('c%')).all()
#print(result)

#成员所属(in_)
result = session.query(User).filter(User.username.in_(['caa', 'ccc'])).all()
# print(result)

#不属于notin 类名前加~ 波浪线
result = session.query(User).filter(~User.username.in_(['caa', 'ccc'])).all()
result = session.query(User).filter(User.username.notin_(['caa', 'ccc'])).all()
# print(result)

#查询数据为空 is null
result = session.query(User).filter(User.password == None).all()
result = session.query(User).filter(User.password.is_(None)).all()
# print(result)

#查询数据不为空 is not none
result = session.query(User).filter(User.password != None).all()
# print(result)
result = session.query(User).filter(User.password.isnot(None)).all()
# print(result)

#多条件过滤查询
result = session.query(User).filter(User.username == 'caa', User.password == 'caaroot').all()
# print(result)
result = session.query(User).filter_by(username = 'caa',password = 'caaroot').all()
# print(result)

#多条件或查询
from sqlalchemy import or_
result = session.query(User).filter(or_(User.username == 'caa', User.password == 'hot')).all()
print(result)



