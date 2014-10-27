#coding:utf-8

import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(here, 'README.md')
changes_file = os.path.join(here, 'CHANGES.txt')

def read_text(file_path):
    """
    fix the default operating system encoding is not utf8
    """
    if sys.version_info.major < 3:
        return open(file_path).read()
    return open(file_path, encoding="utf8").read()

README = read_text(os.path.join(here, 'README.md'))
CHANGES = read_text(os.path.join(here, 'CHANGES.txt'))

requires = [
    'six',
    'nose',
    'libwapiti',
    'setuptools>=1.0',
]


setup(

    name='genius',
    description='genius中文分词 Chinese Segment On linear-chain CRF',
    version='3.1.4',
    author='duanhongyi',
    author_email='duanhyi@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/duanhongyi/genius',
    install_requires=requires,
    platforms='all platform',
    license='BSD',
)
