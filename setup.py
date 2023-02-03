# -*- coding: utf-8 -*-

from setuptools import setup

PATH = 'C:\\Users\\User\\Desktop\\Python\\Projects\\Project-chemeq'
with open(PATH + "\\chemeq\\README.md", "r") as file:
    description_long = file.read()

setup(
      name='chemeq',
      version='0.1.1',
      description='''library for balancing chemical equations and periodic table of elements''',
      author="Elbio Peña",
      author_email="elbioemilio@outlook.es",
      url="github.com/elbiop/chemeq",
      py_modules=["chemeq"],
      requires=["numpy", "pandas"],
      install_requires=["numpy", "pandas"],
      python_requires=">= 3.6",
      keywords=["chemistry", "chemical", "equation", "balance",
                "balancer", "balancing", "periodic table", "elements"],
      classifiers=["Development status ::  8 - Implementation",
                   "Intended audienence :: Students, Developers",
                   "Operating System :: Windows",
                   ],
      long_description=description_long,
      long_description_content_type="text/markdown",
      package_dir={'': PATH}
     )
