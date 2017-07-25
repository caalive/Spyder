
START_GROUP = 9
END_GROUP = 10

HOST_NAME = 'localhost'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'root'
PASSWORD = 'root'

#创建数据库引擎连接数据库,固定格式
DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                           PASSWORD,
                                                           HOST_NAME,
                                                           PORT,
                                                           DATABASE)


