from sqlalchemy import Column, String, Integer,VARCHAR,Float
from aiomysql.sa import create_engine
import sqlalchemy
import pymysql

import asyncio
import uvloop


metadata = sqlalchemy.MetaData()
food = sqlalchemy.Table('food', metadata,
                        Column('id', Integer, primary_key=True,
                               autoincrement=True, default=1),
                        Column('sname', VARCHAR(20)),
                        Column('fullname', VARCHAR(40)),
                        Column('cal', Float(40)),
                        Column('pro', Float(40)),
                        Column('carb', Float(40)),
                        Column('fat', Float(40)),
                        Column('createTime', String(40)))


ENGINE = sqlalchemy.create_engine("mysql+pymysql://root:metal_gear2@localhost:3306/TrainNote?charset=utf8",
                                  convert_unicode=True)
food.drop(bind=ENGINE)
food.create(bind=ENGINE)



# async def insert(loop):
#     engine = await create_engine(user='root', db='TrainNote', host='127.0.0.1',
#                                  password='metal_gear2', loop=loop)

#     async with engine.acquire() as conn:
#         await conn.execute(user.insert().values(name='shit'))

#         async for row in conn.execute(user.select().where(user.c.id == 10)):
#             print(row)

#         trans = await conn.begin()
#         await trans.commit()

#     engine.close()
#     engine.terminate()
#     await engine.wait_closed()


# loop = uvloop.new_event_loop()

# tasks = [insert(loop), insert(loop)]

# loop.run_until_complete(asyncio.wait(tasks, loop=loop))


# loop.close()

# 文档：https://aiomysql.readthedocs.io/en/latest/sa.html
