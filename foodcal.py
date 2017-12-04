#!/usr/bin/env python3
import aiohttp
from luya import Luya
from luya import response
from luya import blueprint
from luya.exception import NOT_FOUND
from luya.view import MethodView

from lxml import etree


food_bp = blueprint.Blueprint('zhengfang', prefix_url='/food')

headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0)\
     AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Accept": "text/html"
}


async def fetch(url):
    '''
    这个函数是使用了aiphttp来异步获取数据
    parma url:获取数据的地址
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            Html = await res.text(encoding='utf-8')
            return Html


class SearchFood():
    def __init__(self, name, gram=100):
        self.search_name = name
        self.real_name = ''
        self.spec_url = ''
        self.cal = ''
        self.food_specs = {}
        self.gram = gram

    @property
    def specs(self):
        '''
        计算食物的重量所对应的参数
        '''
        if self.gram != 100:
            cal = float(self.cal)
            carb = float(self.food_specs['碳水化合物'])
            fat = float(self.food_specs['蛋白质'])
            pro = float(self.food_specs['脂肪'])

            self.food_specs['cal'] = '%.1f' % (cal * self.gram / 100)
            self.food_specs['碳水化合物'] = '%.1f' % (carb * self.gram / 100)
            self.food_specs['蛋白质'] = '%.1f' % (pro * self.gram / 100)
            self.food_specs['脂肪'] = '%.1f' % (fat * self.gram / 100)

        return self.food_specs

    async def search(self):
        '''
        搜索引擎内的食物，并且转化成为食物的各项参数
        '''

        url_search = 'http://www.boohee.com/food/search?keyword={}'
        url_detail = 'http://www.boohee.com{}'
        xpath_title = '//div/h4/a'

        html = etree.HTML(await fetch(url_search.format(self.search_name)))
        result_name = html.xpath(xpath_title)
        self.real_name = result_name[0].text
        self.food_specs['real_name'] = result_name[0].text

        url = url_detail.format(str(result_name[0].attrib['href']))
        await self._search_specs(url)

    async def _search_from_database(self):
        pass

    async def _search_specs(self, url):
        xpath_cal = '//span[@id="food-calory"]/span'
        xpath_specs = '//dd/span'

        html = etree.HTML(await fetch(url))
        cal = html.xpath(xpath_cal)
        assert len(cal) == 1

        self.cal = cal[0].text
        self.food_specs['cal'] = cal[0].text

        result = html.xpath(xpath_specs)
        count = 0
        for index, item in enumerate(result):
            if '碳水化合物' in str(item.text):
                count += 1
                self.food_specs['碳水化合物'] = result[index + 1].text
            if '蛋白质' in str(item.text):
                count += 1
                self.food_specs['蛋白质'] = result[index + 1].text
            if '脂肪' in str(item.text):
                count += 1
                self.food_specs['脂肪'] = result[index + 1].text
            if count >= 3:
                break


@food_bp.route('/<foodname>/<gram:number>')
async def helloWorld(request, foodname=None, gram=100):
    food = SearchFood(foodname, gram=gram)
    await food.search()

    food_specs = food.specs

    print(request.args['123'])
    rsp_html = '''
            <div>
               <p>名字:{}</p>
                <p>热量:{}</p>
                <p>碳水化合物:{}</p>
                <p>脂肪:{}</p>
                <p>蛋白质:{}</p>
            </div>'''.format(food_specs['real_name'], food_specs['cal'],
                             food_specs['碳水化合物'], food_specs['脂肪'], food_specs['蛋白质'])
    return response.html(rsp_html)
