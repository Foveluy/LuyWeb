from luya import Luya
from luya import response

PRINT = 1


app = Luya()


@app.route('/')
async def helloWorld(request):
    return response.html('''
            <div>
                <h1>
                    hello, Zheng123123hello
                </h1>
            </div>''')


if __name__ == '__main__':
    app.run()
