from luya import Luya
import asyncio

app = Luya('things')


def test():
    res = app.test_client().get(url='/')
    print(res)


test()
