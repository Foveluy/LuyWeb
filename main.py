#!/usr/bin/env python3
import aiohttp
from luya import Luya
from luya import response
from luya import blueprint


from foodcal import food_bp

app = Luya()


if __name__ == '__main__':
    app.register_blueprint(food_bp)
    app.run()