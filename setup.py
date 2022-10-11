__author__ = 'samantha'
from setuptools import setup, find_packages
packages = find_packages(exclude=['test'])

setup(name='sjautils',
      version='0.1',
      description='python utilities',
      author='Samantha Atkins',
      author_email='samantha@conceptwareinc.com',
      license='internal',
      packages=packages,
      scripts=['sjautils/word_pass'],
      install_requires = ['validators', 'requests', 'beautifulsoup4', 'pyyaml'],
      zip_safe=False)
