from Luya import Luya

PRINT = 1


app = Luya()


@app.route('/')
def helloWorld(request):
    print('helloWorld')
    return


@app.route('/')
def helloWorld(request):
    print('helloWorld')
    return


if __name__ == '__main__':
    pass
    # app.run()
