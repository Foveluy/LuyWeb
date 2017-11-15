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


from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.route("/")
async def test(request):
    if len(cache) <= 0:
        user = DBInstance.fetch(User)
        for one in user:
            cache.append(one.name)
    return json(cache)


@app.route('/<tag:\d+>')
async def first(request, tag=None):

    return json({'shit': tag, 'number': 123})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, workers=1, debug=False)
