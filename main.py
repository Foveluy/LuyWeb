#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from db import db
import time
from socket import *


# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

sock = socket(AF_INET, SOCK_STREAM)


class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


DBInstance = db()
cache = []


def hello(text):
    print('hello,', text)

    def decorator(func):
        def wrapper(*args, **kw):
            print('我在这里内嵌了一个牛逼东西')
            return func(*args, **kw)

        return wrapper
    
    return decorator

def login(func):
    print('登陆')

    def decorator(*args, **kw):
        return func(*args, **kw)
    return decorator


# @hello('牛逼')
# @login
def world(name, ff):
    print('world func:', name, ff)


# world('方正','牛逼')

hello('牛逼')(world)('方正','牛逼')
# newWorld = decorator(world)
# newWorld('方正','牛逼')


# from sanic import Sanic
# from sanic.response import json

# app = Sanic(__name__)


# @app.route("/")
# async def test(request):
#     if len(cache) <= 0:
#         user = DBInstance.fetch(User)
#         for one in user:
#             cache.append(one.name)
#     return json(cache)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)
