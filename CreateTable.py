#这里拥有一些使用sqlalchemy的演示，包括创建表，创建数据库
from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:


class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


# 初始化数据库连接:
engine = create_engine(
    'mysql+pymysql://root:metal_gear2@localhost:3306/TrainNote')

# 绑定元信息
metadata = MetaData(engine)
metadata.drop_all(engine)

# 创建表格，初始化数据库
user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(20)),
             Column('fullname', String(40)),
             Column('createTime', String(40))
             )
# 创建数据表，如果数据表存在则忽视！！！

metadata.create_all(engine)


# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='8', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()
