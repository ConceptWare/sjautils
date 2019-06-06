__author__ = 'samantha'
from setuptools import setup, find_packages

setup(name='cwutils',
      version='0.1',
      description='python utilities',
      author='Samantha Atkins',
      author_email='samantha@conceptwareinc.com',
      license='internal',
      packages=['cwutils'],
      scripts=['cwutils/word_pass'],
      install_requires = ['validators'],
      zip_safe=False)
