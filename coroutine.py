import time


def sleep():
    _sec = 0
    yield _sec
    print('我是睡觉程序')


def child():

    r = '我是子程序'
    yield r
    print('我第一次')
    yield r
    print('我第二次')
    yield r
    print('我第三次')


def main(c):
    # 如果你直接调用c()，那么会出错
    # 错误是TypeError: 'generator' object is not callable
    while True:
        try:
            c.send(None)
        except StopIteration as e:
            print('子程序运行完毕啦～')
            break


c = child()


main(c)

