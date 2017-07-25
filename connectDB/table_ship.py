#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/25 9:56 PM
# Author : CA


from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
from sqlalchemy.orm import relationship


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

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    d_name = Column(String(50), nullable=False)

    def __repr__(self):
        return 'Department(d_id="%s", d_name="%s")' % (self.id, self.d_name)


class Student(Base):
    __tablename__ = 'student'
    s_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    gender = Column(Boolean)
    register_time = Column(DateTime, default=datetime.now)
    birth_time = Column(Date)
    d_id = Column(Integer, ForeignKey('department.id'))
    department = relationship('Department', backref='student')

    def __repr__(self):
        return 'Student(id="%s", name="%s", gender="%s", d_id="%s")' % (self.s_id, self.name, self.gender, self.d_id)


Base.metadata.create_all()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()


#d1 = Student(d_name='Math', gender=True, birth_time=date(2015, 5, 23))
# d1 = Department(d_name='Math')
# d2 = Department(d_name='Python')
# s3 = Student(name='kkk', gender=True, birth_time=date(2016, 3, 10), d_id=2)
# s4 = Student(name='yyy', gender=False, birth_time=date(2017, 4, 20), d_id=1)

# session.add_all([d1, d2])
# session.commit()
#
#
# session.add_all([s3, s4])
# session.commit()

# dept = session.query(Department).first()
# xiaohei = Student(name='xiaohei', gender=True, birth_time=date(2014, 4, 20), d_id=3)
# dept.student.append(xiaohei)
# session.commit()
#
# dept = session.query(Department).first()
# print(dept.student)

stu = session.query(Student).filter(Student.gender.like('1%')).all()
print(stu)