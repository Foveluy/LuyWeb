"""
LuyA
"""
import codecs
import os
import re
from distutils.errors import DistutilsPlatformError
from distutils.util import strtobool

from setuptools import setup


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        *paths
    )

    return codecs.open(path, mode, encoding)


with open_local(['luya', '__init__.py'], encoding='latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

# with open_local(['README.rst']) as rm:
#     long_description = rm.read()

setup_kwargs = {
    'name': 'luya',
    'version': version,
    'url': 'https://github.com/215566435/LuyWeb',
    'license': 'MIT',
    'author': 'Zheng Fang',
    'author_email': 'snakegear@163.com',
    'description': (
        'a flask like framework'),
    'long_description': 'a flask like framework',
    'packages': ['luya'],
    'platforms': 'any',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

ujson = 'ujson>=1.35'
uvloop = 'uvloop>=0.5.3'

requirements = [
    'httptools>=0.0.9',
    uvloop,
    ujson,
    'aiofiles>=0.3.0',
    'websockets>=4.0',
]


setup_kwargs['install_requires'] = requirements
setup(**setup_kwargs)
