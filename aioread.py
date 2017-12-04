import asyncio
import aiofiles 

async def good():
    async with aiofiles.open('./requirements.txt', mode='r') as f:
        contents = await f.read()
        print(contents)




loop = asyncio.get_event_loop()

server = loop.run_until_complete(good())