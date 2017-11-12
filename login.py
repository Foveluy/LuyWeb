
def add(func):
    print('添加了一段')
    def wapper(*arg,**kw):
        print('多此一举')
        print(*arg,**kw)
        return func(*arg,**kw)

    return wapper

@add
def log():
    print('log函数')





#==========以上相等

class user:
    def __init__(self):
        pass
    
    def user_log(self,url):
        print('string')

        def wrapper(fun):
            print('wrapper里')
        
        return wrapper


new_user = user()


@new_user.user_log('/')
def hello():
    print('hellop')
