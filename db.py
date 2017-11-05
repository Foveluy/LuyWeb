from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class db:
    def __init__(self):
        # 初始化数据库连接:
        engine = create_engine(
            'mysql+pymysql://root:metal_gear2@localhost:3306/TrainNote')

        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=engine)

    def insert(self, model):
        # 创建session对象:
        session = self.DBSession()
        # 添加到session:
        session.add(model)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
    def fetch(self,model):
        session = self.DBSession()
        fetch = session.query(model).all()
        session.close()
        return fetch
