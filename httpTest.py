#!/usr/bin/env python3

from luya import Luya
from luya import response

PRINT = 1


app = Luya()


def login(func):
    async def wrapper(*arg, **kw):
        if 3 > 5:
            return func(*arg, **kw)
        else:
            return response.html('''
            <div>
                <h1>
                    please login
                </h1>
            </div>''')

    return wrapper


@app.route('/')
@login
async def helloWorld(request):
    return response.html('''
            <div>
                <h1>
                    hello, Zheng123123hello
                </h1>
            </div>''')


if __name__ == '__main__':
    app.run()
