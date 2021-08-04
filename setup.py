__author__ = 'samantha'
from setuptools import setup, find_packages

setup(name='sja_utils',
      version='0.1',
      description='python utilities',
      author='Samantha Atkins',
      author_email='samantha@conceptwareinc.com',
      license='internal',
      packages=find_packages(exclude='test'),
      scripts=['sja_utils/word_pass'],
      install_requires = ['validators', 'requests', 'beautifulsoup4', 'pyyaml'],
      zip_safe=False)
