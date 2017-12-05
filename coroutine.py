from luya import Luya
import asyncio

app = Luya('things')

async def test():
    res = await app.test_client().get(url='/')

loop = asyncio.get_event_loop()

loop.run_until_complete(test())
