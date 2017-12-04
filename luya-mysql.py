from sqlalchemy import Column, String, Integer
from aiomysql.sa import create_engine
import sqlalchemy
import pymysql

import asyncio
import uvloop


class LuyaMysql():
    def __init__(self):
        self.loop = None
        self.engine = None

    async def init_engine(self):
        try:
            if self.loop is None:
                self.loop = asyncio.get_event_loop()
            self.engine = await create_engine(user='root', db='TrainNote', host='127.0.0.1',
                                              password='metal_gear2', loop=self.loop)
        except Exception as e:
            # todo:has to do a log system
            print(e)

    async def connection(self):
        try:
            async with self.engine.acquire() as conn:
                return conn
        except Exception as e:
            print(e)


async def insert(loop):
    engine = await create_engine(user='root', db='TrainNote', host='127.0.0.1',
                                 password='metal_gear2', loop=loop)

    async with engine.acquire() as conn:
        await conn.execute(user.insert().values(name='shit'))

        async for row in conn.execute(user.select().where(user.c.id == 10)):
            print(row)

        trans = await conn.begin()
        await trans.commit()
