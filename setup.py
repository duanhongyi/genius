#coding:utf-8

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


requires = [
    'nose',
    'libwapiti',
    'setuptools>=1.0',
]


setup(

    name='genius',
    description='genius中文分词 Chinese Segment On linear-chain CRF',
    version='2.1.1',
    author='duanhongyi',
    author_email='duanhyi@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/duanhongyi/genius',
    install_requires=requires,
    dependency_links=[
        'git+https://github.com/duanhongyi/python-wapiti.git#egg=wapiti-1.0',
    ],
    platforms='all platform',
    license='BSD',
)
