# -*- coding: utf-8 -*-
from setuptools import setup
import os

PATH = os.getcwd()
with open(PATH + os.sep + "README.txt", "r") as file:
    description_long = file.read()

setup(
      name='chemeq',
      version='0.1.1',
      description='''Balance chemical equations, periodic table of elements''',
      author="Elbio Peña",
      author_email="elbioemilio@outlook.es",
      url="github.com/elbiop/chemeq",
      py_modules=["chemeq"],
      requires=["numpy", "pandas"],
      install_requires=["numpy", "pandas"],
      python_requires=">= 3.6",
      keywords=["chemistry", "chemical", "chemicals", "equation",
                "equations", "balance", "balancer", "balancing", "reaction",
                "reactions" "periodic table", "elements"],
      classifiers=["DEVELOPMENT STATUS::5-PRODUCTION/STABLE",
                   "INTENDEN AUDIENCE::EDUCATION",
                   "PROGRAMMING LANGUAGE::PYTHON",
                   "INTENDED AUDIENCE::END USER/DESKTOP",
                   "INTENDED AUDIENCE::SCIENCE/RESEARCH",
                   ],
      long_description=description_long,
      long_description_content_type="text/markdown",
      package_dir={'': PATH}
     )
