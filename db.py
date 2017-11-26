from sqlalchemy import Column, String, Integer
from aiomysql.sa import create_engine
import sqlalchemy

import asyncio
import uvloop


metadata = sqlalchemy.MetaData()
user = sqlalchemy.Table('user', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(20)),
                        Column('fullname', String(40)),
                        Column('createTime', String(40)))


async def insert(loop):
    engine = await create_engine(user='root', db='TrainNote', host='127.0.0.1',
                                 password='metal_gear2', loop=loop)
    async with engine.acquire() as conn:
        await conn.execute(user.insert().values(name='shit'))

        async for row in conn.execute(user.select()):
            print(row)

        trans = await conn.begin()
        await trans.commit()

    engine.close()
    engine.terminate()
    await engine.wait_closed()


loop = uvloop.new_event_loop()
tasks = [insert(loop), insert(loop)]

loop.run_until_complete(asyncio.wait(tasks, loop=loop))


loop.close()

#文档：https://aiomysql.readthedocs.io/en/latest/sa.html
