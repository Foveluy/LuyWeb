#!/usr/bin/env python3
# coding:utf-8
from flask import Flask, jsonify, request, Response, abort
from sqlalchemy import Column, Integer, String, create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from db import db
import time

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:


class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


app = Flask(__name__)
DBInstance = db()
cache = []


@app.route("/exercise", methods=['POST'])
def add():
    content = request.form.get('content', None)
    if not content:
        abort(400)

    now = str(time.time())

    new_user = User(id=now, name='Bob')
    DBInstance.insert(new_user)
    print(content)
    return Response()


@app.route('/data')
def data():
    if len(cache) <= 0:
        user = DBInstance.fetch(User)
        for one in user:
            cache.append(one.name)

    return jsonify(cache)


@app.route("/")
def hello():
    return jsonify(msg='hello world')

from login import login
app.register_blueprint(login,url_prefix='/login')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
