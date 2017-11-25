#!/usr/bin/env python3
import aiohttp
from luya import Luya
from luya import response
from luya import blueprint
from luya.exception import NOT_FOUND
from luya.view import MethodView

from lxml import etree


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


headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS i686 2268.111.0)\
     AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Accept": "text/html"
}


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            Html = await res.text(encoding='utf-8')
            return Html


class SearchFood():
    def __init__(self, name):
        self.search_name = name
        self.real_name = ''
        self.spec_url = ''
        self.cal = ''
        self.food_specs = {}

    async def search(self):
        html = etree.HTML(await fetch(
            'http://www.boohee.com/food/search?keyword=' + self.search_name))
        result_name = html.xpath('//div/h4/a')
        self.real_name = result_name[0].text
        self.food_specs['real_name'] = result_name[0].text

        url = 'http://www.boohee.com' + str(result_name[0].attrib['href'])
        await self._search_specs(url)

    async def _search_specs(self, url):
        html = etree.HTML(await fetch(url))
        cal = html.xpath('//span[@id="food-calory"]/span')
        assert len(cal) == 1
        self.cal = cal[0].text
        self.food_specs['cal'] = cal[0].text

        result = html.xpath('//dd/span')
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


@app.route('/<foodname>')
async def helloWorld(request, foodname=None):
    food = SearchFood(foodname)
    await food.search()

    food_specs = food.food_specs

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


class fuck(MethodView):
    def __init__(self):
        pass

    def get(self, request):
        return response.html('<h1>class view test</h1>')


app.add_route(fuck.to_view(), '/123')
# @app.exception(NOT_FOUND)
# async def helloWorld(request, exception):
#     return response.text('page not found')


if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run()
