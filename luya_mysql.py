from sqlalchemy import Column, String, Integer
from aiomysql.sa import create_engine
import aiomysql
import sqlalchemy
import pymysql
import logging

import asyncio
import uvloop


class LuyaMysql():
    def __init__(self):
        self.loop = None
        self.engine = None

    async def init_engine(self):
        '''
        初始化引擎
        '''
        try:
            logging.warning('初始化')
            if self.loop is None:
                self.loop = asyncio.get_event_loop()
            self.engine = await create_engine(user='root', db='TrainNote', host='127.0.0.1',
                                              password='metal_gear2', loop=self.loop, charset='utf8', use_unicode=True)
        except Exception as e:
            # todo:has to do a log system
            logging.error(e)

    async def connection(self):
        '''
        返回一个connection
        可以用做增删查改
        '''
        try:
            if self.engine is None:
                await self.init_engine()

            async with self.engine.acquire() as conn:
                return conn
        except Exception as e:
            logging.error(e)


sqlInstance = LuyaMysql()
