from setuptools import setup, find_packages

setup(
  name='leprechaun',
  version="2.0",
  description="A simple rainbow table generator",
  long_description=open("README.rst", encoding="utf-8").read(),
  author="Zach Dziura",
  author_email="zcdziura@gmail.com",
  url="https://github.com/zcdziura/leprechaun",
  license="MIT",
  packages=find_packages(),
  package_data={
    "wordlist": ["leprechaun/data/wordlist.txt"]
  }
)
