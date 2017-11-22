#!/usr/bin/env python3
import aiohttp


from luya import Luya
from luya import response
from luya import blueprint
from luya.exception import NOT_FOUND


PRINT = 1


app = Luya()

bp = blueprint.Blueprint('zhengfang', prefix_url='/bp')


@bp.route('/<tag:number>')
async def helloWorld(request, tag=None):

    return response.html('''
            <div>
                <h1>
                    hello, {}
                </h1>
            </div>'''.format(tag))


@app.route('/')
async def helloWorld(request):
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://www.boohee.com/food/search?keyword=%E8%8B%B9%E6%9E%9C') as res:
    #         Html = await res.text(encoding='utf-8')
    #         print(Html)
    return response.html('''
            <div>
                <h1>
                    hello, {}
                </h1>
            </div>'''.format('http'))


# @app.exception(NOT_FOUND)
# async def helloWorld(request, exception):
#     return response.text('page not found')


if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run()
