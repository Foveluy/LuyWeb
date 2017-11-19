#!/usr/bin/env python3

from luya import Luya
from luya import response
from luya import blueprint

PRINT = 1


app = Luya()

bp = blueprint.Blueprint('zhengfang',prefix_url='/bp')
@bp.route('/<tag:number>')
async def helloWorld(request, tag=None):

    return response.html('''
            <div>
                <h1>
                    hello, {}
                </h1>
            </div>'''.format(tag))




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


# @app.route('/<tag>')
# async def helloWorld(request, tag=None):

#     return response.html('''
#             <div>
#                 <h1>
#                     hello, {}
#                 </h1>
#             </div>'''.format(tag))

@app.route('/')
async def helloWorld(request):

    return response.text('hello,world')



if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run()
    pass
