# complementary packages via pip for the enviroments unable to be installed
# using conda env create -f myproject.yml

import os

packages = [
    "build",
    "sphinx-rtd-theme",
    "chardet",
    "charset_normalizer",]

for pkg in packages:
    os.system(f'pip install --upgrade {pkg}')