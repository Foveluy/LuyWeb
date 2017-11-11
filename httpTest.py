from luya import Luya

PRINT = 1


app = Luya()


@app.route('/')
async def helloWorld(request):
    return '''
            <div>
                <h1>
                    hello, Zheng123123hello
                </h1>
            </div>'''


if __name__ == '__main__':
    app.run()
