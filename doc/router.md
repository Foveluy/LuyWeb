router模块
====

router模块要做的事情就是帮助函数解析url，解析url包括：
- /url/<id:name> 非传统
- /url/?name=***&id=xxx 传统
- '/number/<integer_arg:int> url检查

以及指定各种http请求方式
- POST
- GET
- DELETE
- PUT
- patch


http 短方法
- @get
- @post


class-based views
用于定义一个类，类里面有method